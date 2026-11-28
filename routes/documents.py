from flask import Blueprint, request, jsonify, send_from_directory
import os
from extensions import db
from models import Contract, Specification, ContractDocument

documents_bp = Blueprint('documents', __name__)

MAIN_STORAGE = os.path.join(os.getcwd(), 'contracts_docs')

# 8.1. Завантаження нового документа до договору (API POST)
@documents_bp.route('/api/contracts/<int:contract_id>/documents', methods=['POST'])
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

    # Перевіряємо/створюємо основну папку contracts_docs
    if not os.path.exists(MAIN_STORAGE):
        os.makedirs(MAIN_STORAGE)

    # Перевіряємо/створюємо папку договору (формат BR-2_26)
    contract_folder = os.path.join(MAIN_STORAGE, safe_folder_name)
    if not os.path.exists(contract_folder):
        os.makedirs(contract_folder)

    # Формуємо назву файлу за шаблоном: [Номер]_[тип_документа].[розширення]
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
        file_path_db=f"/contracts_docs/{safe_folder_name}/{new_file_name}"
    )
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({'message': 'Документ успішно завантажено!', 'id': new_doc.id, 'file_name': new_file_name}), 201
# -------------------------------------------------------------------------------------------------

# 8.2. Отримання списку документів конкретного договору (API GET)
@documents_bp.route('/api/contracts/<int:contract_id>/documents', methods=['GET'])
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

# 8.3. API: Перегляд або завантаження файлу договору за ID документа з бази
@documents_bp.route('/api/documents/<int:doc_id>/download')
def download_document_by_id(doc_id):
    doc = ContractDocument.query.get_or_404(doc_id)
    
    archive_dir = os.path.abspath('contracts_docs')
    
    # file_path_db зберігає шлях типу /contracts_docs/БР-23_26/БР-23_26_dohovir.pdf
    relative_path = doc.file_path_db.lstrip('/')
    full_path = os.path.join(os.getcwd(), relative_path)
    
    if not os.path.exists(full_path):
        return "Файл не знайдено на диску", 404
        
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    
    return send_from_directory(directory, filename)
# --------------------------------------------------------------------------------------------------

# 8.4. Завантаження нового документа до конкретної специфікації (API POST)
@documents_bp.route('/api/specifications/<int:spec_id>/documents', methods=['POST'])
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

    # Шлях до папки договору: contracts_docs/БР-7_26
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
        file_path_db=f"/contracts_docs/{safe_folder_name}/{spec_folder_name}/{new_file_name}"
    )
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({
        'message': 'Документ специфікації успішно завантажено!',
        'id': new_doc.id,
        'file_name': new_file_name
    }), 201
# --------------------------------------------------------------------------------------------------------

# 8.5. Отримання списку документів конкретної специфікації (API GET)
@documents_bp.route('/api/specifications/<int:spec_id>/documents', methods=['GET'])
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

# 8.6. Видалення документів прикріплених як до самого договору, так і до кожної специфікації окремо (API DELETE)
@documents_bp.route('/api/documents/<int:doc_id>', methods=['DELETE'])
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