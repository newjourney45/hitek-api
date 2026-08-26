# api/index.py
# Real ICMR/HITEK Dataset API — Fetches from Hugging Face Parquet files

import os
import json
import pandas as pd
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# Dataset URLs (Hugging Face)
DATASET_URLS = [
    "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek/resolve/main/part1.parquet",
    "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek/resolve/main/part2a.parquet",
    "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek/resolve/main/part2b_new.parquet"
]

# Cache for loaded data (to avoid re-fetching on every request)
_data_cache = None

def load_all_data():
    """Load and combine all Parquet files from Hugging Face"""
    global _data_cache
    
    if _data_cache is not None:
        return _data_cache
    
    all_dfs = []
    for url in DATASET_URLS:
        try:
            print(f"📥 Loading: {url}")
            df = pd.read_parquet(url)
            all_dfs.append(df)
            print(f"✅ Loaded {len(df)} records from {url.split('/')[-1]}")
        except Exception as e:
            print(f"❌ Failed: {url} — {e}")
    
    if not all_dfs:
        return pd.DataFrame()
    
    combined = pd.concat(all_dfs, ignore_index=True)
    
    # Clean column names
    combined.columns = combined.columns.str.strip()
    
    # Map columns to standard names
    column_map = {
        'name': 'name',
        'fathersName': 'fathersName', 
        'phoneNumber': 'phoneNumber',
        'aadharNumber': 'aadharNumber',
        'otherNumber': 'otherNumber',
        'address': 'address',
        'district': 'district',
        'pincode': 'pincode',
        'state': 'state',
        'town': 'town',
        'source': 'source'
    }
    
    # Rename columns if they exist
    for old, new in column_map.items():
        if old in combined.columns:
            combined = combined.rename(columns={old: new})
    
    _data_cache = combined
    print(f"📊 Total records loaded: {len(combined)}")
    return combined


@app.get("/")
async def root():
    return {
        "success": True,
        "developer": "@Fghgddggf",
        "message": "ICMR/HITEK Dataset Search API",
        "usage": {
            "by_phone": "/?number=9876543210",
            "by_aadhaar": "/?aadhaar=123456789012",
            "by_name": "/?name=Rahul",
            "search_all": "/?q=Rahul"
        },
        "note": "⚠️ This API fetches real personal data from Hugging Face",
        "dataset": "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek"
    }


@app.get("/search")
@app.get("/")
async def search(
    number: str = Query(None, description="Phone number to search"),
    aadhaar: str = Query(None, description="Aadhaar number to search"),
    name: str = Query(None, description="Name to search"),
    q: str = Query(None, description="Search all fields"),
    limit: int = Query(100, description="Max results to return")
):
    """Search the dataset by phone, aadhaar, name, or general query"""
    
    # Help
    if number == "help" or q == "help" or name == "help":
        return {
            "success": True,
            "developer": "@Fghgddggf",
            "message": "Search Help",
            "usage": {
                "by_phone": "/?number=9876543210",
                "by_aadhaar": "/?aadhaar=123456789012",
                "by_name": "/?name=Rahul",
                "search_all": "/?q=Rahul"
            }
        }
    
    try:
        # Load data
        df = load_all_data()
        
        if df.empty:
            return JSONResponse({
                "success": False,
                "developer": "@Fghgddggf",
                "message": "No data loaded. Dataset may be unavailable.",
                "total": 0,
                "data": []
            })
        
        # Start with all data
        result_df = df.copy()
        
        # Apply filters
        if number:
            number = number.strip()
            # Search in phoneNumber and otherNumber
            result_df = result_df[
                (result_df['phoneNumber'].astype(str) == number) |
                (result_df['otherNumber'].astype(str) == number)
            ]
        
        elif aadhaar:
            aadhaar = aadhaar.strip()
            result_df = result_df[result_df['aadharNumber'].astype(str) == aadhaar]
        
        elif name:
            name = name.strip().lower()
            result_df = result_df[
                result_df['name'].str.lower().str.contains(name, na=False)
            ]
        
        elif q:
            q = q.strip().lower()
            # Search in all text columns
            text_cols = ['name', 'fathersName', 'phoneNumber', 'aadharNumber', 
                        'otherNumber', 'address', 'district', 'state', 'town']
            
            mask = pd.Series([False] * len(result_df))
            for col in text_cols:
                if col in result_df.columns:
                    mask = mask | result_df[col].astype(str).str.lower().str.contains(q, na=False)
            result_df = result_df[mask]
        
        # Limit results
        result_df = result_df.head(limit)
        
        # Convert to records
        records = result_df.to_dict(orient='records')
        
        # Clean NaN values
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        return {
            "success": True,
            "developer": "@Fghgddggf",
            "search_term": number or aadhaar or name or q or "all",
            "message": f"Found {len(records)} record(s)",
            "total": len(records),
            "data": records,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "developer": "@Fghgddggf",
            "message": f"Error: {str(e)}",
            "data": []
        })


@app.get("/stats")
async def stats():
    """Get dataset statistics"""
    try:
        df = load_all_data()
        return {
            "success": True,
            "developer": "@Fghgddggf",
            "total_records": len(df),
            "columns": list(df.columns),
            "states": df['state'].unique().tolist() if 'state' in df.columns else [],
            "sources": df['source'].unique().tolist() if 'source' in df.columns else []
        }
    except Exception as e:
        return {
            "success": False,
            "developer": "@Fghgddggf",
            "message": f"Error: {str(e)}"
        }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": pd.Timestamp.now().isoformat()}


# Vercel entry point
def handler(request, context):
    """Vercel serverless function entry point"""
    return app(request, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
