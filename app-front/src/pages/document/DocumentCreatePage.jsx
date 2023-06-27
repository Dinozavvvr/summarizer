import Header from "../../components/header/Header";
import {getMenuItems} from "../../utils";
import {useEffect, useRef, useState} from "react";
import {useNavigate} from "react-router-dom";
import {HOST} from "../../config/config";

export default function DocumentCreatePage() {
    const navigate = useNavigate();
    const token = localStorage.getItem('accessToken');

    const [formData, setFormData] = useState({
        title: '',
        link: '',
        annotation: '',
        text: ''
    });

    const handleInputChange = (event) => {
        const {name, value} = event.target;
        setFormData((prevFormData) => ({
            ...prevFormData,
            [name]: value
        }));
    };


    const [preSent, setPreSent] = useState(false);
    const [buttonText, setButtonText] = useState('Далее');
    const [document, setDocument] = useState({});
    const handleFormSubmit = async (event) => {
        event.preventDefault();

        if (!preSent) {
            try {
                const response = await fetch(`http://${HOST}/downloader/upload/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Token ' + token
                    },
                    body: JSON.stringify(formData),
                });

                if (response.ok) {
                    const documentData = await response.json();
                    setPreSent(true);
                    setButtonText('Сохранить');
                    setDocument(documentData);
                    setFormData(prevFormData => ({
                        ...prevFormData,
                        text: documentData.text
                    }));
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        } else {
            try {
                const documentObj = {
                    text: formData.text,
                    title: formData.title,
                    annotation: formData.annotation,
                    commited: true
                };
                const response = await fetch(`http://${HOST}/document/${document.id}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Token ' + token
                    },
                    body: JSON.stringify(documentObj)
                });

                if (response.ok) {
                    navigate('/document');
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        }
    };

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_title">Добавление документа</div>
                <form className="content_form form" onSubmit={handleFormSubmit}>
                    <div className="form_field">
                        <label htmlFor="iteration_num" className="form_label">Заголовок</label>
                        <input id="iteration_num" className="from_input" type="text" name="title" value={formData.title}
                               onChange={handleInputChange}/>
                    </div>
                    <div className="form_field">
                        <label htmlFor="link" hidden={preSent} className="form_label">Источник</label>
                        <input id="link" name="link" className="from_input" type="text" value={formData.link}
                               onChange={handleInputChange}/>
                    </div>
                    <div className="form_field">
                        <label htmlFor="annotation" className="form_label">Аннотация</label>
                        <textarea id="annotation" name="annotation" className="from_input from_textarea"
                                  value={formData.annotation} onChange={handleInputChange}></textarea>
                    </div>
                    <div className="form_field" hidden={!preSent}>
                        <label htmlFor="text" className="form_label">Текст</label>
                        <textarea style={{height: "90vh"}} id="text" name="text" value={formData.text} onChange={handleInputChange} className="from_input from_textarea"></textarea>
                    </div>
                    <div className="form_field">
                        <button className="content_button" type={"submit"}>{buttonText}</button>
                    </div>
                </form>
            </div>
        </div>
    </>
};