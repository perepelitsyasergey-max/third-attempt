# =================================================================================================
#    1  Налаштування
# =================================================================================================

from flask import Flask, render_template, request, jsonify, session, redirect
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os


# Завантажуємо змінні з файла .env
load_dotenv()

app = Flask(__name__)

# Отримуємо значення з .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Головна папка для збереження документів
MAIN_STORAGE = os.path.join(os.getcwd(), 'contracts_archive')


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
    pay_deadline_db = db.Column(db.String(50), nullable=True)   # <--- НОВЕ ПОЛЕ: Крайня дата оплати
    ship_deadline_db = db.Column(db.String(50), nullable=True)  # <--- НОВЕ ПОЛЕ: Крайня дата поставки


# 2.5. Записи оплат та відвантажень для кожного рядка товару
class PaymentShippingRecord(db.Model):
    __tablename__ = 'payment_shipping_records'

    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор запису
    item_id = db.Column(db.Integer, db.ForeignKey('specification_items.id'), nullable=False)  # Зв'язок із конкретним рядком товару у специфікації
    pay_date_db = db.Column(db.String(50), nullable=True)  # Дата оплати
    pay_sum_db = db.Column(db.Numeric(12, 2), nullable=True, default=0.00)  # Сума оплати
    ship_date_db = db.Column(db.String(50), nullable=True)  # Дата поставки (відвантаження)
    ship_sum_db = db.Column(db.Numeric(12, 2), nullable=True, default=0.00)  # Сума поставки

    # 2.6. Документи по договору
class ContractDocument(db.Model):
    __tablename__ = 'contract_documents'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    # 📌 ДОДАЄМО ЗВ'ЯЗОК ЗІ СПЕЦИФІКАЦІЄЮ (може бути порожнім, якщо документ прив'язаний напряму до договору)
    specification_id = db.Column(db.Integer, db.ForeignKey('specifications.id', ondelete='CASCADE'), nullable=True)
    doc_type_db = db.Column(db.String(50), nullable=False)     # Тип (dohovir, akt_posluh, vydatkova, rakhunok тощо)
    file_name_db = db.Column(db.String(255), nullable=False)   # Оригінальна назва файлу або збережена назва
    file_path_db = db.Column(db.String(500), nullable=False)   # Шлях до файлу на сервері



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
        archival_contracts_db=True if data.get('archival-contracts') else False,
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
    try:
        contracts = Contract.query.all()
        contracts_list = []

        for i in contracts:
            # ЗАХИСНИЙ МЕХАНІЗМ: якщо номер відсутній у базі (старі записи), формуємо його на льоту за ID
            reg_number_with_value = i.reg_number_contract_db
            if not reg_number_with_value:
                reg_number_with_value = f"БР-{i.id}/26"

            # --- ЗБИРАЄМО ФІНАНСОВІ ДАНІ ТА ВАЛЮТУ ЗІ СПЕЦИФІКАЦІЙ ЦЬОГО ДОГОВОРУ ---
            
            # Знаходимо всі специфікації, які належать до поточного договору
            specs = Specification.query.filter_by(contract_id=i.id).all()
            
            total_contract_amount = 0  # Загальна сума договору
            total_paid_amount = 0      # Загальна сума оплат
            total_shipped_amount = 0   # Загальна сума відвантажень
            currencies = set()         # Використовуємо Set (множину), щоб уникнути дублікатів валют

            for spec in specs:
                # Зберігаємо валюту специфікації, якщо вона вказана
                if spec.spec_currency_db:
                    currencies.add(spec.spec_currency_db)
                
                # Знаходимо всі товари (рядки) всередині цієї специфікації
                items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
                
                # Рахуємо суму специфікації у рідній валюті (Кількість × Ціна за одиницю)
                spec_native_total = sum(float(item.product_qty_db or 0) * float(item.product_price_db or 0) for item in items)
                total_contract_amount += spec_native_total

                # Підсумовуємо оплати та відвантаження по всіх рядках товарів
                for item in items:
                    records = PaymentShippingRecord.query.filter_by(item_id=item.id).all()
                    total_paid_amount += sum(float(r.pay_sum_db or 0) for r in records)
                    total_shipped_amount += sum(float(r.ship_sum_db or 0) for r in records)

            # Перетворюємо множину валют у зручний рядок (наприклад, "UAH" або "USD, EUR")
            currency_str = ", ".join(currencies) if currencies else "UAH"

            # Формуємо фінальний об'єкт договору для передачі на фронтенд
            contracts_list.append({
                'id': i.id,
                'reg_number': reg_number_with_value,
                'agreement_number': i.agreement_number_db,
                'contract_number': i.contract_number_db,
                'counterparty_1': i.counterparty_1_db,
                'counterparty_2': i.counterparty_2_db,
                'contract_date': i.contract_date_db,
                'end_date': i.end_date_db,
                'contract_type': i.contract_type_db,
                'contract_stage': i.contract_stage_db,
                'user': i.user_db,
                'is_archived': i.archival_contracts_db,
                # Нові фінансові поля для відображення в таблиці договорів:
                'currency': currency_str,
                'total_amount': total_contract_amount,
                'paid_amount': total_paid_amount,
                'shipped_amount': total_shipped_amount
            })

        return jsonify(contracts_list), 200
    except Exception as e:
        print(f"ПОМИЛКА У GET_CONTRACTS: {str(e)}")
        return jsonify({'error': str(e)}), 500
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
        'archival_contracts': contract.archival_contracts_db,
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

    # ЗАПОБІЖНИК: Перевіряємо валюту існуючих специфікацій цього договору
    new_currency = data.get('spec-currency')    
    existing_specs = Specification.query.filter_by(contract_id=contract.id).all()
    for spec in existing_specs:
        if spec.spec_currency_db and spec.spec_currency_db != new_currency:
            return jsonify({
                'error': f"Неможливо створити специфікацію в іншій валюті ({new_currency}). Усі специфікації цього договору мають бути в єдиній валюті: {spec.spec_currency_db}."
            }), 400

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
            product_vat_db=item.get('productVat'),
            pay_deadline_db=item.get('payDeadline'),
            ship_deadline_db=item.get('shipDeadline')
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

    try:
        # 1. Видаляємо всі прикріплені документи договору з бази (та за бажанням файли з диску)
        documents = ContractDocument.query.filter_by(contract_id=contract.id).all()
        for doc in documents:
            # Якщо потрібно також видаляти самі файли з папки на диску, можна розкоментувати:
            # if doc.file_path and os.path.exists(doc.file_path):
            #     os.remove(doc.file_path)
            db.session.delete(doc)

        # 2. Знаходимо всі специфікації цього договору
        specs = Specification.query.filter_by(contract_id=contract.id).all()
        for spec in specs:
            # 3. Знаходимо всі товари (items) цієї специфікації
            items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
            for item in items:
                # 4. Видаляємо записи оплат та відвантажень для кожного товару
                PaymentShippingRecord.query.filter_by(item_id=item.id).delete()
            
            # 5. Видаляємо товари специфікації
            SpecificationItem.query.filter_by(specification_id=spec.id).delete()
        
        # 6. Видаляємо самі специфікації договору
        Specification.query.filter_by(contract_id=contract.id).delete()

        # 7. Тепер, коли всі дочірні записи (документи, специфікації тощо) видалено, безпечно видаляємо сам договір
        db.session.delete(contract)
        db.session.commit()

        return jsonify({'message': 'Договір та всі пов’язані документи і специфікації успішно видалено'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500# -----------------------------------------------------------------------------------------------------------

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
                'pay_deadline': item.pay_deadline_db or '',
                'ship_deadline': item.ship_deadline_db or '',
                'paid': item_paid,
                'shipped': item_shipped
            })

        # Отримуємо документи, прив'язані до цієї специфікації
        spec_docs = ContractDocument.query.filter_by(specification_id=spec.id).all()
        docs_data = [{'id': d.id, 'doc_type': d.doc_type_db, 'file_name': d.file_name_db, 'file_path': d.file_path_db} for d in spec_docs]
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
            'items': items_data,
            'documents': docs_data  # <--- Передаємо документи на фронтенд
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
            'payDeadline': item.pay_deadline_db or '',   # <--- Відправляємо на фронтенд
            'shipDeadline': item.ship_deadline_db or '', # <--- Відправляємо на фронтенд
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

    
    # ЗАПОБІЖНИК: Перевіряємо валюту інших специфікацій цього ж договору
    new_currency = data.get('spec-currency')    
    existing_specs = Specification.query.filter_by(contract_id=spec.contract_id).all()
    for existing_spec in existing_specs:
        # Пропускаємо поточну специфікацію, яку редагуємо
        if existing_spec.id != spec.id and existing_spec.spec_currency_db:
            if existing_spec.spec_currency_db != new_currency:
                return jsonify({
                    'error': f"Неможливо змінити валюту на {new_currency}. Інші специфікації цього договору використовують валюту: {existing_spec.spec_currency_db}."
                }), 400

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
            product_vat_db=item.get('productVat'),
            pay_deadline_db=item.get('payDeadline'),
            ship_deadline_db=item.get('shipDeadline')
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
                ship_sum_db=rec.get('shipSum') or 0,                
            )
            db.session.add(new_record)

    db.session.commit()
    return jsonify({'message': 'Специфікацію успішно оновлено!'}), 200
# ----------------------------------------------------------------------------------------------
# 6.7. Отримання списку документів конкретного договору (API GET)
@app.route('/api/contracts/<int:contract_id>/documents', methods=['GET'])
def get_contract_documents(contract_id):
    # Отримуємо документи які завантажені під самий договір безпосередньо
    docs = ContractDocument.query.filter_by(contract_id=contract_id, specification_id=None).all()
    
    # Створюємо логічний порядок для типів документів
    type_priority = {
        "dohovir": 1,
        "dodatkova_uhoda": 2,
        "akt_pryimannya_peredachi": 3,
        "akt_posluh": 4,
        "akt_davalnynskoyi": 5,
        "vydatkova": 6,
        "rakhunok": 7,
        "tekhnichne_zavdannya": 8,
        "memorandum": 9,
        "nda": 10,
        "inshe": 11
    }
    
    # Сортуємо масив у Python за пріоритетом типу, а потім за назвою файлу
    docs_sorted = sorted(docs, key=lambda d: (type_priority.get(d.doc_type_db, 99), d.file_name_db))

    docs_list = []
    for d in docs_sorted:
        docs_list.append({
            'id': d.id,
            'doc_type': d.doc_type_db,
            'file_name': d.file_name_db,
            'file_path': d.file_path_db
        })
    return jsonify(docs_list), 200
# -------------------------------------------------------------------------------------------------


# 6.8. Завантаження нового документа до договору (API POST)
@app.route('/api/contracts/<int:contract_id>/documents', methods=['POST'])
def upload_contract_document(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не передано'}), 400
    
    file = request.files['file']
    doc_type = request.form.get('doc_type', 'dohovir') # наприклад: dohovir, akt_posluh, vydatkova, rakhunok

    if file.filename == '':
        return jsonify({'error': 'Файл не обрано'}), 400

    # Визначаємо реєстраційний номер договору для папки (якщо немає, беремо з ID)
    reg_number = contract.reg_number_contract_db or f"BR-{contract.id}_26"
    safe_folder_name = reg_number.replace('/', '_').replace('\\', '_')

    # 1. Перевіряємо/створюємо основну папку contracts_archive
    if not os.path.exists(MAIN_STORAGE):
        os.makedirs(MAIN_STORAGE)

    # 2. Перевіряємо/створюємо папку договору (формат BR-2_26)
    contract_folder = os.path.join(MAIN_STORAGE, safe_folder_name)
    if not os.path.exists(contract_folder):
        os.makedirs(contract_folder)

    # 3. Формуємо назву файлу за шаблоном: [Номер]_[тип_документа].[розширення]
    file_ext = os.path.splitext(file.filename)[1]
    base_name = f"{safe_folder_name}_{doc_type}"
    new_file_name = f"{base_name}{file_ext}"
    target_path = os.path.join(contract_folder, new_file_name)

    # Якщо файл уже існує, підбираємо наступний порядковий номер (_2, _3, _4...)
    counter = 2
    while os.path.exists(target_path):
        new_file_name = f"{base_name}_{counter}{file_ext}"
        target_path = os.path.join(contract_folder, new_file_name)
        counter += 1

    file.save(target_path)

    # Зберігаємо інформацію в базу даних
    new_doc = ContractDocument(
        contract_id=contract.id,
        doc_type_db=doc_type,
        file_name_db=new_file_name,
        file_path_db=f"/contracts_archive/{safe_folder_name}/{new_file_name}"
    )
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({'message': 'Документ успішно завантажено!', 'id': new_doc.id, 'file_name': new_file_name}), 201
# -------------------------------------------------------------------------------------------------

# 6.9. Видалення документа (API DELETE)
@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
def delete_contract_document(doc_id):
    doc = ContractDocument.query.get_or_404(doc_id)
    
    # Повний шлях до файлу на диску
    if doc.file_path_db:
        # Відсікаємо провідний слеш для об'єднання шляхів
        relative_path = doc.file_path_db.lstrip('/')
        full_path = os.path.join(os.getcwd(), relative_path)
        
        # Фізично видаляємо файл, якщо він існує
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                print(f"Помолка видалення файлу з диска: {e}")

    db.session.delete(doc)
    db.session.commit()

    return jsonify({'message': 'Документ успішно видалено'}), 200
# -------------------------------------------------------------------------------------------------

# API: Перегляд або завантаження файлу договору за ID документа з бази
@app.route('/api/documents/<int:doc_id>/download')
def download_document_by_id(doc_id):
    doc = ContractDocument.query.get_or_404(doc_id)
    
    archive_dir = os.path.abspath('contracts_archive')
    
    # file_path_db зберігає шлях типу /contracts_archive/БР-23_26/БР-23_26_dohovir.pdf
    relative_path = doc.file_path_db.lstrip('/')
    full_path = os.path.join(os.getcwd(), relative_path)
    
    if not os.path.exists(full_path):
        return "Файл не знайдено на диску", 404
        
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    
    return send_from_directory(directory, filename)
# --------------------------------------------------------------------------------------------------

# =================================================================================================
#    ДОКУМЕНТИ СПЕЦИФІКАЦІЙ (НОВІ МАРШРУТИ)
# =================================================================================================

# 1. Отримання списку документів конкретної специфікації (API GET)
@app.route('/api/specifications/<int:spec_id>/documents', methods=['GET'])
def get_specification_documents(spec_id):
    docs = ContractDocument.query.filter_by(specification_id=spec_id).all()
    
    docs_list = []
    for d in docs:
        docs_list.append({
            'id': d.id,
            'doc_type': d.doc_type_db,
            'file_name': d.file_name_db,
            'file_path': d.file_path_db
        })
    return jsonify(docs_list), 200
# -------------------------------------------------------------------------------------------------

# 2. Завантаження нового документа до конкретної специфікації (API POST)
@app.route('/api/specifications/<int:spec_id>/documents', methods=['POST'])
def upload_specification_document(spec_id):
    spec = Specification.query.get_or_404(spec_id)
    contract = Contract.query.get_or_404(spec.contract_id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не передано'}), 400
    
    file = request.files['file']
    doc_type = request.form.get('doc_type', 'dohovir')

    if file.filename == '':
        return jsonify({'error': 'Файл не обрано'}), 400

    # Визначаємо реєстраційний номер договору для батьківської папки
    reg_number = contract.reg_number_contract_db or f"BR-{contract.id}_26"
    safe_folder_name = reg_number.replace('/', '_').replace('\\', '_')

    # Шлях до папки договору: contracts_archive/БР-7_26
    contract_folder = os.path.join(MAIN_STORAGE, safe_folder_name)
    if not os.path.exists(contract_folder):
        os.makedirs(contract_folder)

    # 📌 СТВОРЮЄМО ПІДПАПКУ СПЕЦИФІКАЦІЇ: spec_<id> (наприклад, spec_15)
    spec_folder_name = f"spec_{spec.id}"
    spec_folder_path = os.path.join(contract_folder, spec_folder_name)
    if not os.path.exists(spec_folder_path):
        os.makedirs(spec_folder_path)

    # Формуємо назву файлу
    file_ext = os.path.splitext(file.filename)[1]
    base_name = f"{safe_folder_name}_spec{spec.id}_{doc_type}"
    new_file_name = f"{base_name}{file_ext}"
    target_path = os.path.join(spec_folder_path, new_file_name)

    # Захист від дублікатів імен файлів
    counter = 2
    while os.path.exists(target_path):
        new_file_name = f"{base_name}_{counter}{file_ext}"
        target_path = os.path.join(spec_folder_path, new_file_name)
        counter += 1

    file.save(target_path)

    # Зберігаємо інформацію в базу даних (зв'язуємо і з договором, і зі специфікацією)
    new_doc = ContractDocument(
        contract_id=contract.id,
        specification_id=spec.id,
        doc_type_db=doc_type,
        file_name_db=new_file_name,
        file_path_db=f"/contracts_archive/{safe_folder_name}/{spec_folder_name}/{new_file_name}"
    )
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({
        'message': 'Документ специфікації успішно завантажено!',
        'id': new_doc.id,
        'file_name': new_file_name
    }), 201
# --------------------------------------------------------------------------------------------------------

# =================================================================================================
#    АНАЛІТИКА ТА ДЕДЛАЙНИ ДЛЯ ГОЛОВНОЇ СТОРІНКИ (API)
# =================================================================================================
from datetime import datetime

@app.route('/api/dashboard/deadlines', methods=['GET'])
def get_dashboard_deadlines():
    try:
        deadlines_list = []
        today = datetime.now().date()

        # 1. Збираємо дедлайни завершення договорів
        contracts = Contract.query.all()
        for contract in contracts:
            if contract.contract_stage_db == 'completed':
                continue

            if contract.end_date_db:
                try:
                    date_str = contract.end_date_db.strip()
                    if '.' in date_str:
                        d_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
                    else:
                        d_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    reg_num = contract.reg_number_contract_db or f"БР-{contract.id}/26"
                    
                    # Формуємо деталі: Угода + Договір
                    agreement_part = f"Угода: {contract.agreement_number_db}" if contract.agreement_number_db else ""
                    contract_num_part = f"Договір: {contract.contract_number_db}" if contract.contract_number_db else ""
                    details_str = " | ".join(filter(None, [agreement_part, contract_num_part])) or "Без номерів"

                    deadlines_list.append({
                        'type': 'contract_end',
                        'category_label': 'Закінчення договору',
                        'title': f"Договір {reg_num}",
                        'date': date_str,
                        'date_obj': d_obj.isoformat(),
                        'contract_id': contract.id,
                        'reg_number': reg_num,
                        'counterparty': contract.counterparty_1_db or contract.counterparty_2_db or 'Не вказано',
                        'details': details_str,
                        'user': contract.user_db or ''  # <--- Додано для договорів
                    })
                except Exception as ex:
                    print(f"Помилка парсингу дати договору {contract.id}: {ex}")

        # 2. Збираємо дедлайни оплат та відвантажень зі специфікацій
        specs = Specification.query.all()
        for spec in specs:
            contract = Contract.query.get(spec.contract_id)
            if not contract:
                continue
            
            if contract.contract_stage_db == 'completed':
                continue

            reg_num = contract.reg_number_contract_db or f"БР-{contract.id}/26"
            counterparty = contract.counterparty_1_db or contract.counterparty_2_db or 'Не вказано'

            # Базові номери для специфікації
            agreement_part = f"Угода: {contract.agreement_number_db}" if contract.agreement_number_db else ""
            contract_num_part = f"Договір: {contract.contract_number_db}" if contract.contract_number_db else ""
            nums_str = " | ".join(filter(None, [agreement_part, contract_num_part]))

            items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
            for item in items:
                # Перевіряємо фактичні оплати/відвантаження, щоб закриті дедлайни не світилися як прострочені
                records = PaymentShippingRecord.query.filter_by(item_id=item.id).all()
                total_item_cost = (float(item.product_qty_db or 0) * float(item.product_price_db or 0))

                # Крайня дата оплати
                if item.pay_deadline_db:
                    total_paid = sum(float(r.pay_sum_db or 0) for r in records)
                    if total_paid < total_item_cost: # Показуємо тільки якщо не сплачено повністю
                        try:
                            date_str = item.pay_deadline_db.strip()
                            d_obj = datetime.strptime(date_str, '%d.%m.%Y' if '.' in date_str else '%Y-%m-%d').date()

                            item_details = f"{nums_str} | Товар: {item.product_name_db}" if nums_str else f"Товар: {item.product_name_db}"

                            deadlines_list.append({
                                'type': 'payment_deadline',
                                'category_label': 'Термін оплати',
                                'title': f"Специфікація № {spec.spec_number_db or spec.id}",
                                'date': date_str,
                                'date_obj': d_obj.isoformat(),
                                'contract_id': contract.id,
                                'reg_number': reg_num,
                                'counterparty': counterparty,
                                'details': item_details,
                                'user': contract.user_db or ''  # <--- Додано для оплат
                            })
                        except Exception as ex:
                            print(f"Помилка дедлайну оплати товару {item.id}: {ex}")

                # Крайня дата поставки
                if item.ship_deadline_db:
                    total_shipped = sum(float(r.ship_sum_db or 0) for r in records)
                    if total_shipped < total_item_cost: # Показуємо тільки якщо не відвантажено повністю
                        try:
                            date_str = item.ship_deadline_db.strip()
                            d_obj = datetime.strptime(date_str, '%d.%m.%Y' if '.' in date_str else '%Y-%m-%d').date()

                            item_details = f"{nums_str} | Товар: {item.product_name_db}" if nums_str else f"Товар: {item.product_name_db}"

                            deadlines_list.append({
                                'type': 'shipment_deadline',
                                'category_label': 'Термін поставки',
                                'title': f"Специфікація № {spec.spec_number_db or spec.id}",
                                'date': date_str,
                                'date_obj': d_obj.isoformat(),
                                'contract_id': contract.id,
                                'reg_number': reg_num,
                                'counterparty': counterparty,
                                'details': item_details,
                                'user': contract.user_db or ''  # <--- Додано для поставок
                            })
                        except Exception as ex:
                            print(f"Помилка дедлайну поставки товару {item.id}: {ex}")

        deadlines_list.sort(key=lambda x: x['date_obj'])
        return jsonify(deadlines_list), 200

    except Exception as e:
        print(f"ПОМИЛКА У GET_DASHBOARD_DEADLINES: {str(e)}")
        return jsonify({'error': str(e)}), 500
    




if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

