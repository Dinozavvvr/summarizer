import {useNavigate} from "react-router-dom";

export default function Collection({collection}) {

    const navigate = useNavigate();

    const handleClickOnCollection = () => {
        navigate(`/collection/${collection.id}`);
    };

    return <div className="collection" onClick={handleClickOnCollection}>
        <div className="collection_icon">
            <img src={require('../../image/collection.png')} alt="collection"/>
        </div>
        <div className="collection_info">
            <div className="collection_title">{collection.name}</div>
            <div className="collection_description">{collection.description}</div>
        </div>
    </div>
};