from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import duckdb
import os

app = FastAPI()

# DuckDB Connection
con = duckdb.connect()
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

@app.get("/")
def root():
    return {"status": "online", "message": "Hitek Data Gateway API"}

@app.get("/api/FetchData")
def fetch_data(Number: str = Query(None)):
    if not Number or not Number.isdigit() or len(Number) < 10:
        return JSONResponse(
            status_code=400,
            content={"status": "rejected", "message": "Invalid number"}
        )
    
    last_digit = Number[-1]
    primary_url = f"https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main/final_master_shard_{last_digit}.parquet"
    alt_url = f"https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main/alt_master_shard_{last_digit}.parquet"
    
    try:
        query = f"""
            SELECT *, 'Main' AS _record_type FROM read_parquet('{primary_url}') WHERE mobile = '{Number}'
            UNION ALL
            SELECT *, 'Alt' AS _record_type FROM read_parquet('{alt_url}') WHERE alt = '{Number}'
        """
        raw_results = con.execute(query).df().to_dict(orient="records")
        
        main_records = []
        alt_records = []
        for row in raw_results:
            rec_type = row.pop('_record_type')
            if rec_type == 'Main':
                main_records.append(row)
            else:
                alt_records.append(row)
        
        return {"status": "success", "Data": {"Main": main_records, "Alt": alt_records}}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

# Vercel Handler
from mangum import Mangum
handler = Mangum(app)
