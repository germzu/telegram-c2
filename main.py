from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import base64
from datetime import datetime

# Инициализация приложения
app = Flask(__name__)
CORS(app)  # Разрешаем запросы из любого домена (включая web.telegram.org/k)

@app.route('/collect', methods=['POST'])
def collect():
    try:
        raw_data = request.get_data()
        
        # Попытка декодирования Base64, если данные пришли в таком виде
        decoded_str = ''
        if b'=' in raw_data or len(raw_data) % 4 != 0:
            decoded_str = base64.b64decode(raw_data).decode('utf-8')
        else:
            decoded_str = raw_data.decode('utf-8')
        
        # Парсинг JSON из строки
        data = json.loads(decoded_str) if decoded_str else {}
        
        # Логирование в консоль (для удобства просмотра в Replit)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Received from /collect:")
        print(json.dumps(data, indent=2))
        
        return jsonify({"status": "success", "message": "Data received"}), 200
        
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Error processing request:")
        print(str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Запуск сервера на порту 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
