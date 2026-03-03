import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Klasör aramayı iptal edip her şeyi bulunduğu yerde (root) aramasını söylüyoruz
app = Flask(__name__, template_folder='.', static_folder='.')

api_key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    # Artık templates klasörü aramıyor, direkt yanındaki index.html'i açıyor
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')
        # İstanbulunModu Hava Durumu Sistemi kimliği ve özel 'KAR BEKLİYORUZ' kuralı
        instruction = "Sen İstanbulunModu Hava Durumu Sistemi asistanısın. Kar tahminlerinde mutlaka 'KAR BEKLİYORUZ' demelisin."
        response = model.generate_content(f"{instruction}\nKullanıcı: {user_input}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Bağlantı hatası oluştu."}), 500
    
