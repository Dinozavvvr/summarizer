import Header from "../../components/header/Header";
import {getMenuItems} from "../../utils";
import {useNavigate, useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {HOST} from "../../config/config";

export default function CollectionEditPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [collection, setCollection] = useState({});
    const token = localStorage.getItem('accessToken');

    useEffect(() => {
        // Fetch the collection data based on the ID
        fetch(`http://${HOST}/collection/${id}/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
        })
            .then(response => response.json())
            .then(data => setCollection(data))
            .catch(error => console.error('An error occurred:', error));
    }, [id]);


    const handleInputChange = (event) => {
        const {name, value} = event.target;
        setCollection((prevFormData) => ({
            ...prevFormData,
            [name]: value
        }));
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        if (id === undefined) {
            try {
                const response = await fetch(`http://${HOST}/collection/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Token ' + token
                    },
                    body: JSON.stringify(collection)
                });

                if (response.ok) {
                    alert('Успешно сохранено')
                    navigate('/collection')
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        } else {
            try {
                const response = await fetch(`http://${HOST}/collection/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Token ' + token
                    },
                    body: JSON.stringify(collection)
                });

                if (response.ok) {
                    alert('Успешно сохранено')
                    navigate('/collection')
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        }
    }

    const deleteCollection = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch(`http://${HOST}/collection/${collection.id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify(collection)
            });

            if (response.ok) {
                alert('Успешно удалено')
                navigate('/collection')
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    }

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <form className="content_form form" onSubmit={handleFormSubmit}>
                    <div className="form_title">{id === undefined ? 'Создание коллекции' : 'Редактирование коллекции'}</div>
                    <div className="form_field">
                        <label htmlFor="name" className="form_label">Название</label>
                        <input id="name" name="name" className="from_input" type="text" value={collection.name} onChange={handleInputChange}/>
                    </div>
                    <div className="form_field">
                        <label htmlFor="description" className="form_label">Описание</label>
                        <textarea id="description" name="description" className="from_input from_textarea" value={collection.description} onChange={handleInputChange}></textarea>
                    </div>
                    <div className="form_field" hidden={id !== undefined}>
                        <label htmlFor="password" className="form_label">Пароль к коллекции</label>
                        <input type="password" name="password" id="password" className="from_input" value={collection.password} onChange={handleInputChange}/>
                    </div>
                    <div className="form_field">
                        <button className="content_button" type={"submit"}>Создать</button>
                    </div>
                </form>
                <br/>
                <div className="form_field" hidden={id === undefined}>
                    <button onClick={deleteCollection} className="content_button delete_button">Удалить</button>
                </div>
            </div>
        </div>
    </>
}