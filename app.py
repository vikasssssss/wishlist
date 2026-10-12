from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)

def load_cards():
    path = os.path.join(os.path.dirname(__file__), 'cards.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("ОШИБКА: cards.json не найден или поврежден!")
        return []

@app.route('/')
def index():
    cards = load_cards()
    # Для отладки выведем в консоль, сколько карточек загрузилось
    print(f"Загружено карточек: {len(cards)}")
    return render_template('index.html', cards=cards)

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/card/<int:card_id>')
def card_detail(card_id):
    cards = load_cards()
    if card_id >= len(cards):
        abort(404)
    return render_template('card_detail.html', card=cards[card_id])

if __name__ == '__main__':
    app.run(debug=True)