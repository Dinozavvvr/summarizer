import Header from "../components/Header";

export default function HomePage() {
    const menuItems = [
        { path: '/login', label: 'Войти' },
        { path: '/documents', label: 'Документы' },
        { path: '/collections', label: 'Коллекции' },
    ];

    return <>
        <Header menuItems={menuItems}/>
    </>
}