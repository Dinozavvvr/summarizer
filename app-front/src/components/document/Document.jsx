export default function Document({document}) {
    return <div className="collection">
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