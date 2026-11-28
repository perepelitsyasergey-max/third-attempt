from flask import Blueprint, request, jsonify, session
from extensions import db
from models import Contract, Specification, SpecificationItem, PaymentShippingRecord, ContractDocument

contracts_bp = Blueprint('contracts', __name__)

# 6.1. Створення нового Договору (API)
@contracts_bp.route('/api/contracts', methods = ['POST'])
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

# 6.2. Отримання списку всіх договорів (API)
@contracts_bp.route('/api/contracts', methods=['GET'])
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

# 6.3. Отримання даних одного договору за ID (API)
@contracts_bp.route('/api/contracts/<int:contract_id>', methods=['GET'])
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

# 6.4. Оновлення даних існуючого Договору (API)
@contracts_bp.route('/api/contracts/<int:contract_id>', methods=['PUT'])
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

# 6.5. Видалення Договору за ID (API)
@contracts_bp.route('/api/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    contract = Contract.query.get(contract_id)

    if not contract:
        return jsonify({'error': 'Договір не знайдено'}), 404

    try:
        # Видаляємо всі прикріплені документи договору з бази (та за бажанням файли з диску)
        documents = ContractDocument.query.filter_by(contract_id=contract.id).all()
        for doc in documents:
            # Якщо потрібно також видаляти самі файли з папки на диску, можна розкоментувати:
            # if doc.file_path and os.path.exists(doc.file_path):
            #     os.remove(doc.file_path)
            db.session.delete(doc)

        # Знаходимо всі специфікації цього договору
        specs = Specification.query.filter_by(contract_id=contract.id).all()
        for spec in specs:
            # 3. Знаходимо всі товари (items) цієї специфікації
            items = SpecificationItem.query.filter_by(specification_id=spec.id).all()
            for item in items:
                # 4. Видаляємо записи оплат та відвантажень для кожного товару
                PaymentShippingRecord.query.filter_by(item_id=item.id).delete()
            
            # Видаляємо товари специфікації
            SpecificationItem.query.filter_by(specification_id=spec.id).delete()
        
        # Видаляємо самі специфікації договору
        Specification.query.filter_by(contract_id=contract.id).delete()

        # Тепер, коли всі дочірні записи (документи, специфікації тощо) видалено, безпечно видаляємо сам договір
        db.session.delete(contract)
        db.session.commit()

        return jsonify({'message': 'Договір та всі пов’язані документи і специфікації успішно видалено'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# -------------------------------------------------------------------------------------------------------