import os
import subprocess
from flask import Flask, request, send_file
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/')
def inicio():
    return "Servidor de Conversión Activo ✅"

@app.route('/convertir', methods=['POST'])
def convertir():
    if 'file' not in request.files:
        return {"error": "No se recibió archivo"}, 400
    
    file = request.files['file']
    file_id = str(uuid.uuid4())
    input_path = f"/tmp/{file_id}.docx"
    file.save(input_path)
    
    try:
        # Comando de Linux para convertir usando LibreOffice
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf', 
            '--outdir', '/tmp', input_path
        ], check=True)
        
        pdf_path = input_path.replace(".docx", ".pdf")
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
