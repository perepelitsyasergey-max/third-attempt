// 📌 1. ПРАВИЛО ІМЕНУВАННЯ ЗМІННИХ (МАПІНГ З HTML)
// При створенні змінних у JavaScript, які відповідають елементам інтерфейсу з HTML-атрибутами у форматі kebab-case (через дефіс, наприклад: specification-id, contract-type), суворо дотримуватися стилю camelCase для назв змінних (наприклад: specificationId, contractType).
// Мета: Зберігати пряму семантичну та логічну відповідність між розміткою та кодом, водночас не порушуючи правила синтаксису JavaScript для ідентифікаторів.



// 1. ЗМІННІ ТА ЕЛЕМЕНТИ DOM
// 1.1. Кнопки вкладок
// 1.2. Контейнери вмісту вкладок
// 1.3. Елементи вкладки "Товари"
// 1.4. Елементи вкладки "Контрагенти"
// 1.5. Елементи вкладки "Договори"
// 1.6. Елементи вкладки "Специфікації" (усередині договору)

// 2. ПЕРЕМИКАННЯ ВКЛАДОК
// 2.1. Перемикання активної вкладки — switchTab()
// 2.2. Обробники подій для кнопок вкладок та активація
// 2.3. Початкова активація вкладки "Договори" при завантаженні сторінки
// 3. ЛОГІКА РОБОТИ З ТОВАРАМИ

// 3.1. Відкриття модального вікна для створення товару — openAddProductModal()
// 3.2. Обробник кліку на кнопку "Додати товар"
// 3.3. Закриття модального вікна "Товари" — closeAddProductModal()
// 3.4. Обробник кліку на хрестик модального вікна "Товари"
// 3.5. Збір даних з форми товару — getProductFormData()
// 3.6. Відправка даних товару на сервер (POST / PUT) — sendProductOnServer()
// 3.7. Обробник кліку на кнопку "Зберегти" у модальному вікні товару
// 3.8. Завантаження всіх товарів з сервера (GET) — loadProducts()
// 3.9. Відображення списку товарів у вигляді таблиці — renderProducts()
// 3.10. Завантаження даних товару для редагування — loadProductDetalis()
// 3.11. Прив'язка подій до кнопок "Редагувати" у таблиці товарів — attachEditProductEvents()
// 3.12. Видалення товару на сервері (DELETE) — deleteProductOnServer()
// 3.13. Прив'язка подій до кнопок "Видалити" у таблиці товарів — attachDeleteProductEvents()

// 4. ЛОГІКА РОБОТИ З КОНТРАГЕНТАМИ
// 4.1. Відкриття модального вікна для створення контрагента — openAddCounterpartyModal()
// 4.2. Обробник кліку на кнопку "Додати Контрагента"
// 4.3. Закриття модального вікна "Контрагенти" — closeAddCounterpartyModal()
// 4.4. Обробник кліку на хрестик модального вікна "Контрагенти"
// 4.5. Збір даних з форми контрагента — getCounterpartyFormData()
// 4.6. Відправка даних контрагента на сервер (POST / PUT) — sendCounterpartyOnServer()
// 4.7. Обробник кліку на кнопку "Зберегти" у модальному вікні контрагента
// 4.8. Завантаження всіх контрагентів з сервера (GET) — loadCounterparties()
// 4.9. Відображення списку контрагентів у вигляді таблиці — renderCounterparties()
// 4.10. Завантаження даних контрагента для редагування — loadCounterpartyDetalis()
// 4.11. Прив'язка подій до кнопок "Редагувати" у таблиці контрагентів — attachEditCounterpartyEvents()
// 4.12. Видалення контрагента на сервері (DELETE) — deleteCounterpartyOnServer()
// 4.13. Прив'язка подій до кнопок "Видалити" у таблиці контрагентів — attachDeleteCounterpartyEvents()

// 5. ЛОГІКА РОБОТИ З ДОГОВОРАМИ
// 5.1. Відкриття модального вікна для створення договору — openAddContracttModal()
// 5.2. Обробник кліку на кнопку "Додати договір"
// 5.3. Закриття модального вікна "Договори" — closeAddContractModal()
// 5.4. Обробник кліку на хрестик модального вікна "Договори"
// 5.5. Збір даних з форми договору — getContractFormData()
// 5.6. Відправка даних договору на сервер (POST / PUT) — sendContractOnServer()
// 5.7. Обробник кліку на кнопку "Зберегти" у модальному вікні договору
// 5.8. Завантаження контрагентів для списку, що випадає — loadCounterpartiesForSelect()
// 5.9. Завантаження всіх договорів з сервера (GET) — loadContracts()
// 5.10. Відображення списку договорів у вигляді таблиці — renderContracts()
// 5.11. Завантаження даних договору за ID для редагування — loadContractDetails()
// 5.12. Прив'язка подій до кнопок "Редагувати" у таблиці договорів — attachEditContractEvents()

// 6. ЛОГІКА РОБОТИ ЗІ СПЕЦИФІКАЦІЯМИ
// 6.1. Оновлення стану поля курсу залежно від обраної валюти — updateCurrencyRateState()
// 6.2. Відкриття модального вікна створення/редагування специфікації — openAddSpecificationModal()
// 6.3. Обробник зміни значення валюти
// 6.4. Обробник кліку на кнопку "Додати специфікацію" у формі договору
// 6.5. Закриття модального вікна специфікацій — closeAddSpecificationModal()
// 6.6. Обробник кліку на хрестик модального вікна специфікацій
// 6.7. Завантаження товарів для списку, що випадає у специфікації — loadProductsForSelect()
// 6.8. Автозаповнення ціни при виборі товару — attachRowProductSelectEvent()
// 6.9. Розрахунок вартості конкретного рядка товару — calculateRowCost()
// 6.10. Прив'язка подій введення кількості, ціни та виклику оплат/відвантажень — attachRowEvents()
// 6.11. Динамічне додавання нового рядка товару — addNewSpecificationRow()
// 6.12. Ініціалізація подій для існуючих рядків таблиці
// 6.13. Перерахунок загальних підсумків специфікації — updateSpecificationTotals()
// 6.14. Збір даних специфікації для відправки — getSpecificationFormData()
// 6.15. Відправка даних специфікації на сервер (POST) — sendSpecificationOnServer()
// 6.16. Обробник кліку на кнопку "Зберегти специфікацію"
// 6.17. Завантаження та відображення специфікацій договору — loadContractSpecifications()
// 6.18. Прив'язка подій до кнопок керування специфікаціями — attachSpecificationActionEvents()
// 6.19. Видалення специфікації на сервері (DELETE) — deleteSpecificationOnServer()
// 6.20. Відображення підрахованих сум договору за валютами — updateContractTotalsDisplay()

// 7. ОПЛАТИ ТА ВІДВАНТАЖЕННЯ (МІНІ-ВІКНО)
// 7.1. Відкриття міні-вікна оплат і відвантажень для рядка товару — openPayShipModal()
// 7.2. Додавання рядка запису оплат/відвантажень у модальне вікно — addPayShipRowToModal()
// 7.3. Збереження даних з міні-вікна та оновлення підсумків



document.addEventListener('DOMContentLoaded', () => {

    
    // ===========================================================================================
    // 1. ЗМІННІ ТА ЕЛЕМЕНТИ DOM
    // ===========================================================================================

    // 1.1. Кнопки вкладок
    const btnTabHome = document.getElementById("btn-tab-home");
    const btnTabContracts = document.getElementById("btn-tab-contracts");
    const btnTabCounterparties = document.getElementById("btn-tab-counterparties");
    const btnTabProducts = document.getElementById("btn-tab-products");

    // 1.2. Контейнери вмісту вкладок
    const boxTabHome = document.getElementById("tab-home");
    const boxTabContracts = document.getElementById("tab-contracts");
    const boxTabCounterparties = document.getElementById("tab-counterparties");
    const boxTabProducts = document.getElementById("tab-products");

    // 1.3. Елементи вкладки "Товари"
    const btnOpenModalProduct = document.getElementById('btn-open-modal-product');
    const btnCloseModalProduct = document.getElementById('btn-close-modal-product');
    const modalAddProduct = document.getElementById('modal-add-product');
    const formAddProduct = document.getElementById('form-add-product');
    const btnSaveProduct = document.getElementById('btn-save-product');
    const modalProductTitle = document.getElementById('modal-product-title');

    // 1.4. Елементи вкладки "Контрагенти"
    const btnOpenModalCounterparty = document.getElementById('btn-open-modal-counterparty');
    const btnCloseModalCounterparty = document.getElementById('btn-close-modal-counterparty');
    const formAddCounterparty = document.getElementById('form-add-counterparty');
    const modalCounterpartyTitle = document.getElementById('modal-counterparty-title');
    const modalAddCounterparty = document.getElementById('modal-add-counterparty');
    const btnSaveCounterparty = document.getElementById('btn-save-counterparty');

    // 1.5. Елементи вкладки "Договори"
    const btnOpenModalContract = document.getElementById('btn-open-modal-contract');
    const btnCloseModalContract = document.getElementById('btn-close-modal-contract');
    const formAddContract = document.getElementById('form-add-contract');
    const modalContractTitle = document.getElementById('modal-contract-title');
    const modalAddcontract = document.getElementById('modal-add-contract');
    const btnSaveContract = document.getElementById('btn-save-contract');

    // 1.6. Елементи вкладки "Специфікації" (усередині договору)
    const btnOpenModalSpecification = document.getElementById('btn-add-specification');
    const btnCloseModalSpecification = document.getElementById('btn-close-modal-specification');
    const modalAddSpecification = document.getElementById('modal-add-specification');
    const formAddSpecification = document.getElementById('form-add-specification');

    // Елементи валюти та курсу
    const selectSpecCurrency = document.getElementById('spec-currency');
    const inputSpecCurrencyRate = document.getElementById('spec-currency-rate');

    // Масив для зберігання завантажених товарів та їх цін
    let productsCache = [];

    // ===========================================================================================
    // 2. ПЕРЕМИКАННЯ ВКЛАДОК
    // ===========================================================================================

    // 2.1. Функція перемикання активної вкладки
    function switchTab(activePane) {
        boxTabHome.style.display = "none";
        boxTabContracts.style.display = "none";
        boxTabCounterparties.style.display = "none";
        boxTabProducts.style.display = "none";

        if (activePane) {
            activePane.style.display = "block";
        }
    }
    // -----------------------------------------------------------------------------------------------

    // 2.2. Обробники подій для кнопок вкладок та початкова активація
    btnTabHome.addEventListener("click", function () {
        switchTab(boxTabHome);
    });

    btnTabContracts.addEventListener("click", function () {
        switchTab(boxTabContracts);
        loadContracts();
    });

    btnTabCounterparties.addEventListener("click", function () {
        switchTab(boxTabCounterparties);
        loadCounterparties()
    });

    btnTabProducts.addEventListener("click", function () {
        switchTab(boxTabProducts);
        loadProducts();
    });
    // -----------------------------------------------------------------------------------------------


    // 2.3. Початкова активація вкладки "Товари" при завантаженні сторінки
    switchTab(boxTabContracts);
    loadContracts();
    // -----------------------------------------------------------------------------------------------
    


    // ===========================================================================================
    // 3. ЛОГІКА РОБОТИ З ТОВАРАМИ
    // ===========================================================================================

    // 3.1. Функція відкриття модального вікна для створення товару
    function openAddProductModal() {
        if (formAddProduct) {
            formAddProduct.reset();
        }
        if (modalProductTitle) {
            modalProductTitle.innerText = "Додати новий товар";
        }
        document.getElementById('product-id').value = '';
        modalAddProduct.showModal();
    }
    // -----------------------------------------------------------------------------------------------

    // 3.2. Обробник кліку на кнопку "Додати товар"
    btnOpenModalProduct.addEventListener('click', () => {
        openAddProductModal();
    });
    // -----------------------------------------------------------------------------------------------

    // 3.3. Функція закриття модального вікна Товари
    function closeAddProductModal() {
        modalAddProduct.close();
    }
    // -----------------------------------------------------------------------------------------------

    // 3.4. Обробник кліку на хрестик модального вікна Товари
    btnCloseModalProduct.addEventListener('click', closeAddProductModal);
    // -----------------------------------------------------------------------------------------------

    // 3.5. Функція збору даних з форми товару
    function getProductFormData() {        

        // Збираємо всі поля форми (з атрибутом name) у спеціальний об'єкт FormData
        const formData = new FormData(formAddProduct);

        // formData.entries() розпаковує дані у список пар [ключ, значення],
        // a Object.fromEntries() збирає їх у звичайний об'єкт JavaScript { ключ: значення }
        const productData = Object.fromEntries(formData.entries());
        return productData;
    }
    // -----------------------------------------------------------------------------------------------

    // 3.6. Відправка даних створеного або відредагованого товару на сервер (POST / PUT)
    async function sendProductOnServer(productData) {
        try {
            const productId = productData['product-id'];
            
            let method;
            let url;

            if (productId) {
                method = 'PUT';
                url = `/api/products/${productId}`;
            } else {
                method = 'POST';
                url = '/api/products';
            }

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(productData)
            });

            if (!response.ok) {
                throw new Error(`Помилка сервера: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Помилка при збереженні товару:', error);
            alert('Не вдалося зберегти товар');
            return null;
        }
    }
    // -----------------------------------------------------------------------------------------------

    // 3.7. Обробник кліку на кнопку "Зберегти" у модальному вікні
    if (btnSaveProduct) {
        btnSaveProduct.addEventListener('click', async () => {
            const productData = getProductFormData();
            const result = await sendProductOnServer(productData);
            
            if (result) {
                closeAddProductModal();
                await loadProducts();
            }
        });
    }
    // -----------------------------------------------------------------------------------------------

    // 3.8. Функція завантаження всіх товарів з сервера (GET)
    async function loadProducts() {
        try {
            const response = await fetch('/api/products');
            if (!response.ok) {
                throw new Error('Помилка завантаження товарів');
            }
            const products = await response.json();
            renderProducts(products);
        } catch (error) {
            console.error('Помилка:', error);
        }
    }
    // -----------------------------------------------------------------------------------------------

    // 3.9. Функція відображення списку товарів у вигляді таблиці
    function renderProducts(products) {
        const container = document.getElementById('products-list-container');
        container.innerHTML = '';

        if (products.length === 0) {
            container.innerHTML = '<p>Товари відсутні</p>';
            return;
        }

        const table = document.createElement('table');        
        
        table.innerHTML = `
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Назва товару</th>
                    <th>Ціна</th>
                    <th>Редагувати</th>
                    <th>Видалити</th>
                </tr>
            </thead>
            <tbody></tbody>
        `;

        const tbody = table.querySelector('tbody');

        products.forEach(i => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i.id}</td>
                <td>${i.product_name}</td>
                <td>${i.product_price}</td>
                <td>
                    <button class="btn-edit-product" data-id="${i.id}">Редагувати</button>                    
                </td>
                <td>
                    <button class="btn-delete-product" data-id="${i.id}">Видалити</button>
                </td>
            `;
            tbody.appendChild(row);
        });

        container.appendChild(table);

        attachEditProductEvents(container);
        attachDeleteProductEvents(container);
    }
    // -----------------------------------------------------------------------------------------------

    // 3.10. Функція завантаження даних одного товару для редагування (GET) та відкриття модального вікна
    async function loadProductDetalis(productId) {
        try {
            const response = await fetch(`/api/products/${productId}`);
            if (!response.ok) {
                throw new Error('Помилка завантаження даних товару');
            }
            const product = await response.json();

            if (modalProductTitle) {
                modalProductTitle.innerText = "Редагувати товар";
            }

            document.getElementById('product-id').value = product.id;
            document.getElementById('product-name').value = product.product_name;
            document.getElementById('product-price').value = product.product_price;

            modalAddProduct.showModal();
        } catch (error) {
            console.error('Помилка:', error);
            alert('Не вдалося завантажити дані товару з бази');
        }
    }
    // -----------------------------------------------------------------------------------------------

    // 3.11. Прив'язка подій до кнопок "Редагувати" у таблиці
    function attachEditProductEvents(container) {
        const editButtons = container.querySelectorAll('.btn-edit-product');
        editButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const productId = btn.getAttribute('data-id');
                loadProductDetalis(productId);
            });
        });
    }
    // -----------------------------------------------------------------------------------------------

    // 3.12. Функція відправки DELETE-запиту на сервер для видалення товару
    async function deleteProductOnServer(productId) {
        try {
            const response = await fetch(`/api/products/${productId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Помилка при видаленні товару');
            }

            loadProducts();
        } catch (error) {
            console.error('Помилка видалення:', error);
            alert(`Не вдалося видалити товар: ${error.message}`);
        }
    }
    // -----------------------------------------------------------------------------------------------

    // 3.13. Прив'язка подій до кнопок "Видалити" у таблиці
    function attachDeleteProductEvents(container) {
        const deleteButtons = container.querySelectorAll('.btn-delete-product');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.getAttribute('data-id');
                if (confirm('Ви дійсно бажаєте видалити цей товар?')) {
                    deleteProductOnServer(productId);
                }
            });
        });
    }
    // -----------------------------------------------------------------------------------------------

    // ===========================================================================================
    // 4. ЛОГІКА РОБОТИ З КОНТРАГЕНТИ
    // ===========================================================================================

    // 4.1. Функція відкриття модального вікна для створення товару
    
    function openAddCounterpartyModal() {
        if(formAddCounterparty) {
            formAddCounterparty.reset();
        }
        if (modalCounterpartyTitle) {
            modalCounterpartyTitle.innerText ="Додати контрагента"
        }
        document.getElementById('counterparty-id').value='';
        modalAddCounterparty.showModal();
    }
    // -----------------------------------------------------------------------------------------------

    // 4.2 Обробник кліку на кнопку "Додати Контрагента"
    btnOpenModalCounterparty.addEventListener('click', () => {
        openAddCounterpartyModal();
    })
    // -----------------------------------------------------------------------------------------------

    // 4.3. Функція закриття модального вікна Контрагенти
    function closeAddCounterpartyModal() {
        modalAddCounterparty.close();
    }
    // -----------------------------------------------------------------------------------------------
    
    // 4.4. Обробник кліку на хрестик модального вікна Контрагенти
    btnCloseModalCounterparty.addEventListener('click', closeAddCounterpartyModal);
    // -----------------------------------------------------------------------------------------------

    // 4.5. Функція збору даних з форми Контрагента
    function getCounterpartyFormData() {
        // Збираємо всі поля форми Контрагента (з атрибутом name) у спеціальний об'єкт FormData
        const formData = new FormData(formAddCounterparty);

        // formData.entries() розпаковує дані у список пар [ключ, значення],
        // Object.fromEntries() збирає їх у звичайний об'єкт JavaScript { ключ: значення }
        const counterpartyData = Object.fromEntries(formData.entries());
        return counterpartyData;
    }
    // -------------------------------------------------------------------------------------------------

    // 4.6. Відправка даних створеного або відредагованого Контрагента на сервер (POST / PUT)
    async function sendCounterpartyOnServer (counterpartyData) {
        try {
            const counterpartyId = counterpartyData['counterparty-id'];

            let method;
            let url;
            
            // Якщо редагуємо існуючого контрагента
            if (counterpartyId) {
                method = 'PUT';
                url = `/api/counterparties/${counterpartyId}`;

            }
            // Якщо додаємо нового контрагента
            else {
                method = 'POST';
                url = '/api/counterparties';
            }

            const response = await fetch (url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(counterpartyData)
            });

            if (!response.ok) {
                throw new Error('Помилка сервера: ${response.status}');
            }
            const result = await response.json();
            return result;

        }
        catch (error){
            console.error('Помилка при збережені контрагента:', error);
            alert ('Не вдалося зберегти контрагента');
            return null;
        }        
    }
    // -------------------------------------------------------------------------------------------------



    // 4.7. Обробник кліку на кнопку "Зберегти" у модальному вікні
    if (btnSaveCounterparty) { 
        // Перевіряємо, чи існує кнопка "Зберегти контрагента" на сторінці (щоб уникнути помилки, якщо елемент null)

        btnSaveCounterparty.addEventListener('click', async () => { 
            // Додаємо слухач події кліку на кнопку збереження та робимо функцію асинхронною (async), щоб використовувати await

            const counterpartyData = getCounterpartyFormData(); 
            // Викликаємо функцію збору даних з форми та зберігаємо отриманий об'єкт { ключ: значення } у змінну counterpartyData

            const result = await sendCounterpartyOnServer(counterpartyData); 
            // Відправляємо зібрані дані на бекенд (Flask) через POST-запит та чекаємо (await) на відповідь сервера

            if (result) { 
                // Перевіряємо, чи успішно пройшла відправка на сервер (якщо сервер повернув позитивну відповідь)

                closeAddCounterpartyModal(); 
                // Закриваємо модальне вікно додавання контрагента
                
                await loadCounterparties();
            }
        }); 
        // Закриваємо асинхронну функцію-обробник події кліку
    } 
    // Закриваємо блок перевірки if (btnSaveCounterparty)
    // ----------------------------------------------------------------------------------------------------------------

    // 4.8. Функція завантаження всіх Контрагентів з сервера (GET)
    async function loadCounterparties() {
        try {
            const response =await fetch('/api/counterparties');
            if (!response.ok) {
                throw new Error('Помилка завантаження контрагентів');
            }
            const counterparties = await response.json();
            renderCounterparties(counterparties)
            
        }
        catch (error) {
            console.error('Помилка', error)
        }
    }
    // ---------------------------------------------------------------------------------------------------
    

    // 4.9. Функція відображення списку товарів у вигляді таблиці
    function renderCounterparties(counterparties) {
        const container = document.getElementById('counterparties-list-container');
        container.innerHTML = '';

        if (counterparties.length === 0) {
            container.innerHTML = '<p>Контрагенти відсутні</p>';
            return
        }

        const table = document.createElement('table')

        table.innerHTML = `
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Назва</th>
                    <th>ЄДРПОУ</th>
                    <th>ІПН</th>
                    <th>Контаки</th>
                    <th>Адреса</th>
                    <th>Редагувати</th>
                    <th>Видалити</th>
                </tr>
            </thead>
            <tbody></tbody>
        `;
       // Потрібно сформувати tbody та заповнити його data-рядками:
        const tbody = table.querySelector('tbody');

        counterparties.forEach(i => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i.id}</td>
                <td>${i.counterparty_name || ''}</td>
                <td>${i.counterparty_edrpou || ''}</td>
                <td>${i.counterparty_ipn || ''}</td>
                <td>${i.counterparty_contacts || ''}</td>
                <td>${i.counterparty_adress || ''}</td>
                <td>
                    <button class="btn-edit-counterparty" data-id="${i.id}">Редагувати</button>                    
                </td>
                <td>
                    <button class="btn-delete-counterparty" data-id="${i.id}">Видалити</button>
                </td>
            `;
            tbody.appendChild(row);
        });

        container.appendChild(table);
        attachEditCounterpartyEvents(container);
        attachDeleteCounterpartyEvents(container)
    }


    // 4.10. Функція завантаження даних одного Контрагента для редагування (GET) та відкриття модального вікна
    async function loadCounterpartyDetalis(counterpartyId) {
        try {
            const response = await fetch(`/api/counterparties/${counterpartyId}`);
            if(!response.ok) {
                throw new Error('Помилка завантаження даних контрагента');
            }
            const counterparty = await response.json();

            if (modalCounterpartyTitle) {
                modalCounterpartyTitle.innerText = "Редагування контрагента"
            }

            document.getElementById('counterparty-id').value = counterparty.id;
            document.getElementById('counterparty-name').value = counterparty.name;
            document.getElementById('counterparty-edrpou').value = counterparty.edrpou;
            document.getElementById('counterparty-ipn').value = counterparty.ipn;
            document.getElementById('counterparty-contacts').value = counterparty.contacts;
            document.getElementById('counterparty-adress').value = counterparty.adress;

            modalAddCounterparty.showModal();
        }
        catch (error) {
            console.error('Помилка:', error);
            alert('Не вдалося завантажили дані контрагента з бази');
        }        
    }
    // ---------------------------------------------------------------------------------------------
    
    // 4.11. Прив'язка подій до кнопок "Редагувати" Контрагента у таблиці
    
    function attachEditCounterpartyEvents(container) {
        const editButtons = container.querySelectorAll('.btn-edit-counterparty');
        editButtons.forEach (i => {
            i.addEventListener('click', () => {
                const counterpartyId = i.getAttribute('data-id');
                loadCounterpartyDetalis(counterpartyId);
            });
        });
    }
    // --------------------------------------------------------------------------------------

    // 4.12. Функція відправки DELETE-запиту на сервер для видалення контрагента
    async function deleteCounterpartyOnServer (counterpartyId) {
        try {
            const response = await fetch(`/api/counterparties/${counterpartyId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                // 1. Отримуємо текст помилки від Flask
                const errorData = await response.json(); 
                
                // 2. Кидаємо помилку, щоб зупинити execution
                throw new Error(errorData.error || 'Помилка при видалені контрагента'); 
            }
            loadCounterparties(); // Цей рядок НЕ виконається, якщо була помилка
        } catch (error) {
            // 3. Сюди потрапляє об'єкт Error, який ми тільки-но створили через `throw`
            // error.message буде містити або text з Flask, або ваш дефолтний текст
            alert(`Не вдалося видалити контрагента: ${error.message}`); 
        }
    }
    // ----------------------------------------------------------------------------------------

    // 4.13. Прив'язка подій до кнопок "Видалити" у таблиці Контрагенти

    // Оголошуємо функцію, яка приймає container (блок/контейнер, у якому лежить наша таблиця)
    function attachDeleteCounterpartyEvents(container) {

        // Знаходимо всі елементи з класом btn-delete-counterparty всередині container        
        const deleteButtons = container.querySelectorAll('.btn-delete-counterparty');

        // Перебираємо кожну знайдену кнопку з отриманого списку за допомогою циклу forEach
        deleteButtons.forEach (button => {

            // Вішаємо на поточну кнопку (button) слухач події "клік" (click)
            button.addEventListener('click', function() {

                // Отримуємо значення атрибута data-id кнопки, на яку клікнув користувач (this посилається на цю кнопку)
                const counterpartyId = this.getAttribute('data-id');

                // Показуємо вспливаюче вікно підтвердження (ОК / Скасувати). Якщо користувач натискає "ОК", confirm повертає true
                if (confirm ('Ви дійсно бажаєте видалити цього контрагента?')) {

                    // Викликаємо функцію відправки DELETE-запиту на сервер, передаючи ID контрагента
                    deleteCounterpartyOnServer(counterpartyId);
                }
            }) // Закриваємо анонімну функцію-обробник та метод addEventListener
        }) // Закриваємо цикл forEach
    } // Закриваємо функцію attachDeleteCounterpartyEvents
    // --------------------------------------------------------------------------------------------
    


    // ===========================================================================================
    // 5. ЛОГІКА РОБОТИ З Договорами
    // ===========================================================================================

    // 5.1. Функція відкриття модального вікна для створення Договору    
    async function openAddContracttModal () {
        if (formAddContract) {
            formAddContract.reset();
        }
        if (modalContractTitle) {
            modalContractTitle.innerText = "Додати договір"
        }
        document.getElementById('contract-id').value = '';
        
        // Завантажуємо актуальний список контрагентів у селекти перед відкриттям вікна
        await loadCounterpartiesForSelect();
        
        modalAddcontract.showModal();
    }
    // ------------------------------------------------------------------------------------------
    
    // 5.2 Обробник кліку на кнопку "Додати договір"
    
    btnOpenModalContract.addEventListener('click', () => {
        openAddContracttModal ();
    })
    // ---------------------------------------------------------------------------------------------

    // 5.3. Функція закриття модального вікна Договори
    function closeAddContractModal () {
        modalAddcontract.close();
    }
    // -----------------------------------------------------------------------------------------------
    
    // 5.4. Обробник кліку на хрестик модального вікна Контрагенти
    btnCloseModalContract.addEventListener('click', closeAddContractModal);
    // --------------------------------------------------------------------------------------------------
    
    // 5.5. Функція збору даних з форми Контрагента
    function getContractFormData() {
        // Збираємо всі поля форми Контрагента (з атрибутом name) у спеціальний об'єкт FormData
        const formData = new FormData(formAddContract);

        // formData.entries() розпаковує дані у список пар [ключ, значення],
        // Object.fromEntries() збирає їх у звичайний об'єкт JavaScript { ключ: значення }
        const contractData = Object.fromEntries(formData.entries());

        return contractData;
    }
    // -----------------------------------------------------------------------------------------------------

    // 5.6. Відправка даних створеного або відредагованого Контрагента на сервер (POST / PUT)
    async function sendContractOnServer (contractData) {
        try {
            const contractId = contractData['conrtact-id'];

            let method;
            let url;

            // Якщо редагуємо існуючий договір (тобто наявний ID)
            if (contractId) {
                method = 'PUT'
                url = `/api/contracts/${contractId}`;
            }

            // Якщо додаємо новий договір (тобто ID відсутній)
            else {
                method = 'POST';
                url = '/api/contracts';
            }

            const response = await fetch (url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify(contractData)
            });
            if (!response.ok) {
                throw new Error('Помилка сервера: ${response.status}');
            }

            const result = await response.json();
            return result;
        }
        catch (error) {
            console.error('Помилка при збережені договору:', error);
            alert ('Не вдалося зберегти договір')
            return null;
        }
    }
    // -------------------------------------------------------------------------------------------------            
           
    // 5.7. Обробник кліку на кнопку "Зберегти" у модальному вікні Договір
    if (btnSaveContract) {
        btnSaveContract.addEventListener('click', async () =>{
            const contractData = getContractFormData();
            const result = await sendContractOnServer(contractData);

            if (result) {
                closeAddContractModal();
            }
        });
    }
    // ----------------------------------------------------------------------------------------------------

    // 5.8. Функція завантаження контрагентів для випадаючих списків у формі створення договору
    async function loadCounterpartiesForSelect() {
        try {
            const response = await fetch('/api/counterparties');
            if (!response.ok) {
                throw new Error('Помилка завантаження списку контрагентів');
            }

            const counterparties = await response.json();
            
            // Знаходимо єдиний datalist за його id
            const datalist = document.getElementById('counterparties-list');
            
            if (datalist) {
                let optionsHtml = '';
                counterparties.forEach(i => {
                    // Для кожного контрагента створюємо HTML-тег <option> з його назвою.
                    // Оператор += дописує (додає) новий варіант до вже існуючого рядка.
                    optionsHtml += `<option value="${i.counterparty_name}">`;
                });
                
                datalist.innerHTML = optionsHtml;
            }
        }
        catch (error) {
            console.error('Помилка при завантаженні контрагентів для селекту:', error);
        }
    }
    // -------------------------------------------------------------------------------------------------

    // 5.9. Функція завантаження всіх Договорів з сервера (GET)
    async function loadContracts() {
        try {
            const response = await fetch('/api/contracts');
            if (!response.ok) {
                throw new Error('Помилка завантаження договорів');
            }
            const contracts = await response.json();
            renderContracts(contracts);
        } catch (error) {
            console.error('Помилка:', error);
        }
    }
    // ------------------------------------------------------------------------------------------------------

    // 5.10. Функція відображення списку договорів у вигляді таблиці
    function renderContracts(contracts) {
        const container = document.getElementById('contracts-list-container');
        container.innerHTML = '';

        if (contracts.length === 0) {
            container.innerHTML = '<p>Договори відсутні</p>';
            return;
        }

        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Реєстр. ном. дог. БР</th>
                    <th>Номер договору</th>
                    <th>Контрагент 1</th>
                    <th>Контрагент 2</th>
                    <th>Дата дог.</th>
                    <th>Статус</th>
                    <th>Дії</th>
                </tr>
            </thead>
            <tbody></tbody>
        `;

        const tbody = table.querySelector('tbody');

        contracts.forEach(i => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i.id}</td>
                <td>${i.reg_number || ''}</td>
                <td>${i.contract_number || ''}</td>
                <td>${i.counterparty_1 || ''}</td>
                <td>${i.counterparty_2 || ''}</td>
                <td>${i.contract_date || ''}</td>
                <td>${i.contract_stage || ''}</td>
                <td>
                    <button class="btn-edit-contract" data-id="${i.id}">Редагувати</button>
                </td>
            `;
            tbody.appendChild(row);
        });

        container.appendChild(table);
        attachEditContractEvents(container);
    }
    // -------------------------------------------------------------------------------------------------------

    // 5.11. Функція завантаження даних одного договору за ID для редагування (GET)
    async function loadContractDetails(contractId) {
        try {
            const response = await fetch(`/api/contracts/${contractId}`);
            if (!response.ok) {
                throw new Error('Помилка завантаження даних договору');
            }
            const contract = await response.json();

            if (modalContractTitle) {
                modalContractTitle.innerText = "Редагування договору";
            }

            // Заповнюємо поля форми даними з бази
            document.getElementById('contract-id').value = contract.id;
            document.getElementById('reg-number-contract').value = contract.reg_number || '';
            document.getElementById('agreement-number').value = contract.agreement_number || '';
            document.getElementById('contract-number').value = contract.contract_number || '';
            document.getElementById('counterparty-1').value = contract.counterparty_1 || '';
            document.getElementById('counterparty-2').value = contract.counterparty_2 || '';
            document.getElementById('contract-date').value = contract.contract_date || '';
            document.getElementById('end-date').value = contract.end_date || '';
            document.getElementById('auto-prolongation').checked = contract.auto_prolongation || false;
            document.getElementById('contract-type').value = contract.contract_type || '';
            document.getElementById('contract-stage').value = contract.contract_stage || '';
            document.getElementById('funds-type').value = contract.funds_type || '';
            document.getElementById('contract-notes').value = contract.contract_notes || '';

            // Завантажуємо контрагентів для селектів перед відкриттям
            await loadCounterpartiesForSelect();

            // Завантаження специфікацій для цього договору:
            await loadContractSpecifications(contractId);

            modalAddcontract.showModal();
        } catch (error) {
            console.error('Помилка:', error);
            alert('Не вдалося завантажити дані договору');
        }
    }

    // 5.12. Прив'язка подій до кнопок "Редагувати" у таблиці договорів
    function attachEditContractEvents(container) {
        const editButtons = container.querySelectorAll('.btn-edit-contract');
        editButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const contractId = btn.getAttribute('data-id');
                loadContractDetails(contractId);
            });
        });
    }

    // ===========================================================================================
    // 6. ЛОГІКА РОБОТИ ЗІ СПЕЦИФІКАЦІЯМИ
    // ===========================================================================================

    // 6.1. Функція оновлення стану поля курсу залежно від валюти
    function updateCurrencyRateState() {
        if (!selectSpecCurrency || !inputSpecCurrencyRate) return;

        if (selectSpecCurrency.value === 'UAH') {
            inputSpecCurrencyRate.value = '1.0000';
            inputSpecCurrencyRate.disabled = true;
        } else {
            inputSpecCurrencyRate.value = '0.0000';
            inputSpecCurrencyRate.disabled = false;
        }
    }
    // -----------------------------------------------------------------------------------------------

    // 6.2. Функція відкриття модального вікна для створення або редагування специфікації
    async function openAddSpecificationModal(specId = null) {
        // Очищаємо форму від попередніх заповнень
        if (formAddSpecification) {
            formAddSpecification.reset();
        }
        
        // Зберігаємо або очищаємо ID специфікації у прихованому інпуті форми
        const specificationId = document.getElementById('specification-id');
        if (specificationId) {
            specificationId.value = specId || '';
        }

        // Завантажуємо актуальний список товарів у випадаючий список (datalist)
        await loadProductsForSelect();

        // Знаходимо тіло таблиці товарів у модальному вікні та повністю його очищаємо
        const tbody = document.querySelector('#modal-add-specification .spec-products-table tbody');
        if (tbody) {
            tbody.innerHTML = ''; 
        }

        // Перевіряємо, чи передано ID: якщо так — режим редагування, якщо ні — створення нової
        if (specId) {
            try {
                // Робимо GET-запит на сервер для отримання даних конкретної специфікації
                const response = await fetch(`/api/specifications/${specId}`);
                if (!response.ok) {
                    throw new Error('Помилка завантаження специфікації');
                }
                const specData = await response.json();

                // Заповнюємо шапку специфікації (валюта, курс, загальна сума)
                document.getElementById('spec-number').value = specData.spec_number || '';
                document.getElementById('spec-currency').value = specData.currency || 'UAH';
                document.getElementById('spec-currency-rate').value = specData.currencyRate || 1.0000;
                document.getElementById('spec-total-amount').value = specData.totalAmount || 0.00;
                updateCurrencyRateState(); // Активуємо/деактивуємо поле курсу

                // Якщо у специфікації є збережені товари, заповнюємо ними таблицю
                if (specData.items && specData.items.length > 0) {
                    // Створюємо стільки рядків у таблиці, скільки товарів було збережено
                    specData.items.forEach(() => {
                        addNewSpecificationRow();
                    });

                    // Отримуємо всі щойно створені рядки товарів в таблиці
                    const rows = tbody.querySelectorAll('tr');

                    // Заповнюємо кожен рядок відповідними даними з бази
                    specData.items.forEach((item, idx) => {
                        if (rows[idx]) {
                            const row = rows[idx];
                            
                            // Заповнюємо основні поля товару з безпечним пошуком селекторів
                            const nameInput = row.querySelector('input[name="product-name"]');
                            const qtyInput = row.querySelector('input[name="product-qty"]');
                            const priceInput = row.querySelector('input[name="product-price"]');

                            if (nameInput) nameInput.value = item.productName || '';
                            if (qtyInput) qtyInput.value = item.productQty || '';
                            if (priceInput) priceInput.value = item.productPrice || '';
                            
                            // Заповнюємо ставку ПДВ, якщо вона є
                            const vatSelect = row.querySelector('select[name="product-vat"]');
                            if (vatSelect) {
                                vatSelect.value = item.productVat || '';
                            }

                            // Відновлюємо збережені записи оплат та відвантажень для цього рядка
                            if (item.payShipRecords && item.payShipRecords.length > 0) {
                                // Перетворюємо масив записів (оплат/відвантажень) у текстовий формат JSON (JSON.stringify(item.payShipRecords)) і зберігаємо його в attributes рядка таблиці ('data-pay-ship-records')
                                row.setAttribute('data-pay-ship-records', JSON.stringify(item.payShipRecords));
                                
                                // Рахуємо суми для відображення у мітці
                                let totalPay = item.payShipRecords.reduce((sum, r) => sum + (parseFloat(r.paySum) || 0), 0);
                                let totalShip = item.payShipRecords.reduce((sum, r) => sum + (parseFloat(r.shipSum) || 0), 0);
                                
                                const infoSpan = row.querySelector('.payment-shipping-info');
                                if (infoSpan) {
                                    infoSpan.textContent = `💳 ${totalPay.toFixed(2)} | 📦 ${totalShip.toFixed(2)}`;
                                }
                            }

                            // Перераховуємо вартість рядка та підключаємо слухачі подій
                            calculateRowCost(row);
                            attachRowProductSelectEvent(row);
                            attachRowEvents(row);
                        }
                    });

                    // Оновлюємо загальні підсумки внизу модального вікна
                    updateSpecificationTotals();
                }
            } catch (error) {
                console.error(error);
                alert('Не вдалося завантажити специфікацію для редагування');
                return;
            }
        } else {
            // Режим створення нової специфікації: виставляємо дефолтний курс і додаємо один порожній рядок
            document.getElementById('spec-number').value = '';
            updateCurrencyRateState();
            addNewSpecificationRow();
        }

        // Відкриваємо модальне вікно
        if (modalAddSpecification) {
            modalAddSpecification.showModal();
        }
    }
    // -------------------------------------------------------------------------------------------------------------


    // 6.3. Обробник зміни значення валюти
    if (selectSpecCurrency) {
        selectSpecCurrency.addEventListener('change', () => {
            updateCurrencyRateState();
        });
    }
    // -----------------------------------------------------------------------------------------------

    // 6.4. Обробник кліку на кнопку "Додати специфікацію" у формі договору
    if (btnOpenModalSpecification) {
        btnOpenModalSpecification.addEventListener('click', () => {
            // Перевіряємо, чи збережено договір (чи є значення в інпуті contract-id)
            const contractId = document.getElementById('contract-id').value;
            
            if (!contractId) {
                alert('Будь ласка, спочатку збережіть договір (натисніть кнопку збереження договору), перш ніж додавати специфікації!');
                return; // Зупиняємо виконання і не відкриваємо вікно
            }

            openAddSpecificationModal();
        });
    }
    // -----------------------------------------------------------------------------------------------

    // 6.5. Функція закриття модального вікна специфікацій
    function closeAddSpecificationModal() {
        if (modalAddSpecification) {
            modalAddSpecification.close();
        }
    }
    // -----------------------------------------------------------------------------------------------

    // 6.6. Обробник кліку на хрестик модального вікна специфікацій
    if (btnCloseModalSpecification) {
        btnCloseModalSpecification.addEventListener('click', () => {
            closeAddSpecificationModal();
        });
    }
    // -----------------------------------------------------------------------------------------------

    // 6.7. Функція завантаження товарів для випадаючих списків у формі специфікації
    async function loadProductsForSelect() {
        try {
            const response = await fetch('/api/products');
            if (!response.ok) {
                throw new Error('Помилка завантаження списку товарів');
            }

            // Зберігаємо масив товарів у глобальну змінну для подальшого використання
            productsCache = await response.json();
            
            // Знаходимо datalist за його id у формі специфікації
            const datalist = document.getElementById('products-list');
            
            if (datalist) {
                let optionsHtml = '';
                productsCache.forEach(i => {
                    // Для кожного товару створюємо HTML-тег <option> з його назвою
                    optionsHtml += `<option value="${i.product_name}">`;
                });
                
                datalist.innerHTML = optionsHtml;
            }
        }
        catch (error) {
            console.error('Помилка при завантаженні товарів для селекту:', error);
        }
    }
    // -------------------------------------------------------------------------------------------------

    // 6.8. Функція автозаповнення ціни при виборі товару
    function attachRowProductSelectEvent(row) {
        // Шукаємо інпут за його атрибутом name="product-name" у межах поточного рядка
        const productInput = row.querySelector('input[name="product-name"]');
        
        // Перевіряємо, чи існує цей елемент на сторінці (щоб уникнути помилок, якщо вікно ще не відкрите)
        if (productInput) {
            // Додаємо слухач події 'change', яка спрацьовує, коли користувач завершив вибір варіанту зі списку datalist
            productInput.addEventListener('change', (e) => {
                // Отримуємо текст, який ввів/обрав користувач, та за допомогою .trim() видаляємо зайві пробіли на початку і в кінці
                const selectedName = e.target.value.trim();          
                
                // Проходимо по масиву productsCache і шукаємо об'єкт (товар), у якого поле product_name збігається з обраною назвою
                const foundProduct = productsCache.find(p => p.product_name === selectedName);                
                
                // Шукаємо найближчий батьківський елемент рядка таблиці (<tr>) для поточного інпуту товару
                const row = productInput.closest('tr');
                // Всередині цього ж рядка шукаємо поле введення ціни за його атрибутом name="product-price"
                const priceInput = row.querySelector('input[name="product-price"]');
                
                // Перевіряємо: чи вдалося знайти товар у базі даних (foundProduct) і чи існує поле ціни в цьому рядку (priceInput)
                if (foundProduct && priceInput) {
                    // Якщо все є — автоматично записуємо ціну з бази у значення поля ціни цього рядка
                    priceInput.value = foundProduct.product_price;

                    attachRowEvents(row);      // Активуємо слідкування за кількістю та ціною в цьому рядку
                    calculateRowCost(row);     // Одразу перераховуємо вартість (Кількість × Ціна)
                }
            });
        }
    }
    // -------------------------------------------------------------------------------------------------

    // 6.9. Функція розрахунку вартості конкретного рядка товару
    function calculateRowCost(row) {
        const qtyInput = row.querySelector('input[name="product-qty"]');
        const priceInput = row.querySelector('input[name="product-price"]');
        const costSpan = row.querySelector('.product-cost');

        // Отримуємо значення кількості та ціни (замінюємо кому на крапку на випадок введення через кома)
        const qty = parseFloat(qtyInput.value.replace(',', '.')) || 0;
        const price = parseFloat(priceInput.value.replace(',', '.')) || 0;

        // Множимо кількість на ціну
        const cost = qty * price;

        // Виводимо результат у поле "Вартість" з двома знаками після коми
        if (costSpan) {
            costSpan.textContent = cost.toFixed(2);
        }

        //  Додаємо виклик загального перерахунку вартості, оплат та відвантажень
        updateSpecificationTotals();
    }
    // ---------------------------------------------------------------------------------------------------

    // 6.10. Прив'язка подій введення кількості та ціни для розрахунку
    function attachRowEvents(row) {
        const qtyInput = row.querySelector('input[name="product-qty"]');
        const priceInput = row.querySelector('input[name="product-price"]');

        // Коли користувач змінює кількість або ціну — одразу перераховуємо вартість
        [qtyInput, priceInput].forEach(input => {
            if (input) {
                input.addEventListener('input', () => {
                    calculateRowCost(row);
                });
            }
        });
        // Прив'язка відкриття міні-вікна оплат/відвантажень
        const payShipInfo = row.querySelector('.payment-shipping-info');
        if (payShipInfo) {
            payShipInfo.style.cursor = 'pointer';
            payShipInfo.title = 'Клікніть, щоб редагувати оплати та відвантаження';
            
            payShipInfo.onclick = () => {
                openPayShipModal(row);
            };
        }
    }
    // ------------------------------------------------------------------------------------------------------

    // 6.11. Функція динамічного додавання нового рядка товару до таблиці специфікації
    function addNewSpecificationRow(productData = null) {
        const tbody = document.querySelector('#modal-add-specification .spec-products-table tbody');
        if (!tbody) return;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <input
                    type="text"
                    name="product-name"
                    class="input-field"
                    list="products-list"
                    placeholder="Почніть введення..."
                    value="${productData ? productData.productName : ''}"
                />
            </td>
            <td>
                <input type="number" name="product-qty" class="input-field" value="${productData ? productData.productQty : ''}" />
            </td>
            <td>
                <input type="text" name="product-price" class="input-field" value="${productData ? productData.productPrice : ''}" />
            </td>
            <td>
                <select name="product-vat" class="input-field">
                    <option value="without_vat" ${productData && productData.productVat === 'without_vat' ? 'selected' : ''}>Без ПДВ</option>
                    <option value="with_vat" ${productData && productData.productVat === 'with_vat' ? 'selected' : ''}>З ПДВ</option>
                </select>
            </td>
            <td>
                <span class="product-cost">0.00</span>
            </td>
            <td>
                <span class="payment-shipping-info">💳 0.00 | 📦 0.00</span>
            </td>
            <td>
                <button type="button" class="btn-delete-row">&times;</button>
            </td>
        `;

        // Відновлюємо записи оплат/відвантажень, якщо вони передані (при редагуванні)
        if (productData && productData.payShipRecords && productData.payShipRecords.length > 0) {
            tr.setAttribute('data-pay-ship-records', JSON.stringify(productData.payShipRecords));
            let totalPay = productData.payShipRecords.reduce((sum, r) => sum + (parseFloat(r.paySum) || 0), 0);
            let totalShip = productData.payShipRecords.reduce((sum, r) => sum + (parseFloat(r.shipSum) || 0), 0);
            
            const infoSpan = tr.querySelector('.payment-shipping-info');
            if (infoSpan) {
                infoSpan.textContent = `💳 ${totalPay.toFixed(2)} | 📦 ${totalShip.toFixed(2)}`;
            }
        }

        // Кнопка видалення рядка
        const deleteBtn = tr.querySelector('.btn-delete-row');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                if (tbody.querySelectorAll('tr').length > 0) {
                    tr.remove();
                    // перераховуємо загальні підсумки специфікації (вартість, оплати, відвантаження)
                    updateSpecificationTotals();
                }
            });
        }

        tbody.appendChild(tr);

        // Підключаємо подію автозаповнення ціни та назви при виборі товару з випадаючого списку (datalist) для щойно створеного рядка
        attachRowProductSelectEvent(tr);

        // Підключаємо загальні події для рядка: відстеження змін у полях кількості/ціни для перерахунку та відкриття міні-вікна оплат/відвантажень
        attachRowEvents(tr);
        
        // Якщо товар заповнений (при редагуванні), одразу рахуємо вартість
        if (productData) {
            calculateRowCost(tr);
        }
    }
    // -----------------------------------------------------------------------------------------

    // 6.12. Підключаємо події для всіх наявних рядків таблиці
    const rows = modalAddSpecification.querySelectorAll('tbody tr');
    rows.forEach(row => {
        attachRowProductSelectEvent(row);        
        attachRowEvents(row);
    });
    // -------------------------------------------------------------------------------------------

    const btnAddSpecRow = document.getElementById('btn-add-row'); // або ваш селектор кнопки "+ Додати товар"
    if (btnAddSpecRow) {
        btnAddSpecRow.addEventListener('click', () => {
            addNewSpecificationRow();
        });
    }
    // ----------------------------------------------------------------------------------------------

    // 6.13. Функція перерахунку загальних підсумків специфікації (вартість, оплати, відвантаження)
    function updateSpecificationTotals() {
        const tbody = document.querySelector('#modal-add-specification .spec-products-table tbody');
        if (!tbody) return;

        const rows = tbody.querySelectorAll('tr');
        let totalCost = 0;
        let totalPaid = 0;
        let totalShipped = 0;

        rows.forEach(row => {
            // 1. Рахуємо загальну вартість рядка (Кількість × Ціна)
            const qtyInput = row.querySelector('input[name="product-qty"]');
            const priceInput = row.querySelector('input[name="product-price"]');
            const qty = parseFloat(qtyInput?.value.replace(',', '.')) || 0;
            const price = parseFloat(priceInput?.value.replace(',', '.')) || 0;
            totalCost += (qty * price);

            // 2. Збираємо суми оплат та відвантажень з дата-атрибута рядка
            const storedData = row.getAttribute('data-pay-ship-records');
            if (storedData) {
                try {
                    const records = JSON.parse(storedData);
                    records.forEach(rec => {
                        totalPaid += parseFloat(rec.paySum) || 0;
                        totalShipped += parseFloat(rec.shipSum) || 0;
                    });
                } catch (e) {
                    // Якщо дані не розпарсилися — ігноруємо
                }
            }
        });

        // 3. Знаходимо панель підсумків внизу модального вікна та оновлюємо значення
        const summaryBar = document.querySelector('#modal-add-specification .spec-summary-bar');
        if (summaryBar) {
            const bElements = summaryBar.querySelectorAll('b');
            if (bElements.length >= 3) {
                bElements[0].textContent = `${totalCost.toFixed(2)} грн`;
                bElements[1].textContent = `${totalPaid.toFixed(2)} грн`;
                bElements[2].textContent = `${totalShipped.toFixed(2)} грн`;
            }
        }

        // Також оновлюємо поле "Загальна сума специфікації в грн." у верхній частині форми, якщо воно є
        const specTotalAmountInput = document.getElementById('spec-total-amount');
        if (specTotalAmountInput) {
            specTotalAmountInput.value = totalCost.toFixed(2);
        }
    }
    // -----------------------------------------------------------------------------------------------------

    // 6.14. Функція збору даних зі специфікації для відправки на сервер
    function getSpecificationFormData() {
        const specNumber = document.getElementById('spec-number').value.trim();
        const currency = document.getElementById('spec-currency').value;
        const currencyRate = document.getElementById('spec-currency-rate').value;
        const totalAmount = document.getElementById('spec-total-amount').value;

        const tbody = document.querySelector('#modal-add-specification .spec-products-table tbody');
        const rows = tbody.querySelectorAll('tr');
        
        let items = [];

        rows.forEach(row => {
            const productName = row.querySelector('input[name="product-name"]')?.value.trim() || '';
            const productQty = row.querySelector('input[name="product-qty"]')?.value || 0;
            const productPrice = row.querySelector('input[name="product-price"]')?.value || 0;
            const productVat = row.querySelector('select[name="product-vat"]')?.value || '';

            // Збираємо збережені записи оплат та відвантажень для цього рядка
            let payShipRecords = [];
            const storedData = row.getAttribute('data-pay-ship-records');
            if (storedData) {
                try {
                    payShipRecords = JSON.parse(storedData);
                } catch (e) {
                    payShipRecords = [];
                }
            }

            if (productName) {
                items.push({
                    productName,
                    productQty,
                    productPrice,
                    productVat,
                    payShipRecords
                });
            }
        });

        return {
            'spec-number': specNumber,
            'spec-currency': currency,
            'spec-currency-rate': currencyRate,
            'spec-total-amount': totalAmount,
            'items': items
        };
    }
    // ------------------------------------------------------------------------------------------------------

    // 6.15. Відправка даних специфікації на сервер (POST)
    async function sendSpecificationOnServer(contractId, specData) {
        try {
            const response = await fetch(`/api/contracts/${contractId}/specifications`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(specData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Помилка при збереженні специфікації');
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Помилка:', error);
            alert(`Не вдалося зберегти специфікацію: ${error.message}`);
            return null;
        }
    }

    // 6.16. Обробник кліку на кнопку "Зберегти специфікацію"
    const btnSaveSpecification = document.getElementById('btn-save-specification');
    if (btnSaveSpecification) {
        btnSaveSpecification.addEventListener('click', async () => {
            const contractId = document.getElementById('contract-id').value;
            const specId = document.getElementById('specification-id')?.value;

            if (!contractId) {
                alert('Будь ласка, спочатку збережіть договір!');
                return;
            }

            const specData = getSpecificationFormData();
            
            let url = `/api/contracts/${contractId}/specifications`;
            let method = 'POST';

            if (specId) {
                url = `/api/specifications/${specId}`;
                method = 'PUT';
            }

            try {
                const response = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(specData)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Помилка при збереженні специфікації');
                }

                const result = await response.json();
                alert(result.message);
                closeAddSpecificationModal();

                // Перезавантажуємо список специфікацій у формі договору
                await loadContractSpecifications(contractId);
            } catch (error) {
                console.error('Помилка:', error);
                alert(`Не вдалося зберегти специфікацію: ${error.message}`);
            }
        });
    }
    // ----------------------------------------------------------------------------------------------------------

    // 6.17. Функція завантаження та відображення специфікацій у формі договору
    async function loadContractSpecifications(contractId) {
        const container = document.getElementById('contract-specifications-container'); // Блок у правій колонці праворуч від полів договору
        if (!container) return;

        container.innerHTML = '<p>Завантаження специфікацій...</p>';

        const currencyTotals = {
            'UAH': { total: 0, paid: 0, shipped: 0 },
            'USD': { total: 0, paid: 0, shipped: 0 },
            'EUR': { total: 0, paid: 0, shipped: 0 }
        };

        try {
            const response = await fetch(`/api/contracts/${contractId}/specifications`);
            if (!response.ok) {
                throw new Error('Помилка завантаження специфікацій');
            }

            const specs = await response.json();

            if (specs.length === 0) {
                container.innerHTML = '<p>До цього договору поки немає доданих специфікацій.</p>';
                return;
            }

            let html = '';
            specs.forEach((spec, index) => {
                
                
                const displayNum = `№ ${spec.spec_number}`;

                const curr = (spec.currency || 'UAH').toUpperCase();

                if (currencyTotals[curr]) {
                    currencyTotals[curr].total += parseFloat(spec.total_amount) || 0;
                    currencyTotals[curr].paid += parseFloat(spec.total_paid) || 0;
                    currencyTotals[curr].shipped += parseFloat(spec.total_shipped) || 0;
                }
                
                html += `
                    <div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; border-radius: 5px; background: #fafafa;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                            <div>
                                <strong>Специфікація ${displayNum}</strong> (Валюта: ${spec.currency || 'UAH'})
                            </div>
                            <div>
                                <button type="button" class="btn-edit-spec" data-id="${spec.id}">Редагувати</button>
                                <button type="button" class="btn-delete-spec" data-id="${spec.id}">Видалити</button>
                            </div>
                        </div>
                        
                        <small>Загальна сума: ${spec.total_amount} | Оплачено: ${spec.total_paid} | Відвантажено: ${spec.total_shipped}</small>
                        <table style="width: 100%; margin-top: 5px; font-size: 13px; border-collapse: collapse;" border="1">
                            <thead>
                                <tr style="background: #eee;">
                                    <th>Назва товару</th>
                                    <th>Ціна</th>
                                    <th>Кількість</th>
                                    <th>Загальна сума</th>
                                    <th>Оплачено / Відвантажено</th>
                                </tr>
                            </thead>
                            <tbody>
                `;

                spec.items.forEach(item => {
                    html += `
                        <tr>
                            <td>${item.product_name}</td>
                            <td>${item.price}</td>
                            <td>${item.qty}</td>
                            <td>${item.cost}</td>
                            <td>${item.paid} / ${item.shipped}</td>
                        </tr>
                    `;
                });

                html += `
                            </tbody>
                        </table>
                    </div>
                `;
            });

            container.innerHTML = html;

            // Передаємо пораховані суми для виведення у форму договору
            updateContractTotalsDisplay(currencyTotals);

            // Виклик функції прив'язки подій до кнопок
            attachSpecificationActionEvents(container, contractId);

        } catch (error) {
            console.error('Помилка:', error);
            container.innerHTML = '<p style="color: red;">Не вдалося завантажити специфікації.</p>';
            updateContractTotalsDisplay(currencyTotals);
        }
    }
    // ------------------------------------------------------------------------------------------------------------

    // 6.18. Прив'язка подій до кнопок керування специфікаціями (Редагувати / Видалити)
    function attachSpecificationActionEvents(container, contractId) {
        // Кнопки видалення специфікації
        const deleteButtons = container.querySelectorAll('.btn-delete-spec');
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', async () => {
                const specId = btn.getAttribute('data-id');
                if (confirm('Ви дійсно бажаєте видалити цю специфікацію?')) {
                    await deleteSpecificationOnServer(specId, contractId);
                }
            });
        });

        // Кнопки редагування специфікації
        const editButtons = container.querySelectorAll('.btn-edit-spec');
        editButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const specId = btn.getAttribute('data-id');
                openAddSpecificationModal(specId); // Відкриваємо модальне вікно завантаживши дані цієї специфікації
            });
        });
    }
    // ----------------------------------------------------------------------------------------------------------

    // 6.19. Функція видалення специфікації на сервері (DELETE)
    async function deleteSpecificationOnServer(specId, contractId) {
        try {
            const response = await fetch(`/api/specifications/${specId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Помилка при видаленні специфікації');
            }

            // Перезавантажуємо список специфікацій для поточного договору
            await loadContractSpecifications(contractId);
        } catch (error) {
            console.error('Помилка видалення:', error);
            alert(`Не вдалося видалити специфікацію: ${error.message}`);
        }
    }
    // ---------------------------------------------------------------------------------------------------------

    // 6.20. Функція відображення підрахованих сум договору у формі
    function updateContractTotalsDisplay(totals) {
        document.getElementById('sum-uah').textContent = totals.UAH.total.toFixed(2);
        document.getElementById('paid-uah').textContent = totals.UAH.paid.toFixed(2);
        document.getElementById('shipped-uah').textContent = totals.UAH.shipped.toFixed(2);

        document.getElementById('sum-usd').textContent = totals.USD.total.toFixed(2);
        document.getElementById('paid-usd').textContent = totals.USD.paid.toFixed(2);
        document.getElementById('shipped-usd').textContent = totals.USD.shipped.toFixed(2);

        document.getElementById('sum-eur').textContent = totals.EUR.total.toFixed(2);
        document.getElementById('paid-eur').textContent = totals.EUR.paid.toFixed(2);
        document.getElementById('shipped-eur').textContent = totals.EUR.shipped.toFixed(2);
    }
    // ---------------------------------------------------------------------------------------------------------


    // ===========================================================================================
    // 7. ОПЛА ТИ ТА ВІДВАНТАЖЕННЯ (МІНІ-ВІКНО)
    // ===========================================================================================

    
    // 7.1. Змінні ОПЛА ТИ ТА ВІДВАНТАЖЕННЯ (МІНІ-ВІКНО)
    const modalPayShip = document.getElementById('modal-pay-ship');
    const btnCloseModalPayShip = document.getElementById('btn-close-modal-pay-ship');
    const btnAddPayShipRow = document.getElementById('btn-add-pay-ship-row');
    const btnSavePayShip = document.getElementById('btn-save-pay-ship');
    const payShipTableBody = document.querySelector('#pay-ship-table tbody');
    
    // Змінна для збереження посилання на поточний рядок таблиці товарів, який редагується
    let activeProductRow = null;
    // ----------------------------------------------------------------------------------------------

    // 7.2 Закриття міні-вікна
    if (btnCloseModalPayShip) {
        btnCloseModalPayShip.addEventListener('click', () => {
            if (modalPayShip) modalPayShip.close();
        });
    }
    // -------------------------------------------------------------------------------------------------

    // 7.3. Функція відкриття міні-вікна для конкретного рядка товару
    function openPayShipModal(row) {
        activeProductRow = row;
        
        // Отримуємо назву товару для відображення у заголовку міні-вікна
        const productInput = row.querySelector('input[name="product-name"]') || row.querySelector('#spec-product-input');
        const productNameSpan = document.getElementById('pay-ship-product-name');
        if (productNameSpan) {
            productNameSpan.textContent = productInput ? productInput.value || '(товар не обрано)' : '';
        }

        // Очищаємо таблицю в міні-вікні перед завантаженням
        payShipTableBody.innerHTML = '';

        // Отримуємо збережені дані або створюємо порожній рядок за замовчуванням
        let records = [];
        const storedData = row.getAttribute('data-pay-ship-records');
        if (storedData) {
            try {
                records = JSON.parse(storedData);
            } catch (e) {
                records = [];
            }
        }

        if (records.length === 0) {
            // Якщо записів ще немає, додаємо один порожній рядок
            addPayShipRowToModal('', '', '', '');
        } else {
            // Заповнюємо збереженими записами
            records.forEach(rec => {
                addPayShipRowToModal(rec.payDate, rec.paySum, rec.shipDate, rec.shipSum);
            });
        }

        if (modalPayShip) {
            modalPayShip.showModal();
        }
    }
    // -------------------------------------------------------------------------------------------------------

    // 7.4. Додавання нового рядка у таблицю міні-вікна
    function addPayShipRowToModal(payDate = '', paySum = '', shipDate = '', shipSum = '') {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="date" name="pay-date" class="input-field" value="${payDate}"></td>
            <td><input type="number" step="0.01" name="pay-sum" class="input-field" value="${paySum}" placeholder="0.00"></td>
            <td><input type="date" name="ship-date" class="input-field" value="${shipDate}"></td>
            <td><input type="number" step="0.01" name="ship-sum" class="input-field" value="${shipSum}" placeholder="0.00"></td>
            <td><button type="button" class="btn-delete-row">&times;</button></td>
        `;

        // Кнопка видалення рядка у міні-вікні
        const deleteBtn = tr.querySelector('.btn-delete-row');
        deleteBtn.addEventListener('click', () => {
            if (payShipTableBody.querySelectorAll('tr').length > 1) {
                tr.remove();
            } else {
                // Якщо рядок останній — просто очищаємо його поля
                tr.querySelectorAll('input').forEach(input => input.value = '');
            }
        });

        payShipTableBody.appendChild(tr);
    }

    if (btnAddPayShipRow) {
        btnAddPayShipRow.addEventListener('click', () => {
            addPayShipRowToModal();
        });
    }

    // Збереження даних з міні-вікна у рядок товару та перерахунок підсумків
    if (btnSavePayShip) {
        btnSavePayShip.addEventListener('click', () => {
            if (!activeProductRow) return;

            const rows = payShipTableBody.querySelectorAll('tr');
            let records = [];
            let totalPay = 0;
            let totalShip = 0;

            rows.forEach(tr => {
                const payDate = tr.querySelector('input[name="pay-date"]').value;
                const paySum = parseFloat(tr.querySelector('input[name="pay-sum"]').value) || 0;
                const shipDate = tr.querySelector('input[name="ship-date"]').value;
                const shipSum = parseFloat(tr.querySelector('input[name="ship-sum"]').value) || 0;

                records.push({ payDate, paySum, shipDate, shipSum });

                totalPay += paySum;
                totalShip += shipSum;
            });

            // Зберігаємо масив записів у атрибуті рядка товару
            activeProductRow.setAttribute('data-pay-ship-records', JSON.stringify(records));

            // Оновлюємо відображення у головній таблиці специфікації
            const infoSpan = activeProductRow.querySelector('.payment-shipping-info');
            if (infoSpan) {
                infoSpan.textContent = `💳 ${totalPay.toFixed(2)} | 📦 ${totalShip.toFixed(2)}`;
            }

            // Додаємо виклик загального перерахунку нижньої панелі
            updateSpecificationTotals();

            modalPayShip.close();
        });
    }

    
    
        

});