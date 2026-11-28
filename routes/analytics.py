# =================================================================================================
#    9. АНАЛІТИКА ТА ДЕДЛАЙНИ ДЛЯ ГОЛОВНОЇ СТОРІНКИ (API)
# =================================================================================================

# 9.1. Отримання списку дедлайнів для головної сторінки (API)
from flask import Blueprint, jsonify
from models import Contract, Specification, SpecificationItem, PaymentShippingRecord
from datetime import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/dashboard/deadlines', methods=['GET'])
def get_dashboard_deadlines():
    try:
        deadlines_list = []
        today = datetime.now().date()

        # Збираємо дедлайни завершення договорів
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

        # Збираємо дедлайни оплат та відвантажень зі специфікацій
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
# --------------------------------------------------------------------------------------------------