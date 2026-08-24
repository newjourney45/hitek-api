from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
import requests
from io import BytesIO

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "active",
        "message": "Hitek Data Gateway API",
        "endpoints": {
            "/FetchData": "GET - Query with ?Number=XXXXXXXXXX"
        },
        "developer": "╭━━[ 𓃵 𝐏𝐀𝐓𝐄𝐋 𓃵 ]━━╮💀"
    }

@app.get("/FetchData")
def fetch_data(Number: str = Query(None)):
    # Validation
    if not Number:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Number parameter required",
                "usage": "/FetchData?Number=9876543210"
            }
        )
    
    if not Number.isdigit():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Number must contain only digits",
                "provided": Number
            }
        )
    
    if len(Number) < 10 or len(Number) > 15:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Number must be 10-15 digits",
                "provided": Number,
                "length": len(Number)
            }
        )
    
    try:
        # Get last digit for sharding
        last_digit = Number[-1]
        
        # Primary and Alt URLs
        primary_url = f"https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main/final_master_shard_{last_digit}.parquet"
        alt_url = f"https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main/alt_master_shard_{last_digit}.parquet"
        
        results = []
        
        # Try Primary
        try:
            response = requests.get(primary_url, timeout=30)
            if response.status_code == 200:
                df = pd.read_parquet(BytesIO(response.content))
                main_result = df[df['mobile'].astype(str) == Number]
                if not main_result.empty:
                    results.extend(main_result.to_dict(orient="records"))
        except:
            pass
        
        # Try Alt
        try:
            response = requests.get(alt_url, timeout=30)
            if response.status_code == 200:
                df = pd.read_parquet(BytesIO(response.content))
                alt_result = df[df['alt'].astype(str) == Number]
                if not alt_result.empty:
                    results.extend(alt_result.to_dict(orient="records"))
        except:
            pass
        
        if not results:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not_found",
                    "phone": Number,
                    "message": "Number not found in database"
                }
            )
        
        return {
            "status": "success",
            "phone": Number,
            "records_found": len(results),
            "data": results,
            "developer": "@SOCIALBANNERR"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "developer": "@SOCIALBANNERR"
            }
        )

# For Vercel
from mangum import Mangum
handler = Mangum(app)
