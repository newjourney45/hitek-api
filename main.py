from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import duckdb
import os

app = FastAPI()

# DuckDB - Bas ek baar connect karo
con = duckdb.connect()
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

@app.get("/")
def root():
    return {
        "status": "active",
        "message": "Hitek Data Gateway",
        "endpoint": "/FetchData?Number=XXXXXXXXXX",
        "developer": "@SOCIALBANNERR"
    }

@app.get("/FetchData")
def fetch_data(Number: str = Query(None)):
    # Validation
    if not Number or not Number.isdigit() or len(Number) < 10:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "10-15 digits only", "developer": "@SOCIALBANNERR"}
        )
    
    last_digit = Number[-1]
    
    # TERI LINK - Yahi se data lega
    url = f"https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main/alt_master_shard_{last_digit}.parquet"
    
    try:
        # DuckDB direct query - 2.62GB file bhi seconds mein
        query = f"SELECT * FROM read_parquet('{url}') WHERE alt = '{Number}'"
        result = con.execute(query).df()
        
        if result.empty:
            return JSONResponse(
                status_code=404,
                content={"status": "not_found", "phone": Number, "developer": "@SOCIALBANNERR"}
            )
        
        return {
            "status": "success",
            "phone": Number,
            "data": result.to_dict(orient="records"),
            "developer": "@SOCIALBANNERR"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "developer": "@SOCIALBANNERR"}
        )
