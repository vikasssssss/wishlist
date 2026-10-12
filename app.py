from flask import Flask, render_template, abort, jsonify, request
import json
import os

app = Flask(__name__)


def load_cards():
    path = os.path.join(os.path.dirname(__file__), 'cards.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_gifts():
    path = os.path.join(os.path.dirname(__file__), 'gifts.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Новые функции для bookings.json
def load_bookings():
    path = os.path.join(os.path.dirname(__file__), 'bookings.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_bookings(bookings):
    path = os.path.join(os.path.dirname(__file__), 'bookings.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=4)


@app.route('/')
def index():
    cards = load_cards()
    return render_template('index.html', cards=cards)


@app.route('/wishlist')
def wishlist():
    gifts = load_gifts()
    bookings = load_bookings()  # Загружаем брони
    return render_template('wishlist.html', gifts=gifts, bookings=bookings)


@app.route('/card/<int:card_id>')
def card_detail(card_id):
    cards = load_cards()
    if card_id >= len(cards):
        abort(404)
    return render_template('card_detail.html', card=cards[card_id])


@app.route('/api/reserve/<int:gift_id>', methods=['POST'])
def reserve_gift(gift_id):
    data = request.json
    gifts = load_gifts()
    bookings = load_bookings()
    gift_id_str = str(gift_id)  # В JSON ключи всегда строки

    if gift_id < len(gifts):
        action = data.get('action')
        booker_id = data.get('booker_id')

        if action == 'reserve':
            bookings[gift_id_str] = booker_id
        elif action == 'unreserve':
            # Снять бронь может только тот, кто её оставил
            if bookings.get(gift_id_str) == booker_id:
                del bookings[gift_id_str]
            else:
                return jsonify({'error': 'Unauthorized'}), 403

        save_bookings(bookings)
        return jsonify({'success': True})

    return jsonify({'error': 'Gift not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)