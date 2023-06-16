import Header from "../../components/header/Header";
import {Link} from "react-router-dom";
import {getMenuItems} from "../../utils";
import {useEffect, useState} from "react";
import {HOST} from "../../config/config";

import "./profile.css"

export default function ProfilePage() {
    const [user, setUser] = useState({});

    const token = localStorage.getItem('accessToken');
    useEffect(() => {
        const fetchData = async () => {
            try {
                const userData = await getUserData(token);
                setUser(userData);
            } catch (error) {
                console.error('An error occurred:', error);
            }
        };

        fetchData().then();
    }, [token]);

    async function getUserData(token) {
        try {
            const response = await fetch(`http://${HOST}/user/me/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
            });

            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('An error occurred:', error);
            return null;
        }
    }

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_profile profile">
                    <div className="profile_username">{user.username}</div>
                    <div className="profile_email">{user.email}</div>
                </div>
                <div className="content_profile_menu">
                    <Link to={"/document"} className="content_menu__item"><span>Мои документы</span></Link>
                    <Link to={"/collection"} className="content_menu__item"><span>Мои коллекции</span></Link>
                    <Link to={"/logout"} className="content_button"><span>Выйти</span></Link>
                </div>
            </div>
        </div>
    </>
}