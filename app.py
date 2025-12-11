from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

# REST Countries API (Anahtarsız/Public)
API_URL = "https://restcountries.com/v3.1/all"

@app.route('/')
def home():
    try:
        # 1. Tüm ülkeleri çekiyoruz
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            ulkeler = response.json()
            
            # 2. Listeden rastgele bir ülke seç
            ulke = random.choice(ulkeler)
            
            # 3. Verileri ayıklayalım (Bazen başkent boş olabilir, önlem alıyoruz)
            ad = ulke['name']['common']
            resmi_ad = ulke['name']['official']
            
            baskent = "Yok"
            if 'capital' in ulke:
                baskent = ulke['capital'][0]
                
            kita = ulke['region']
            nufus = "{:,}".format(ulke['population']) # Sayıyı virgülle ayırır (Örn: 80,000,000)
            bayrak = ulke['flags']['svg']
            harita_link = ulke['maps']['googleMaps']
            
            return render_template('index.html', 
                                   ad=ad,
                                   resmi_ad=resmi_ad,
                                   baskent=baskent,
                                   kita=kita,
                                   nufus=nufus,
                                   bayrak=bayrak,
                                   harita=harita_link)
        else:
            return "API Veri Hatası"
    except Exception as e:
        return f"Bir hata oluştu: {e}"

if __name__ == '__main__':
    # Docker için host 0.0.0.0 şart
    app.run(debug=True, host='0.0.0.0', port=5000)
