import requests
import traceback
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hedef API'nin URL'si
API_ENDPOINT = "http://spicaws.assessment.com.tr/links"

@app.route('/links', methods=['POST'])
def convert_and_send():
    try:
        # Gelen JSON verisini al
        data = request.get_json()

        if not data:
            return jsonify({"message": "Eksik JSON verisi"}), 400

        # "X-Auth-Token" değerini al
        auth_token = request.headers.get("X-Auth-Token")

        if not auth_token:
            return jsonify({"message": "Yetkilendirme hatası: Token eksik"}), 401

        # JSON'u multipart/form-data'ya dönüştür (Doğru veri tipleriyle)
        form_data = {
            "firstName": (None, data.get("firstName")),
            "lastName": (None, data.get("lastName")),
            "email": (None, data.get("email")),
            "TCKN": (None, data.get("TCKN")),
            "userID": (None, int(data.get("userID"))),      # ✅ `int` formatına çevrildi
            "folderID": (None, int(data.get("folderID"))),  # ✅ `int` formatına çevrildi
            "productID": (None, int(data.get("productID"))),# ✅ `int` formatına çevrildi
            "language": (None, data.get("language"))
        }

        # Header'ı Hedef API'ye ekleyelim
        headers = {
            "X-Auth-Token": auth_token
        }

        # Log ekleyelim (Gönderilen veriyi görmek için)
        print(f"Bağlanmaya çalışılan URL: {API_ENDPOINT}")
        print(f"Gönderilen Header'lar: {headers}")
        print(f"Gönderilen Form Data: {form_data}")

        # Hedef API'ye `multipart/form-data` isteği gönder
        response = requests.post(API_ENDPOINT, files=form_data, headers=headers, timeout=15, verify=False)

        # Yanıtı döndür
        return jsonify(response.json()), response.status_code

    except requests.exceptions.ConnectionError as conn_err:
        return jsonify({
            "message": "Bağlantı hatası oluştu",
            "error": str(conn_err),
            "traceback": traceback.format_exc()
        }), 500
    except requests.exceptions.Timeout:
        return jsonify({"message": "Hata: API yanıt vermedi!"}), 500
    except Exception as e:
        return jsonify({
            "message": "Hata oluştu",
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    port = 5001  # 5000 yerine 5001 kullanılıyor, ÇAKIŞMA OLMAYACAK!
    print(f"Flask API {port} portunda başlatılıyor...")
    print("Eğer erişim sorunu yaşarsanız, güvenlik duvarı ve port izinlerini kontrol edin.")
    app.run(host="0.0.0.0", port=port)
