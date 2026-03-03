import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Dosyaların klasörsüz (ana dizinde) çalışması için ayar
app = Flask(__name__, template_folder='.', static_folder='.')

api_key = os.environ.get('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')
        # İstanbulunModu kuralları
        instruction = "Sen İstanbulunModu Hava Durumu Sistemi asistanısın. Tahminlerinde 'KAR BEKLİYORUZ' demelisin."
        response = model.generate_content(f"{instruction}\nSoru: {user_input}")
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"HATA: {e}")
        return jsonify({"reply": "API anahtarı hatası veya bağlantı sorunu."}), 500
