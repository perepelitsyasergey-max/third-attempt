# =================================================================================================
#    1  Налаштування
# =================================================================================================

from flask import Flask, render_template, request, jsonify, session, redirect
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


# Завантажуємо змінні з файла .env
load_dotenv()

app = Flask(__name__)

# Отримуємо значення з .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =================================================================================================
#    2  Класи
# =================================================================================================

# 2.1. Користувачі
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name_db = db.Column(db.String(80), unique=True, nullable=False)
    user_password_db = db.Column(db.String(256), nullable=False)


# 2.2.  Товари
class Product (db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name_db = db.Column(db.String(255), nullable=False)
    product_price_db = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

class Counterparty (db.Model):
    __tablename__ = 'counterparty'

    id = db.Column(db.Integer, primary_key=True)
    counterparty_name_db = db.Column(db.String(255), nullable=True)
    counterparty_edrpou_db = db.Column(db.String, nullable=True)
    counterparty_ipn_db = db.Column(db.String, nullable=False)
    counterparty_contacts_db = db.Column(db.String(1000), nullable=False)
    counterparty_adress_db = db.Column(db.String(1000), nullable=False)


class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    reg_number_contract_db = db.Column(db.String(255), nullable=True)
    agreement_number_db = db.Column(db.String(255), nullable=True)
    contract_number_db = db.Column(db.String(255), nullable=True)
    counterparty_1_db = db.Column(db.String(255), nullable=True)
    counterparty_2_db = db.Column(db.String(255), nullable=True)
    contract_date_db = db.Column(db.String(50), nullable=True)
    end_date_db = db.Column(db.String(50), nullable=True)
    auto_prolongation_db = db.Column(db.Boolean, default=False)
    archival_contracts_db = db.Column(db.Boolean, default=False)
    user_db = db.Column(db.String(80), nullable=True)
    contract_type_db = db.Column(db.String(100), nullable=True)
    contract_stage_db = db.Column(db.String(100), nullable=True)
    funds_type_db = db.Column(db.String(100), nullable=True)
    contract_notes_db = db.Column(db.Text, nullable=True)

class Specification(db.Model):
    __tablename__ = 'specifications'

    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор специфікації
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)  # Зовнішній ключ для зв'язку з конкретним договором
    spec_number_db = db.Column(db.String(100), nullable=True) # Номер специфікації
    spec_currency_db = db.Column(db.String(10), nullable=True)  # Валюта специфікації (UAH, USD, EUR)
    spec_currency_rate_db = db.Column(db.Numeric(10, 4), nullable=True)  # Курс валюти
    spec_total_amount_db = db.Column(db.Numeric(12, 2), nullable=True)  # Загальна сума специфікації в грн

# 2.4. Позиції (товари) у специфікації
class SpecificationItem(db.Model):
    __tablename__ = 'specification_items'

    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор рядка товару
    specification_id = db.Column(db.Integer, db.ForeignKey('specifications.id'), nullable=False)  # Зв'язок із батьківською специфікацією
    product_name_db = db.Column(db.String(255), nullable=False)  # Назва товару
    product_qty_db = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  # Кількість товару
    product_price_db = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  # Ціна за одиницю
    product_vat_db = db.Column(db.String(50), nullable=True)  # Ставка ПДВ (з ПДВ / без ПДВ)


# 2.5. Записи оплат та відвантажень для кожного рядка товару
class PaymentShippingRecord(db.Model):
    __tablename__ = 'payment_shipping_records'

    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор запису
    item_id = db.Column(db.Integer, db.ForeignKey('specification_items.id'), nullable=False)  # Зв'язок із конкретним рядком товару у специфікації
    pay_date_db = db.Column(db.String(50), nullable=True)  # Дата оплати
    pay_sum_db = db.Column(db.Numeric(12, 2), nullable=True, default=0.00)  # Сума оплати
    ship_date_db = db.Column(db.String(50), nullable=True)  # Дата поставки (відвантаження)
    ship_sum_db = db.Column(db.Numeric(12, 2), nullable=True, default=0.00)  # Сума поставки



# =================================================================================================
#    3  Маршрути Авторизація
# =================================================================================================

# 3.1. Основна адреса
@app.route('/')
def login():
    return render_template('login.html')
# ---------------------------------------------------------------------------------------------

# 3.2. Авторизація користувача (API)
@app.route('/api/login', methods=['POST'])
def login_page():
        data = request.get_json()

        user_name = data.get('userName')
        user_password = data.get('userPassword')

        if not user_name or not user_password:
            return jsonify({'success': False, 'message': 'Логін та пароль обов’язкові'}), 400

        found_user = User.query.filter_by(user_name_db=user_name).first()

        if found_user and found_user.user_password_db == user_password:
            session['user_in_session'] = found_user.user_name_db
            return jsonify({'success': True, 'message': 'Успішний вхід!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Невірний логін або пароль!'}), 401
# ---------------------------------------------------------------------------------------------

# 3.3. Вихід із системи
@app.route('/logout')
def logout():
     session.pop('user_in_session', None)
     return redirect('/')
# ---------------------------------------------------------------------------------------------

# 3.4. Головна панель управління (HTML)
@app.route('/dashboard')
def dashboard():
     get_user_name = session.get('user_in_session')
     return render_template('dashboard.html', user_name_with_session = get_user_name )
# ---------------------------------------------------------------------------------------------


# =================================================================================================
#    4  Маршрути вкладка Товари
# =================================================================================================

# 4.1. Створення нового товару (API)
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Валідація
    if not data or not data.get('product-name'):
        return jsonify({'error': "Назва товару є обов'язковою"}), 400

    # Створення об'єкта та збереження в БД
    new_product = Product(
        product_name_db=data.get('product-name'),
        product_price_db=data.get('product-price', 0)
    )

    db.session.add(new_product)
    db.session.commit()

    return (
        jsonify({'message': 'Товар успішно збережено в БД'}), 201,
    )
# ------------------------------------------------------------------------------------------

# 4.2. Отримання списку всіх товарів (API)
@app.route('/api/products', methods=['GET'])
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
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'product_name': product.product_name_db,
        'product_price': str(product.product_price_db)
    }), 200
# -----------------------------------------------------------------------------------------------

# 4.4. Оновлення даних існуючого товару (API)
@app.route('/api/products/<int:product_id>', methods=['PUT'])
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
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Товар не знайдено'}), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Товар успішно видалено'}), 200
# ------------------------------------------------------------------------------------------------


# =================================================================================================
#    5  Маршрути вкладка Контрагенти
# =================================================================================================


# 5.1. Створення нового Контрагента (API)
@app.route('/api/counterparties', methods = ['POST'])
def create_counterparty():
    data = request.get_json()

    if not data or not data.get('counterparty-name'):
        return jsonify({'error': "Назва контрагента є обов'язкова"}), 400


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
@app.route('/api/counterparties', methods = ['GET'])
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
@app.route('/api/counterparties/<int:counterparty_id>', methods=['GET'])
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
@app.route('/api/counterparties/<int:counterparty_id>', methods=['PUT'])
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
@app.route('/api/counterparties/<int:counterparty_id>', methods = ['DELETE'])
def delete_counterparty(counterparty_id):
    counterparty = Counterparty.query.get(counterparty_id)

    if not counterparty:
        return jsonify ({'error': 'Контрагента не знайдено'}), 404

    
    db.session.delete(counterparty)
    db.session.commit()

    return jsonify ({'message': 'Контрагент успішно видалений'}), 200
# -----------------------------------------------------------------------------------------


# =================================================================================================
#    6  Маршрути вкладка Договори
# =================================================================================================


# 6.1. Створення нового Договору (API)
@app.route('/api/contracts', methods = ['POST'])
def create_contract():
    data = request.get_json()

    if not data:
        return jsonify({'error': "Дані відсутні"}), 400

    # Створення об'єкта та збереження в БД
    new_contract = Contract (
        reg_number_contract_db=data.get('reg-number-contract'),
        agreement_number_db=data.get('agreement-number'),
        contract_number_db=data.get('contract-number'),
        counterparty_1_db=data.get('counterparty-1'),
        counterparty_2_db=data.get('counterparty-2'),
        contract_date_db=data.get('contract-date'),
        end_date_db=data.get('end-date'),
        auto_prolongation_db=True if data.get('auto-prolongation') else False,
        is_archived_db=True if data.get('archival-contracts') else False,
        user_db=session.get('user_in_session'),
        contract_type_db=data.get('contract-type'),
        contract_stage_db=data.get('contract-stage'),
        funds_type_db=data.get('funds-type'),
        contract_notes_db=data.get('contract-notes')
    )

    db.session.add(new_contract)
    db.session.commit()

    return jsonify({
        'message': 'Договір успішно збережено!',
        'id': new_contract.id  # <--- Передаємо згенерований ID договору
    }), 201
# ------------------------------------------------------------------------------------------------------

# Отримання списку всіх договорів (API)
@app.route('/api/contracts', methods=['GET'])
def get_contracts():
    contracts = Contract.query.all()
    contracts_list = []

    for i in contracts:
        # ЗАХИСНИЙ МЕХАНІЗМ: якщо номер відсутній у базі (старі записи), формуємо його на льоту за ID
        reg_number_with_value = i.reg_number_contract_db
        if not reg_number_with_value:
            reg_number_with_value = f"БР-{i.id}/26"
        contracts_list.append({
            'id': i.id,
            'reg_number': reg_number_with_value,
            'agreement_number': i.agreement_number_db,
            'contract_number': i.contract_number_db,
            'counterparty_1': i.counterparty_1_db,
            'counterparty_2': i.counterparty_2_db,
            'contract_date': i.contract_date_db,
            'end_date': i.end_date_db,
            'end_date': i.end_date_db,
            'contract_stage': i.contract_stage_db,
            'user': i.user_db,
            'is_archived': i.archival_contracts_db
        })

    return jsonify(contracts_list), 200
# --------------------------------------------------------------------------------------------------------

# Отримання даних одного договору за ID (API)
@app.route('/api/contracts/<int:contract_id>', methods=['GET'])
def get_contract(contract_id):
    contract = Contract.query.get_or_404(contract_id)

    reg_number_with_value = contract.reg_number_contract_db
    if not reg_number_with_value:
        reg_number_with_value = f"БР-{contract.id}/26"

    return jsonify({
        'id': contract.id,
        'reg_number': reg_number_with_value,
        'agreement_number': contract.agreement_number_db,
        'contract_number': contract.contract_number_db,
        'counterparty_1': contract.counterparty_1_db,
        'counterparty_2': contract.counterparty_2_db,
        'contract_date': contract.contract_date_db,
        'end_date': contract.end_date_db,
        'auto_prolongation': contract.auto_prolongation_db,
        'archival-contracts': contract.archival_contracts_db,
        'user': contract.user_db,
        'contract_type': contract.contract_type_db,
        'contract_stage': contract.contract_stage_db,
        'funds_type': contract.funds_type_db,
        'contract_notes': contract.contract_notes_db
    }), 200
# ------------------------------------------------------------------------------------------------------

# Створення специфікації для конкретного договору (API)
@app.route('/api/contracts/<int:contract_id>/specifications', methods=['POST'])
def create_specification(contract_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': "Дані відсутні"}), 400

    # Перевіряємо, чи існує такий договір у базі
    contract = Contract.query.get_or_404(contract_id)

    # 1. Створюємо та зберігаємо головну специфікацію
    new_spec = Specification(
        contract_id=contract.id,
        spec_number_db=data.get('spec-number'),
        spec_currency_db=data.get('spec-currency'),
        spec_currency_rate_db=data.get('spec-currency-rate') or 1.0000,
        spec_total_amount_db=data.get('spec-total-amount-in-uah') or 0.00
    )
    db.session.add(new_spec)
    db.session.flush()  # Отримуємо ID новоствореної специфікації до коміту

    # 2. Зберігаємо товари (рядки) специфікації
    items_data = data.get('items', [])
    for item in items_data:
        new_item = SpecificationItem(
            specification_id=new_spec.id,
            product_name_db=item.get('productName'),
            product_qty_db=item.get('productQty') or 0,
            product_price_db=item.get('productPrice') or 0,
            product_vat_db=item.get('productVat')
        )
        db.session.add(new_item)
        db.session.flush()  # Отримуємо ID рядка товару

        # 3. Зберігаємо оплати та відвантаження для цього рядка товару
        records_data = item.get('payShipRecords', [])
        for rec in records_data:
            new_record = PaymentShippingRecord(
                item_id=new_item.id,
                pay_date_db=rec.get('payDate'),
                pay_sum_db=rec.get('paySum') or 0,
                ship_date_db=rec.get('shipDate'),
                ship_sum_db=rec.get('shipSum') or 0
            )
            db.session.add(new_record)

    db.session.commit()

    return jsonify({'message': 'Специфікацію успішно збережено в БД!'}), 201
# -----------------------------------------------------------------------------------------------------

# 6.5. Оновлення даних існуючого Договору (API)
@app.route('/api/contracts/<int:contract_id>', methods=['PUT'])
def update_contract(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': "Дані відсутні"}), 400

    # Оновлюємо поля договору в базі даних
    contract.reg_number_contract_db = data.get('reg-number-contract')
    contract.agreement_number_db = data.get('agreement-number')
    contract.contract_number_db = data.get('contract-number')
    contract.counterparty_1_db = data.get('counterparty-1')
    contract.counterparty_2_db = data.get('counterparty-2')
    contract.contract_date_db = data.get('contract-date')
    contract.end_date_db = data.get('end-date')
    contract.auto_prolongation_db = True if data.get('auto-prolongation') else False
    contract.archival_contracts_db = True if data.get('archival-contracts') else False
    contract.contract_type_db = data.get('contract-type')
    contract.contract_stage_db = data.get('contract-stage')
    contract.funds_type_db = data.get('funds-type')
    contract.contract_notes_db = data.get('contract-notes')

    db.session.commit()

    return jsonify({'message': 'Договір успішно оновлено!'}), 200
# ----------------------------------------------------------------------------------------------------------

# 6.6. Видалення Договору за ID (API)
@app.route('/api/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    contract = Contract.query.get(contract_id)

    if not contract:
        return jsonify({'error': 'Договір не знайдено'}), 404

    db.session.delete(contract)
    db.session.commit()

    return jsonify({'message': 'Договір успішно видалено'}), 200
# -----------------------------------------------------------------------------------------------------------

# Отримання списку специфікацій для конкретного договору (API)
@app.route('/api/contracts/<int:contract_id>/specifications', methods=['GET'])
def get_contract_specifications(contract_id):
    specs = Specification.query.filter_by(contract_id=contract_id).order_by(Specification.spec_number_db).all()
    specs_list = []

    for spec in specs:
        items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
        items_data = []
        
        spec_total_paid = 0
        spec_total_shipped = 0

        for item in items:
            # Рахуємо оплати та відвантаження для цього рядка
            records = PaymentShippingRecord.query.filter_by(item_id=item.id).all()
            item_paid = sum(float(r.pay_sum_db or 0) for r in records)
            item_shipped = sum(float(r.ship_sum_db or 0) for r in records)
            
            spec_total_paid += item_paid
            spec_total_shipped += item_shipped

            items_data.append({                
                'product_name': item.product_name_db,
                'qty': float(item.product_qty_db or 0),
                'price': float(item.product_price_db or 0),
                'cost': float(item.product_qty_db or 0) * float(item.product_price_db or 0),
                'paid': item_paid,
                'shipped': item_shipped
            })

        # Рахуємо загальну вартість у валюті специфікації (без урахування курсу)
        spec_currency_total = sum(float(item.product_qty_db or 0) * float(item.product_price_db or 0) for item in items)

        specs_list.append({
            'id': spec.id,
            'spec_number': spec.spec_number_db or '',
            'currency': spec.spec_currency_db,
            'currency_total': spec_currency_total,  # <--- Додаємо це поле (Загальна вартість у валюті)
            'total_amount': float(spec.spec_total_amount_db or 0), # Це залишається для гривень (з курсом)
            'total_paid': spec_total_paid,
            'total_shipped': spec_total_shipped,
            'items': items_data
        })

    return jsonify(specs_list), 200
# -------------------------------------------------------------------------------------------------------

# Видалення специфікації за ID (API)
@app.route('/api/specifications/<int:spec_id>', methods=['DELETE'])
def delete_specification(spec_id):
    spec = Specification.query.get(spec_id)
    if not spec:
        return jsonify({'error': 'Специфікацію не знайдено'}), 404
    
    # Видаляємо пов'язані записи оплат/відвантажень та позиції
    items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
    for item in items:
        PaymentShippingRecord.query.filter_by(item_id=item.id).delete()
    
    SpecificationItem.query.filter_by(specification_id=spec.id).delete()
    db.session.delete(spec)
    db.session.commit()
    
    return jsonify({'message': 'Специфікацію успішно видалено'}), 200
# -----------------------------------------------------------------------------------------------------------

# Отримання даних однієї специфікації для редагування (API)
@app.route('/api/specifications/<int:spec_id>', methods=['GET'])
def get_specification(spec_id):
    spec = Specification.query.get_or_404(spec_id)
    items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
    
    items_data = []
    for item in items:
        records = PaymentShippingRecord.query.filter_by(item_id=item.id).all()
        records_data = []
        for r in records:
            records_data.append({
                'payDate': r.pay_date_db,
                'paySum': float(r.pay_sum_db or 0),
                'shipDate': r.ship_date_db,
                'shipSum': float(r.ship_sum_db or 0)
            })
            
        items_data.append({
            'specNumber': spec.spec_number_db or '',
            'productName': item.product_name_db,
            'productQty': float(item.product_qty_db or 0),
            'productPrice': float(item.product_price_db or 0),
            'productVat': item.product_vat_db,
            'payShipRecords': records_data
        })

    return jsonify({
        'id': spec.id,
        'spec_number': spec.spec_number_db or '',
        'currency': spec.spec_currency_db,
        'currencyRate': float(spec.spec_currency_rate_db or 1.0),
        'totalAmount': float(spec.spec_total_amount_db or 0),
        'items': items_data
    }), 200
# ----------------------------------------------------------------------------------------------------------

# Оновлення існуючої специфікації (API PUT)
@app.route('/api/specifications/<int:spec_id>', methods=['PUT'])
def update_specification(spec_id):
    spec = Specification.query.get_or_404(spec_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': "Дані відсутні"}), 400

    # Оновлюємо загальні поля специфікації    
    spec.spec_number_db = data.get('spec-number')
    spec.spec_currency_db = data.get('spec-currency')
    spec.spec_currency_rate_db = data.get('spec-currency-rate') or 1.0000
    spec.spec_total_amount_db = data.get('spec-total-amount-in-uah') or 0.00

    # Видаляємо старі пов'язані записи оплат та товари, щоб перезаписати їх новими з форми
    old_items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
    for item in old_items:
        PaymentShippingRecord.query.filter_by(item_id=item.id).delete()
    SpecificationItem.query.filter_by(specification_id=spec.id).delete()

    # Додаємо нові товари та їх оплати/відвантаження
    items_data = data.get('items', [])
    for item in items_data:
        new_item = SpecificationItem(
            specification_id=spec.id,            
            product_name_db=item.get('productName'),
            product_qty_db=item.get('productQty') or 0,
            product_price_db=item.get('productPrice') or 0,
            product_vat_db=item.get('productVat')
        )
        db.session.add(new_item)
        db.session.flush()

        records_data = item.get('payShipRecords', [])
        for rec in records_data:
            new_record = PaymentShippingRecord(
                item_id=new_item.id,
                pay_date_db=rec.get('payDate'),
                pay_sum_db=rec.get('paySum') or 0,
                ship_date_db=rec.get('shipDate'),
                ship_sum_db=rec.get('shipSum') or 0
            )
            db.session.add(new_record)

    db.session.commit()
    return jsonify({'message': 'Специфікацію успішно оновлено!'}), 200
# ----------------------------------------------------------------------------------------------



    




if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

