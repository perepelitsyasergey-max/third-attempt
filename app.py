# =================================================================================================
#    1.  Налаштування
# =================================================================================================

from flask import Flask
import os
from dotenv import load_dotenv
from extensions import db

# Імпортуємо класи
from models import User, Product, Counterparty, Contract, Specification, SpecificationItem, PaymentShippingRecord, ContractDocument


from routes.analytics import analytics_bp               # Імпортуємо аналітику
from routes.products import products_bp                 # Імпортуємо товари
from routes.counterparties import counterparties_bp     # Імпортуємо контрагентів
from routes.contracts import contracts_bp               # Імпортуємо договори
from routes.specifications import specifications_bp     # Імпортуємо специфікації
from routes.documents import documents_bp               # Імпортуємо документи
from routes.auth import auth_bp                         # Імпортуємо логування


load_dotenv()           # Завантажуємо змінні з файла .env

app = Flask(__name__)   # Створюємо екземпляр веб-додатку Flask


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')   # Зберігаємо налаштування бази даних з .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')      # Задаємо секретний ключ для безпеки сесій та шифрування
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # Вимикаємо зайве відстеження змін у базі задля економії пам'яті
db.init_app(app)        # Зв'язує базу даних (db) з Flask-додатком (app), щоб
                        # застосунок міг використовувати налаштування підключення та керувати базою.



app.register_blueprint(auth_bp)             # Реєструємо логування
app.register_blueprint(products_bp)         # Реєструємо продукти
app.register_blueprint(counterparties_bp)   # Реєструємо контрагентів
app.register_blueprint(contracts_bp)        # Реєструємо договори
app.register_blueprint(specifications_bp)   # Реєструємо специфікації
app.register_blueprint(documents_bp)        # Реєструємо документи
app.register_blueprint(analytics_bp)        # Реєструємо блупринт аналітики



if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

