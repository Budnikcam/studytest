async function registerUser(username, password) {
    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
        const error = await response.json();
        console.error('Ошибка регистрации:', error);
        return;
    }

    const data = await response.json();
    console.log('Пользователь зарегистрирован:', data);
}

// Убедитесь, что этот код выполняется после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    const facultyHeaders = document.querySelectorAll('.faculty-header');

    facultyHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const topics = this.nextElementSibling; // Получаем следующий элемент (список тем)
            // Проверяем, существует ли следующий элемент
            if (topics) {
                // Переключаем видимость
                topics.style.display = topics.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});
