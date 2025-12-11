from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

@app.route('/')
def home():
    # 1. Nesil (Orijinal) pokemonlardan rastgele birini seç (1-151 arası)
    poke_id = random.randint(1, 151)
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    
    try:
        # User-Agent ekliyoruz ki tarayıcı gibi görünsün
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verileri ayıklama
            isim = data['name'].upper()
            resim = data['sprites']['other']['official-artwork']['front_default']
            tur = data['types'][0]['type']['name'].upper()
            boy = data['height'] / 10 # Metreye çevir
            kilo = data['weight'] / 10 # Kg'ye çevir
            
            # Türe göre renk ayarı
            renk = "#333"
            if "fire" in tur.lower(): renk = "#ff4422"
            elif "grass" in tur.lower(): renk = "#77cc55"
            elif "water" in tur.lower(): renk = "#3399ff"
            elif "electric" in tur.lower(): renk = "#ffcc33"
            
            return render_template('index.html', 
                                   isim=isim, 
                                   resim=resim, 
                                   tur=tur, 
                                   boy=boy, 
                                   kilo=kilo,
                                   renk=renk)
        else:
            return "API Hatası: Pokémon bulunamadı."
            
    except Exception as e:
        return f"Bağlantı Hatası: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
