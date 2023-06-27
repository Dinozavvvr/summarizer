import Header from "../../components/header/Header";
import {getMenuItems} from "../../utils";
import {Link, useNavigate, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {HOST} from "../../config/config";
import Document from "../../components/document/Document";
import TraineeResult from "../../components/collection/TraineeResult";

export default function CollectionPage() {
    const {id} = useParams();
    const navigate = useNavigate();
    const [collection, setCollection] = useState({
        documents: [],
        trainees: []
    });
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
            .then(data => {
                console.log(data)
                setCollection(data)
            })
            .catch(error => console.error('An error occurred:', error));
    }, [id]);

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_title-wrapper">
                    <div className="content_title">Коллекция обучения журнала: Известия высших учебных заведений.
                        Математика
                    </div>
                    <div className="content_title-buttons">
                        <Link className="content_title-button"
                              to={`/collection/${collection.id}/trainee`}>Обучение</Link>
                        <Link className="content_title-button"
                              to={"/collection/edit/" + collection.id}>Редактировать</Link>
                    </div>
                </div>
                <div className="content_title">Результаты обучений:</div>
                <div className="content_collections">
                    {collection.trainees.map((trainee, index) => (
                        <TraineeResult trainee={trainee} onClick={() => {
                            navigate(`/collection/${trainee.id}/summarize/`);
                        }}/>))}
                </div>
                <div className="content_title">Документы:</div>
                <div className="form_field">
                    <Link className="content_button" to={`/collection/${collection.id}/documents/`}><span>Добавить документ</span></Link>
                </div>
                <div className="content_collections">
                    {collection.documents.map((document, index) => (
                        <Document document={document} onClick={() => {
                            navigate(`/document/${document.id}`);
                        }}/>
                    ))}
                </div>
            </div>
        </div>
    </>
}