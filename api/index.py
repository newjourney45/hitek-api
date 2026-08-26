from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
import requests
from mangum import Mangum

app = FastAPI()

# Hugging Face Dataset
DATASET_URLS = [
    "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek/resolve/main/part1.parquet",
    "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek/resolve/main/part2a.parquet",
    "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek/resolve/main/part2b_new.parquet"
]

_data_cache = None

def load_data():
    global _data_cache
    if _data_cache is not None:
        return _data_cache
    
    all_dfs = []
    for url in DATASET_URLS:
        try:
            df = pd.read_parquet(url)
            all_dfs.append(df)
            print(f"✅ Loaded {len(df)} records")
        except Exception as e:
            print(f"❌ Failed: {url} — {e}")
    
    if all_dfs:
        _data_cache = pd.concat(all_dfs, ignore_index=True)
        print(f"📊 Total: {len(_data_cache)} records")
        return _data_cache
    return pd.DataFrame()


@app.get("/")
async def root(
    number: str = Query(None),
    aadhaar: str = Query(None),
    name: str = Query(None),
    q: str = Query(None)
):
    """Search the dataset"""
    
    # 📌 Agar koi search parameter nahi hai toh base response do
    if not any([number, aadhaar, name, q]):
        return {
            "success": True,
            "developer": "@Fghgddggf",
            "message": "ICMR/HITEK Dataset Search API",
            "usage": {
                "by_phone": "/?number=9693615642",
                "by_aadhaar": "/?aadhaar=511953762036",
                "by_name": "/?name=Babita",
                "search_all": "/?q=Babita"
            },
            "note": "⚠️ Fetches real personal data from Hugging Face",
            "dataset": "https://huggingface.co/datasets/kzr0xx/icmr-and-hitek"
        }
    
    # 📌 Help
    if number == "help" or q == "help":
        return {
            "success": True,
            "developer": "@Fghgddggf",
            "message": "Search Help",
            "usage": {
                "by_phone": "/?number=9693615642",
                "by_aadhaar": "/?aadhaar=511953762036",
                "by_name": "/?name=Babita",
                "search_all": "/?q=Babita"
            }
        }
    
    try:
        df = load_data()
        
        if df.empty:
            return {
                "success": False,
                "developer": "@Fghgddggf",
                "message": "No data loaded",
                "data": []
            }
        
        result_df = df.copy()
        
        # 🔍 Search Logic
        if number:
            number = number.strip()
            result_df = result_df[
                (result_df['phoneNumber'].astype(str) == number) |
                (result_df['otherNumber'].astype(str) == number)
            ]
        elif aadhaar:
            aadhaar = aadhaar.strip()
            result_df = result_df[result_df['aadharNumber'].astype(str) == aadhaar]
        elif name:
            name = name.strip().lower()
            result_df = result_df[result_df['name'].str.lower().str.contains(name, na=False)]
        elif q:
            q = q.strip().lower()
            text_cols = ['name', 'fathersName', 'phoneNumber', 'aadharNumber', 
                        'otherNumber', 'address', 'district', 'state', 'town']
            mask = pd.Series([False] * len(result_df))
            for col in text_cols:
                if col in result_df.columns:
                    mask = mask | result_df[col].astype(str).str.lower().str.contains(q, na=False)
            result_df = result_df[mask]
        
        # Convert to records
        records = result_df.head(100).to_dict(orient='records')
        
        # Clean NaN
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        return {
            "success": True,
            "developer": "@Fghgddggf",
            "search_term": number or aadhaar or name or q,
            "total": len(records),
            "data": records,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "developer": "@Fghgddggf",
            "message": f"Error: {str(e)}",
            "data": []
        }


@app.get("/stats")
async def stats():
    df = load_data()
    return {
        "total_records": len(df),
        "columns": list(df.columns) if not df.empty else []
    }


# Vercel handler
handler = Mangum(app)
