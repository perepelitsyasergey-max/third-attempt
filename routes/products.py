from flask import Blueprint, request, jsonify
from extensions import db
from models import Product

products_bp = Blueprint('products', __name__)


# 4.1. Створення нового товару (API)
@products_bp.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Валідація
    if not data or not data.get('product-name'):
        return jsonify({'error': "Назва товару є обов'язковою"}), 400
    
    # Очищення та нормалізація ціни
    raw_price = data.get('product-price')
    price_value = 0.0
    
    if raw_price is not None and str(raw_price).strip() != '':
        try:
            # Видаляємо звичайні пробіли, нерозривні пробіли (\xa0) та замінюємо кому на крапку
            cleaned_price = str(raw_price).replace('\xa0', '').replace(' ', '').replace(',', '.')
            price_value = float(cleaned_price)
        except ValueError:
            return jsonify({'error': "Неприпустимий формат ціни"}), 400
    
    # Створення об'єкта та збереження в БД
    new_product = Product(
        product_name_db=data.get('product-name'),
        product_price_db=data.get('product-price', 0)
    )

    db.session.add(new_product)
    db.session.commit()

    return (
        jsonify({'message': 'Товар успішно збережено!'}), 201,
    )
# ------------------------------------------------------------------------------------------

# 4.2. Отримання списку всіх товарів (API)
@products_bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_list = []

    for i in products:
        products_list.append({
            'id': i.id,
            'product_name': i.product_name_db,
            'product_price': i.product_price_db
        })

    return jsonify(products_list), 200
#--------------------------------------------------------------------------------------------

# 4.3. Отримання даних одного товару за ID (API)
@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'product_name': product.product_name_db,
        'product_price': str(product.product_price_db)
    }), 200
# -----------------------------------------------------------------------------------------------

# 4.4. Оновлення даних існуючого товару (API)
@products_bp.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    if not data or not data.get('product-name'):
        return jsonify({'error': "Назва товару є обов'язковою"}), 400

    # Оновлюємо поля в базі даних
    product.product_name_db = data.get('product-name')
    product.product_price_db = data.get('product-price', 0)

    db.session.commit()

    return jsonify({'message': 'Товар успішно оновлено'}), 200
# -----------------------------------------------------------------------------------------------

# 4.5. Видалення товару за ID
@products_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Товар не знайдено'}), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Товар успішно видалено'}), 200
# ------------------------------------------------------------------------------------------------