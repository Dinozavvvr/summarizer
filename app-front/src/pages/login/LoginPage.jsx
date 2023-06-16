import Header from "../../components/header/Header";
import "./login.css"
import {useNavigate} from "react-router-dom";
import {useState} from "react";
import {HOST} from "../../config/config";
import {getMenuItems} from "../../utils";

export default function LoginPage() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const userData = {
            username,
            password,
        };

        try {
            const response = await fetch(`http://${HOST}/user/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            });

            if (response.ok) {
                console.log('Login successful');

                const data = await response.json();
                const token = data.token;

                localStorage.setItem('accessToken', token);
                navigate('/profile')
            } else {
                console.error('Login failed');
                alert('Неверный username или пароль')
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    }

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <form className="content_form form" onSubmit={handleSubmit}>
                    <div className="form_title">Вход</div>
                    <div className="form_field">
                        <label htmlFor="username" className="form_label">Username</label>
                        <input id="username" className="from_input" type="text" value={username}
                               onChange={handleUsernameChange}/>
                    </div>
                    <div className="form_field">
                        <label htmlFor="password" className="form_label">Пароль</label>
                        <input type="password" id="password" className="from_input" value={password}
                               onChange={handlePasswordChange}/>
                    </div>
                    <div className="form_field">
                        <button className="content_button" type={"submit"}>Войти</button>
                    </div>
                </form>
            </div>
        </div>
    </>
}