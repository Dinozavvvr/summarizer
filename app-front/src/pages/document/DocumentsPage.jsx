import {useEffect, useState} from "react";
import {HOST} from "../../config/config";
import Header from "../../components/header/Header";
import {Link, useNavigate} from "react-router-dom";
import {getMenuItems} from "../../utils";
import "../collections.css"
import Document from "../../components/document/Document";

export default function DocumentsPage() {
    const [documents, setDocuments] = useState([]);

    const token = localStorage.getItem('accessToken');
    useEffect(() => {
        const fetchData = async () => {
            try {
                const documentsData = await getUserData(token);
                setDocuments(documentsData);
            } catch (error) {
                console.error('An error occurred:', error);
            }
        };

        fetchData().then();
    }, [token]);

    async function getUserData(token) {
        try {
            const response = await fetch(`http://${HOST}/document/`, {
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

    const navigate = useNavigate();

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_title">Мои документы</div>
                <div className="form_field">
                    <Link className="content_button" to={"/document/create"}><span>Добавить документ</span></Link>
                </div>
                <div className="content_collections">
                    {documents.map((document, index) => (
                        <Document document={document} onClick={() => {
                            navigate(`/document/${document.id}`);
                        }}/>
                    ))}
                </div>
            </div>
        </div>
    </>
}