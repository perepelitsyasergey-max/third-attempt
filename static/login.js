document.getElementById('login-form').addEventListener('submit', async(event) => {
    event.preventDefault();

    
    // 1. Крок
    const userNameValue = document.getElementById('user-name').value;
    const userPasswordValue = document.getElementById('user-password').value;

    // 2. Крок
    const dataToSend = {
        userName: userNameValue,
        userPassword: userPasswordValue
    };

    // 3. Крок
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    });

    // 4. Крок
    const result = await response.json();
    
    if (result.success){
        window.location.href = '/dashboard';
    } else {
        alert(result.message);
    }

});