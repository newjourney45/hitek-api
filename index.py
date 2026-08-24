from flask import Flask, request, jsonify, render_template_string
import duckdb
import os

app = Flask(__name__)

# DuckDB Setup
con = duckdb.connect()
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Landing Page HTML (Same as before)
LANDING_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hitek Data Gateway - LIVE</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #050505; color: #00ffcc; font-family: 'Courier New', Courier, monospace; }
        #canvas-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; }
        .overlay { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            text-align: center; background: rgba(10, 10, 10, 0.85); padding: 50px; 
            border: 1px solid #00ffcc; border-radius: 12px; box-shadow: 0 0 30px rgba(0, 255, 204, 0.3); 
            backdrop-filter: blur(5px);
        }
        h1 { margin: 0 0 15px 0; font-size: 3.5em; text-transform: uppercase; letter-spacing: 6px; text-shadow: 0 0 15px #00ffcc; }
        p { font-size: 1.2em; margin: 8px 0; color: #ccc; }
        .highlight { color: #00ffcc; font-weight: bold; }
        .status-box { 
            margin-top: 30px; font-weight: bold; padding: 15px; 
            border-radius: 8px; background: rgba(0, 255, 204, 0.1); 
            border: 1px solid rgba(0, 255, 204, 0.5);
            font-size: 1.1em;
        }
        .blinking { animation: blinker 1.5s linear infinite; display: inline-block; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div id="canvas-container"></div>
    <div class="overlay">
        <h1>SYSTEM ONLINE</h1>
        <p>API Gateway is <span class="highlight">Active & Secured</span></p>
        <p>Parquet Cloud Engine: <span class="highlight">Connected</span></p>
        <div class="status-box">
            <span class="blinking" style="color: #00ffcc;">●</span> HTTP 200 OK - LISTENING FOR QUERIES
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        for (let i = 0; i < 8000; i++) {
            vertices.push(THREE.MathUtils.randFloatSpread(3000));
            vertices.push(THREE.MathUtils.randFloatSpread(3000));
            vertices.push(THREE.MathUtils.randFloatSpread(3000));
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        const material = new THREE.PointsMaterial({ color: 0x00ffcc, size: 2.5, transparent: true, opacity: 0.8 });
        const points = new THREE.Points(geometry, material);
        scene.add(points);

        camera.position.z = 1200;

        function animate() {
            requestAnimationFrame(animate);
            points.rotation.x += 0.0005;
            points.rotation.y += 0.001;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

# Custom 404 Error Handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "rejected",
        "message": "Invalid endpoint. STRICTLY use /FetchData?Number=XXXXXXXXXX",
        "Developer": "@rajanhackerd"
    }), 404

# Route: Landing Page
@app.route("/")
def root_landing_page():
    return render_template_string(LANDING_PAGE_HTML)

# Route: Fetch Data
@app.route("/FetchData", methods=['GET'])
def fetch_data():
    number = request.args.get('Number')
    
    # Validation
    if not number or not number.isdigit() or len(number) < 10 or len(number) > 15:
        return jsonify({
            "status": "rejected",
            "message": "Invalid parameter. STRICTLY use /FetchData?Number=XXXXXXXXXX",
            "Developer": "@rajanhackerd"
        }), 400
    
    last_digit = number[-1]
    
    # Updated bucket URL
    base_url = "https://huggingface.co/datasets/CutehackX/hitek-data-bucket/resolve/main"
    primary_url = f"{base_url}/final_master_shard_{last_digit}.parquet"
    alt_url = f"{base_url}/alt_master_shard_{last_digit}.parquet"
    
    try:
        query = f"""
            SELECT *, 'Main' AS _record_type FROM read_parquet('{primary_url}') WHERE mobile = '{number}'
            UNION ALL
            SELECT *, 'Alt' AS _record_type FROM read_parquet('{alt_url}') WHERE alt = '{number}'
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
        
        if not main_records and not alt_records:
            return jsonify({
                "status": "not_found", 
                "phone": number,
                "Developer": "@rajanhackerd"
            }), 404
            
        return jsonify({
            "status": "success", 
            "Data": {
                "Main_Records": main_records,
                "Alt_Records": alt_records
            },
            "Developer": "@rajanhackerd"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Database processing error: {str(e)}",
            "Developer": "@rajanhackerd"
        }), 500

# This is the important part - for Vercel
# Remove the if __name__ == "__main__" block entirely
# Vercel will import 'app' directly
