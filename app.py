from flask import Flask, render_template, session, request, jsonify, redirect, url_for
import requests
import random

app = Flask(__name__)
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
        return render_template('index.html', pokemon=pokemon)
    except Exception as e:
        return f"Hata: {e}"

# Favoriler Sayfası Rotası
@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
