from flask import Flask, render_template, session, request, redirect, url_for
import requests
import random

app = Flask(__name__)

# Session (Hafıza) anahtarı
app.secret_key = "pokedex_master_key_ash_ketchum"

# Pokemon Türlerine Göre Renk Paleti (Neon Renkler)
TYPE_COLORS = {
    'fire': '#ff4422',      # Kırmızı
    'water': '#3399ff',     # Mavi
    'grass': '#77cc55',     # Yeşil
    'electric': '#ffcc33',  # Sarı
    'psychic': '#ff5599',   # Pembe
    'ice': '#66ccff',       # Buz Mavisi
    'dragon': '#7766ee',    # Mor
    'dark': '#705848',      # Koyu Kahve
    'fairy': '#ee99ac',     # Açık Pembe
    'normal': '#aaaa99',    # Gri
    'fighting': '#bb5544',  # Kiremit
    'flying': '#8899ff',    # Gök Mavisi
    'poison': '#aa5599',    # Mor
    'ground': '#ddbb55',    # Toprak
    'rock': '#bbaa66',      # Kaya
    'bug': '#aabb22',       # Böcek Yeşili
    'ghost': '#6666bb',     # Hayalet Moru
    'steel': '#aaaabb'      # Çelik Grisi
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'favoriler' not in session:
        session['favoriler'] = []

    # Rastgele Pokemon (1. Nesil ile 8. Nesil arası)
    poke_id = random.randint(1, 898)
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Verileri Ayıkla
            tur_ingilizce = data['types'][0]['type']['name']
            # Rengi sözlükten bul, yoksa gri yap
            renk = TYPE_COLORS.get(tur_ingilizce, '#aaaa99')
            
            pokemon = {
                'isim': data['name'].upper(),
                'resim': data['sprites']['other']['official-artwork']['front_default'],
                'tur': tur_ingilizce.upper(),
                'boy': data['height'] / 10, # Metreye çevir
                'kilo': data['weight'] / 10, # Kg'ye çevir
                'renk': renk
            }

            return render_template('index.html', 
                                   pokemon=pokemon, 
                                   favoriler=session['favoriler'])
        else:
            return "API Hatası"
    except Exception as e:
        return f"Hata: {e}"

# --- FAVORİ EKLEME ---
@app.route('/favori-ekle', methods=['POST'])
def favori_ekle():
    yeni_fav = {
        'isim': request.form['isim'],
        'resim': request.form['resim'],
        'tur': request.form['tur'],
        'renk': request.form['renk']
    }
    
    mevcut = session.get('favoriler', [])
    
    # Aynı Pokemon'u tekrar ekleme kontrolü
    zaten_var = False
    for p in mevcut:
        if p['isim'] == yeni_fav['isim']:
            zaten_var = True
            break
            
    if not zaten_var:
        mevcut.insert(0, yeni_fav)
        session['favoriler'] = mevcut
        
    return redirect(url_for('home'))

# --- TEMİZLEME ---
@app.route('/temizle')
def temizle():
    session['favoriler'] = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)

# STATE: Uygulama çalıştığı sürece favorileri burada tutar
poke_bank = []

def get_random_pokemon():
    poke_id = random.randint(1, 898)
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}").json()
    
    # Tasarımın için renk eşleştirme
    type_colors = {
        'fire': '#ff4444', 'water': '#44aaff', 'grass': '#44ff44', 
        'electric': '#ffff44', 'psychic': '#ff44aa', 'ice': '#aaffff',
        'dragon': '#7744ff', 'ghost': '#9944ff', 'normal': '#aaaaaa'
    }
    main_type = res['types'][0]['type']['name']
    
    return {
        "isim": res['name'].upper(),
        "resim": res['sprites']['other']['official-artwork']['front_default'],
        "tur": main_type.upper(),
        "boy": res['height'] / 10,
        "kilo": res['weight'] / 10,
        "renk": type_colors.get(main_type, '#00ffcc')
    }

@app.route('/')
def index():
    pokemon = get_random_pokemon()
    return render_template('index.html', pokemon=pokemon, favoriler=poke_bank)

@app.route('/kaydet', methods=['POST'])
def kaydet():
    data = request.json
    # Eğer listede yoksa ekle (State kontrolü)
    if not any(p['isim'] == data['isim'] for p in poke_bank):
        poke_bank.append(data)
    return jsonify(poke_bank) # Güncel listeyi geri döndür

@app.route('/temizle')
def temizle():
    global poke_bank
    poke_bank = []
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
