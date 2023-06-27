import Header from "../../components/header/Header";
import {getMenuItems} from "../../utils";
import {useEffect, useState} from "react";
import {HOST} from "../../config/config";
import {useParams} from "react-router-dom";

export default function CollectionSummarizePage() {
    const {id} = useParams();
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


    const [needPassword, setNeedPassword]= useState(false)
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://${HOST}/trainee/${id}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Token ' + token
                    },
                });

                const data = await response.json();
                console.log(data);
                if (data.id === undefined) {
                    setNeedPassword(true);
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        };

        fetchData(); // Call the fetchData function
    }, [id, token]);

    const [documentId, setDocumentId] = useState('');
    const [maxLen, setMaxLen] = useState(250);
    const [password, setPassword] = useState('');

    const handleMaxLenChange = (e) => {
        setMaxLen(e.target.value)
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value)
    }


    const [annotation, setAnnotation] = useState(null);

    const annotateDocument = async () => {
        if (documentId === '') {
            alert('Документ не выбран')
        }

        setAnnotation(null)

        const summarizeObj = {
            document_id: documentId,
            password: password,
            max_len: maxLen
        }

        try {
            const response = await fetch(`http://${HOST}/trainee/${id}/summarize/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify(summarizeObj)
            });

            if (response.ok) {
                const responseData = await response.json();
                setAnnotation(responseData.text);
            }
        } catch (error) {
            console.error('An error occurred:', error);
            return null;
        }
    };

    const selectDocument = (event) => {
        const selectedDocumentId = event.target.value;
        setDocumentId(selectedDocumentId);
        console.log(selectedDocumentId);
    };


    return (
        <>
            <Header menuItems={getMenuItems()}/>
            <div className="content-wrapper">
                <div className="content">
                    <div className="content_title">Аннотирование документа</div>
                    <form className="content_form form">
                        <div className="form_field">
                            <label className="form_label">Документ</label>
                            <select
                                className="from_input form_select"
                                onChange={selectDocument}>
                                <option value="">Выберите документ</option>
                                {documents.map((document, index) => (
                                    <option key={index} value={document.id}>
                                        {document.title}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="form_field">
                            <label htmlFor="len" className="form_label">Длина</label>
                            <input id="len" name="len" className="from_input" type="text" value={maxLen}
                                   onChange={handleMaxLenChange}/>
                        </div>
                        <div className="form_field" hidden={!needPassword}>
                            <label htmlFor="password" className="form_label">Пароль</label>
                            <input id="password" name="password" className="from_input" type="password" value={password}
                                   onChange={handlePasswordChange}/>
                        </div>
                        <div className="form_field" hidden={annotation === null}><br/><br/>{annotation}</div>
                        <div className="form_field">
                            <button
                                className="content_button"
                                type={"button"}
                                onClick={annotateDocument}>
                                Аннотировать
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}