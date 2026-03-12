import os
import subprocess
from flask import Flask, request, send_file
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app) # Esto permite que n8n se conecte sin bloqueos

@app.route('/convertir', methods=['POST'])
def convertir():
    # 1. Verificamos si n8n envió un archivo
    if 'file' not in request.files:
        return {"error": "No se recibió ningún archivo"}, 400
    
    file = request.files['file']
    
    # 2. Creamos nombres temporales para que no se mezclen archivos de diferentes usuarios
    file_id = str(uuid.uuid4())
    input_path = f"/tmp/{file_id}.docx"
    
    # 3. Guardamos el Word que envió n8n
    file.save(input_path)
    
    try:
        # 4. Usamos LibreOffice para convertir (es el comando de Linux)
        # Esto es lo que reemplaza a la librería de Windows que usábamos antes
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf', 
            '--outdir', '/tmp', input_path
        ], check=True)
        
        # 5. Preparamos el archivo PDF para enviarlo de vuelta
        pdf_path = input_path.replace(".docx", ".pdf")
        
        return send_file(pdf_path, as_attachment=True)
        
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    # Importante: Render usa el puerto 10000 por defecto o el que él asigne
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)