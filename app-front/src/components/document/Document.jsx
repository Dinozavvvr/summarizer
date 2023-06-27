export default function Document({document, selected, onClick}) {

    const documentClassName = selected ? 'collection selected' : 'collection';
    return <div className={documentClassName} onClick={onClick}>
        <div className="collection_icon">
            <img src={require('../../image/document.png')} alt="document"/>
        </div>
        <div className="collection_info">
            <div className="collection_title">{document.title}
            </div>
            <div className="collection_description">{document.annotation}
            </div>
        </div>
    </div>
}