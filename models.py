from extensions import db

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