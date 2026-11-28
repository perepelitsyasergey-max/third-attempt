from flask import Blueprint, request, jsonify
from extensions import db
from models import Contract, Specification, SpecificationItem, PaymentShippingRecord, ContractDocument

specifications_bp = Blueprint('specifications', __name__)

# 7.1. Створення специфікації для конкретного договору (API)
@specifications_bp.route('/api/contracts/<int:contract_id>/specifications', methods=['POST'])
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

    # Створюємо та зберігаємо головну специфікацію
    new_spec = Specification(
        contract_id=contract.id,
        spec_number_db=data.get('spec-number'),
        spec_currency_db=data.get('spec-currency'),
        spec_currency_rate_db=data.get('spec-currency-rate') or 1.0000,
        spec_total_amount_db=data.get('spec-total-amount-in-uah') or 0.00
    )
    db.session.add(new_spec)
    db.session.flush()  # Отримуємо ID новоствореної специфікації до коміту

    # Зберігаємо товари (рядки) специфікації
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

        # Зберігаємо оплати та відвантаження для цього рядка товару
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

# 7.2. Отримання списку всіх специфікацій для конкретного договору (API)
@specifications_bp.route('/api/contracts/<int:contract_id>/specifications', methods=['GET'])
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

# 7.3. Отримання даних однієї специфікації для редагування (API)
@specifications_bp.route('/api/specifications/<int:spec_id>', methods=['GET'])
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

# 7.4. Оновлення існуючої специфікації (API PUT)
@specifications_bp.route('/api/specifications/<int:spec_id>', methods=['PUT'])
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

# 7.5. Видалення специфікації за ID (API)
@specifications_bp.route('/api/specifications/<int:spec_id>', methods=['DELETE'])
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
