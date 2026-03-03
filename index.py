import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Vercel'in dosyaları bulabilmesi için yolları bu şekilde sabitliyoruz
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# API Anahtarı (Vercel Settings > Environment Variables kısmına eklenmeli)
api_key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')
        # Özel kimlik ve 'KAR BEKLİYORUZ' kuralı
        prompt = (
            "Sen İstanbulunModu Hava Durumu Sistemi asistanısın. "
            "Tahminlerinde asla 'KAR BEKLENİYOR' deme, mutlaka 'KAR BEKLİYORUZ' ifadesini kullan. "
            "Kullanıcı mesajı: " + user_input
        )
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Bir bağlantı hatası oluştu."}), 500
