import Header from "../../components/header/Header";
import "./login.css"

export default function LoginPage() {
    const menuItems = [
        {path: '/login', label: 'Войти'},
        {path: '/signup', label: 'Зарегистрироваться'},
        {path: '/documents', label: 'Документы'},
        {path: '/collections', label: 'Коллекции'},
    ];

    return <>
        <Header menuItems={menuItems}/>
        <div className="content-wrapper">
            <div className="content">
                <form className="content_form form">
                    <div className="form_title">Вход</div>
                    <div className="form_field">
                        <label htmlFor="username" className="form_label">Username</label>
                        <input id="username" className="from_input" type="text"/>
                    </div>
                    <div className="form_field">
                        <label htmlFor="password" className="form_label">Пароль</label>
                        <input type="password" id="password" className="from_input"/>
                    </div>
                    <div className="form_field">
                        <button className="content_button">Войти</button>
                    </div>
                </form>
            </div>
        </div>
    </>
}