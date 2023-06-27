import React, { useEffect, useState } from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {HOST} from "../../config/config";
import Header from "../../components/header/Header";
import {getMenuItems} from "../../utils";

export default function DocumentPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [document, setDocument] = useState({});
    const token = localStorage.getItem('accessToken');

    useEffect(() => {
        // Fetch the document data based on the ID
        fetch(`http://${HOST}/document/${id}/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
        })
            .then(response => response.json())
            .then(data => setDocument(data))
            .catch(error => console.error('An error occurred:', error));
    }, [id]);


    const handleInputChange = (event) => {
        const {name, value} = event.target;
        setDocument((prevFormData) => ({
            ...prevFormData,
            [name]: value
        }));
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch(`http://${HOST}/document/${document.id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify(document)
            });

            if (response.ok) {
                alert('Успешно сохранено')
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    }

    const deleteDocument = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch(`http://${HOST}/document/${document.id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify(document)
            });

            if (response.ok) {
                alert('Успешно удалено')
                navigate('/document')
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    }

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_title">Редактирование документа</div>
                <form className="content_form form" onSubmit={handleFormSubmit}>
                    <div className="form_field">
                        <label htmlFor="iteration_num" className="form_label">Заголовок</label>
                        <input id="iteration_num" className="from_input" type="text" name="title" value={document.title}
                               onChange={handleInputChange}/>
                    </div>
                    <div className="form_field">
                        <label htmlFor="annotation" className="form_label">Аннотация</label>
                        <textarea id="annotation" name="annotation" className="from_input from_textarea"
                                  value={document.annotation} onChange={handleInputChange}></textarea>
                    </div>
                    <div className="form_field">
                        <label htmlFor="text" className="form_label">Текст</label>
                        <textarea style={{height: "90vh"}} id="text" name="text" value={document.text} onChange={handleInputChange} className="from_input from_textarea"></textarea>
                    </div>
                    <div className="form_field">
                        <button className="content_button" type={"submit"}>Сохранить</button>
                    </div>
                </form>
                <br/>
                <div className="form_field">
                    <button onClick={deleteDocument} className="content_button delete_button">Удалить</button>
                </div>
            </div>
        </div>
    </>
}