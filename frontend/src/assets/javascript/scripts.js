document.addEventListener('DOMContentLoaded', function() {
    const authenticatedSection = document.getElementById('authenticated-section');
    const adminSection = document.getElementById('admin-section');

    checkAuthStatus();

    function checkAuthStatus() {
        fetch('http://localhost:5001/users/check_auth', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token') // Предполагается, что токен хранится в localStorage
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.isAuthenticated) {
                showAuthenticatedContent();
                if (data.isAdmin) {
                    showAdminContent();
                }
            } else {
                showUnauthenticatedContent();
            }
        })
        .catch(error => {
            console.error('Ошибка при проверке авторизации:', error);
            showUnauthenticatedContent();
        });
    }

    function showAuthenticatedContent() {
        document.querySelector('nav ul li:nth-child(2) a').textContent = 'Мой аккаунт';
        authenticatedSection.style.display = 'block';
    }

    function showUnauthenticatedContent() {
        authenticatedSection.style.display = 'none';
    }

    function showAdminContent() {
        document.querySelector('nav ul li:nth-child(3) a').textContent = 'Админ панель';
        adminSection.style.display = 'block';
    }
});