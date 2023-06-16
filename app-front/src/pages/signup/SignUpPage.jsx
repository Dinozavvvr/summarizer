import Header from "../../components/header/Header";
import "./registration.css"
import {useState} from "react";
import {HOST} from "../../config/config";
import { useNavigate } from "react-router-dom";
import {getMenuItems} from "../../utils";


export default function SignUpPage() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const userData = {
            username,
            email,
            password,
        };

        try {
            const response = await fetch(`http://${HOST}/user/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            });

            if (response.ok) {
                console.log('Registration successful');

                const data = await response.json();
                const token = data.token;

                localStorage.setItem('accessToken', token);
                navigate('/profile')
            } else {
                console.error('Registration failed');
                alert('Пожалуйста заполните поля корректно!')
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
                    <div className="form_title">Регистрация</div>
                    <div className="form_field">
                        <label htmlFor="email" className="form_label">E-mail</label>
                        <input id="email" className="from_input" type="text" value={email}
                               onChange={handleEmailChange}/>
                    </div>
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
                        <button className="content_button" type="submit">Зарегистрироваться</button>
                    </div>
                </form>
            </div>
        </div>
    </>
}