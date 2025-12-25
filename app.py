from flask import Flask, render_template, session, request, jsonify, redirect, url_for
import requests
import random

app = Flask(__name__)

# Session (Hafıza) anahtarı
app.secret_key = "pokedex_master_key_ash_ketchum"

TYPE_COLORS = {
    'fire': '#ff4422', 'water': '#3399ff', 'grass': '#77cc55',
    'electric': '#ffcc33', 'psychic': '#ff5599', 'ice': '#66ccff',
    'dragon': '#7766ee', 'dark': '#705848', 'fairy': '#ee99ac',
    'normal': '#aaaa99', 'fighting': '#bb5544', 'flying': '#8899ff',
    'poison': '#aa5599', 'ground': '#ddbb55', 'rock': '#bbaa66',
    'bug': '#aabb22', 'ghost': '#6666bb', 'steel': '#aaaabb'
}

@app.route('/')
def home():
    # Session başlatma
    if 'favoriler' not in session:
        session['favoriler'] = []
        function favoriyeEkle() {
    // Ekranda o an hangi pokemon yazıyorsa onu alıyoruz
    const pokemonAdi = document.querySelector('h2').innerText; 
    const pokemonResmi = document.querySelector('.pokemon-img').src;

    let favoriler = JSON.parse(localStorage.getItem('favoriPokemonlar')) || [];

    // Eğer zaten ekli değilse ekle
    const kontrol = favoriler.find(p => p.ad === pokemonAdi);
    
    if (!kontrol) {
        favoriler.push({ ad: pokemonAdi, resim: pokemonResmi });
        localStorage.setItem('favoriPokemonlar', JSON.stringify(favoriler));
        alert(pokemonAdi + " favorilerine eklendi!");
    } else {
        alert("Bu Pokemon zaten listende!");
    }
}

    # Rastgele Pokemon seç
    poke_id = random.randint(1, 898)
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    
    try:
        response = requests.get(url)
        data = response.json()
        tur_ingilizce = data['types'][0]['type']['name']
        
        pokemon = {
            'isim': data['name'].upper(),
            'resim': data['sprites']['other']['official-artwork']['front_default'],
            'tur': tur_ingilizce.upper(),
            'boy': data['height'] / 10,
            'kilo': data['weight'] / 10,
            'renk': TYPE_COLORS.get(tur_ingilizce, '#aaaa99')
        }

        return render_template('index.html', pokemon=pokemon, favoriler=session['favoriler'])
    except Exception as e:
        return f"Hata: {e}"

# --- FAVORİ EKLEME (Fetch API ile uyumlu) ---
@app.route('/favori-ekle', methods=['POST'])
def favori_ekle():
    data = request.get_json() # JavaScript'ten gelen JSON verisini al
    mevcut_favoriler = session.get('favoriler', [])

    # Aynı Pokemon'un listede olup olmadığını kontrol et
    if not any(p['isim'] == data['isim'] for p in mevcut_favoriler):
        mevcut_favoriler.insert(0, data) # En başa ekle
        session['favoriler'] = mevcut_favoriler
        session.modified = True # Flask'a session'ın değiştiğini haber ver
    
    # Güncel listeyi JSON olarak döndür (Sayfa yenilenmesini engeller)
    return jsonify(session['favoriler'])

# --- TEMİZLEME ---
@app.route('/temizle')
def temizle():
    session['favoriler'] = []
    # Eğer fetch ile çağırıyorsan jsonify, butonla çağırıyorsan redirect yapmalısın
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.path == '/temizle':
        return redirect(url_for('home'))
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
