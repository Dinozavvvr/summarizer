import Header from "../../components/header/Header";
import {getMenuItems} from "../../utils";
import {Link} from "react-router-dom";
import {useEffect, useState} from "react";
import {HOST} from "../../config/config";
import Collection from "../../components/collection/Collection";

export default function CollectionsPage() {

    const [collections, setCollections] = useState([]);

    const token = localStorage.getItem('accessToken');
    useEffect(() => {
        const fetchData = async () => {
            try {
                const collectionsData = await getUserData(token);
                console.log(collectionsData)
                setCollections(collectionsData);
            } catch (error) {
                console.error('An error occurred:', error);
            }
        };

        fetchData().then();
    }, [token]);

    async function getUserData(token) {
        try {
            const response = await fetch(`http://${HOST}/collection/`, {
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
                <div className="content_title">Коллекции</div>
                <div className="form_field">
                    <Link className="content_button" to={"/collection/create"}><span>Добавить коллекцию</span></Link>
                </div>
                <div className="content_collections">
                    {collections.map((collection, index) => (
                        <Collection collection={collection}/>
                    ))}
                </div>
            </div>
        </div>
    </>
};