function isAuthenticated() {
    return localStorage.getItem('accessToken') !== undefined
        && localStorage.getItem('accessToken') !== null
        && localStorage.getItem('accessToken') !== ""
}

function getMenuItems() {
    const authenticatedMenu = [
        {path: '/profile', label: 'Профиль'},
        {path: '/document', label: 'Документы'},
        {path: '/collection', label: 'Коллекции'},
        {path: '/logout', label: 'Выйти'},
    ];

    const notAuthenticatedMenu = [
        {path: '/login', label: 'Войти'},
        {path: '/signup', label: 'Зарегистрироваться'},
    ];

    if (isAuthenticated()) {
        return authenticatedMenu
    } else {
        return notAuthenticatedMenu
    }
}

export {isAuthenticated, getMenuItems}