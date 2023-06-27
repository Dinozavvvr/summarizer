import {useEffect, useState} from "react";
import {HOST} from "../../config/config";
import Header from "../../components/header/Header";
import {Link, useNavigate, useParams} from "react-router-dom";
import {getMenuItems} from "../../utils";
import "../collections.css"
import Document from "../../components/document/Document";

export default function CollectionAddDocumentsPage() {
    const [documents, setDocuments] = useState([]);

    const {id} = useParams();
    const navigate = useNavigate();
    const [collection, setCollection] = useState({
        documents: []
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

        const fetchData = async () => {
            try {
                const documentsData = await getUserData(token);
                setDocuments(documentsData);
            } catch (error) {
                console.error('An error occurred:', error);
            }
        };

        fetchData().then();
    }, [id, token]);

    const handleDocumentClick = (document) => {
        const documentIds = collection.documents.map(doc => doc.id);

        if (documentIds.includes(document.id)) {
            const updatedDocuments = collection.documents.filter(doc => doc.id !== document.id);
            setCollection(prevCollection => ({...prevCollection, documents: updatedDocuments}));
        } else {
            const updatedDocuments = [...collection.documents, document];
            setCollection(prevCollection => ({...prevCollection, documents: updatedDocuments}));
        }
    };

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

    const saveCollection = async () => {
        try {
            const response = await fetch(`http://${HOST}/collection/${id}/add_documents/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify(collection)
            });

            if (response.ok) {
                // alert('Успешно сохранено')
                navigate('/collection/' + collection.id)
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    }

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_title">Документы</div>
                <div className="form_field">
                    <div className="content_button" onClick={saveCollection}><span>Сохранить</span></div>
                </div>
                <div className="content_collections">
                    {documents.map((document, index) => (
                        <Document key={document.id}
                                  selected={collection.documents.map(doc => doc.id).includes(document.id)}
                                  document={document} onClick={() => handleDocumentClick(document)}/>
                    ))}
                </div>
            </div>
        </div>
    </>
}