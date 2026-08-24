from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import duckdb
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# DuckDB Connection with HTTPFS
con = duckdb.connect(':memory:')
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Simple Landing Page
LANDING_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hitek Data Gateway</title>
    <style>
        body {
            margin: 0;
            background: #050505;
            color: #00ffcc;
            font-family: 'Courier New', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            text-align: center;
            padding: 50px;
            border: 2px solid #00ffcc;
            border-radius: 15px;
            background: rgba(0, 0, 0, 0.9);
            box-shadow: 0 0 50px rgba(0, 255, 204, 0.2);
        }
        h1 { font-size: 3em; text-shadow: 0 0 20px #00ffcc; }
        .status { color: #00ffcc; font-weight: bold; }
        .blink { animation: blink 1s infinite; }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        .endpoint {
            background: #1a1a1a;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 0.9em;
            color: #888;
        }
        .developer {
            margin-top: 30px;
            color: #00ffcc;
            font-weight: bold;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 SYSTEM ONLINE</h1>
        <p>API Gateway: <span class="status">● Active</span></p>
        <p>Status: <span class="status blink">HTTP 200 OK</span></p>
        <div class="endpoint">
            <strong>📡 ENDPOINT:</strong><br>
            /FetchData?Number=XXXXXXXXXX
        </div>
        <div class="developer">👨‍💻 Developer: @SOCIALBANNERR</div>
    </div>
</body>
</html>
"""

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "status": "rejected",
                "message": "Invalid endpoint. Use /FetchData?Number=XXXXXXXXXX",
                "Developer": "@SOCIALBANNERR"
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "Developer": "@SOCIALBANNERR"}
    )

@app.get("/", response_class=HTMLResponse)
def root_landing_page():
    return HTMLResponse(content=LANDING_PAGE_HTML, status_code=200)

@app.get("/FetchData")
def fetch_data(Number: str = Query(None)):
    # Validation
    if not Number:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Number parameter required",
                "usage": "/FetchData?Number=9876543210",
                "Developer": "@SOCIALBANNERR"
            }
        )
    
    if not Number.isdigit():
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Number must contain only digits",
                "provided": Number,
                "Developer": "@SOCIALBANNERR"
            }
        )
    
    if len(Number) < 10 or len(Number) > 15:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Number must be 10-15 digits",
                "provided": Number,
                "length": len(Number),
                "Developer": "@SOCIALBANNERR"
            }
        )
    
    try:
        last_digit = Number[-1]
        results = []
        
        # ===== PRIMARY SHARD (DuckDB Query) =====
        primary_url = f"https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main/final_master_shard_{last_digit}.parquet"
        
        try:
            # DuckDB query - reads parquet directly from URL
            query = f"""
                SELECT * FROM read_parquet('{primary_url}') 
                WHERE CAST(mobile AS VARCHAR) = '{Number}'
            """
            df = con.execute(query).df()
            if not df.empty:
                results.extend(df.to_dict(orient="records"))
        except Exception as e:
            print(f"Primary query error: {e}")
        
        # ===== ALT SHARD (if not found in primary) =====
        if not results:
            alt_url = f"https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main/alt_master_shard_{last_digit}.parquet"
            
            try:
                query = f"""
                    SELECT * FROM read_parquet('{alt_url}') 
                    WHERE CAST(alt AS VARCHAR) = '{Number}'
                """
                df = con.execute(query).df()
                if not df.empty:
                    results.extend(df.to_dict(orient="records"))
            except Exception as e:
                print(f"Alt query error: {e}")
        
        if not results:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "not_found",
                    "phone": Number,
                    "message": "Number not found in database",
                    "Developer": "@SOCIALBANNERR"
                }
            )
        
        return {
            "status": "success",
            "phone": Number,
            "records_found": len(results),
            "data": results,
            "Developer": "@SOCIALBANNERR"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Processing error: {str(e)}",
                "Developer": "@SOCIALBANNERR"
            }
        )

from mangum import Mangum
handler = Mangum(app)
