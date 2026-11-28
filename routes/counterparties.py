from flask import Blueprint, request, jsonify
from extensions import db
from models import Counterparty

counterparties_bp = Blueprint('counterparties', __name__)

# 5.1. Створення нового Контрагента (API)
@counterparties_bp.route('/api/counterparties', methods = ['POST'])
def create_counterparty():
    data = request.get_json()

    if not data or not data.get('counterparty-name'):
        return jsonify({'error': "Назва контрагента є обов'язкова"}), 400

    # Отримуємо та очищаємо поля від зайвих пробілів
    edrpou = (data.get('counterparty-edrpou') or '').strip()
    ipn = (data.get('counterparty-ipn') or '').strip()

    # Перевірка на дублікат за ЄДРПОУ (якщо поле заповнене)
    if edrpou:
        existing_edrpou = Counterparty.query.filter_by(counterparty_edrpou_db=edrpou).first()
        if existing_edrpou:
            return jsonify({'error': f'Контрагент із таким ЄДРПОУ вже існує (Назва: {existing_edrpou.counterparty_name_db})'}), 400

    # Перевірка на дублікат за ІПН (якщо поле заповнене)
    if ipn:
        existing_ipn = Counterparty.query.filter_by(counterparty_ipn_db=ipn).first()
        if existing_ipn:
            return jsonify({'error': f'Контрагент із таким ІПН вже існує (Назва: {existing_ipn.counterparty_name_db})'}), 400


    # Створення об'єкта та збереження в БД
    new_counterparty = Counterparty (
        counterparty_name_db = data.get('counterparty-name'),
        counterparty_edrpou_db = data.get('counterparty-edrpou'),
        counterparty_ipn_db = data.get('counterparty-ipn'),
        counterparty_contacts_db = data.get('counterparty-contacts'),
        counterparty_adress_db = data.get('counterparty-adress')
    )

    db.session.add(new_counterparty)
    db.session.commit()

    return (
        jsonify({'message': 'Контрагент успішно збережений!'}), 201
        )
# -----------------------------------------------------------------------------------------


# 5.2. Отримання списку всіх Контрагентів (API)
@counterparties_bp.route('/api/counterparties', methods = ['GET'])
def get_counterparties ():
    counterparties = Counterparty.query.all()
    counterparties_list = []

    for i in counterparties:
        counterparties_list.append({
            'id': i.id,
            'counterparty_name': i.counterparty_name_db,
            'counterparty_edrpou': i.counterparty_edrpou_db,
            'counterparty_ipn': i.counterparty_ipn_db,
            'counterparty_contacts': i.counterparty_contacts_db,
            'counterparty_adress': i.counterparty_adress_db
        })
    return jsonify(counterparties_list), 200
# --------------------------------------------------------------------------------------

# 5.3. Отримання даних одного контрагента за ID (API)
@counterparties_bp.route('/api/counterparties/<int:counterparty_id>', methods=['GET'])
def get_counterparty(counterparty_id):
    counterparty = Counterparty.query.get(counterparty_id)
    if not counterparty:
        return jsonify({'error': 'Контрагента не знайдено'}), 404

    return jsonify({
        'id': counterparty.id,
        'name': counterparty.counterparty_name_db,
        'edrpou': counterparty.counterparty_edrpou_db,
        'ipn': counterparty.counterparty_ipn_db,
        'contacts': counterparty.counterparty_contacts_db,
        'adress': counterparty.counterparty_adress_db
    }), 200
# ------------------------------------------------------------------------------------------

# 5.4. Оновлення даних існуючого контрагента (API)
@counterparties_bp.route('/api/counterparties/<int:counterparty_id>', methods=['PUT'])
def update_counterparty(counterparty_id):
    counterparty = Counterparty.query.get(counterparty_id)
    if not counterparty:
        return jsonify({'error': 'Контрагента не знайдено'}), 404

    data = request.get_json()

    if not data or not data.get('counterparty-name'):
        return jsonify({'error': "Назва контрагента є обов'язковою"}), 400

    # Оновлюємо поля в базі даних (назви ключів з форми HTML)
    counterparty.counterparty_name_db = data.get('counterparty-name')
    counterparty.counterparty_edrpou_db = data.get('counterparty-edrpou')
    counterparty.counterparty_ipn_db = data.get('counterparty-ipn')
    counterparty.counterparty_contacts_db = data.get('counterparty-contacts')
    counterparty.counterparty_adress_db = data.get('counterparty-adress')

    db.session.commit()

    return jsonify({'message': 'Контрагента успішно оновлено'}), 200
# ------------------------------------------------------------------------------------

# 5.5. Видалення Контрагента за ID
@counterparties_bp.route('/api/counterparties/<int:counterparty_id>', methods = ['DELETE'])
def delete_counterparty(counterparty_id):
    counterparty = Counterparty.query.get(counterparty_id)

    if not counterparty:
        return jsonify ({'error': 'Контрагента не знайдено'}), 404

    
    db.session.delete(counterparty)
    db.session.commit()

    return jsonify ({'message': 'Контрагент успішно видалений'}), 200
# -----------------------------------------------------------------------------------------
