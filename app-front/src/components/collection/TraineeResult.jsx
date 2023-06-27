export default function TraineeResult({trainee, onClick}) {
    if (trainee.score !== null) {
        let weightMap = {};
        weightMap = JSON.parse(trainee.weights);
        console.log(weightMap)


        return (
            <div className="collection" onClick={onClick}>
                <div className="collection_info">
                    <div className="collection_title">id: {trainee.id} | Score: {trainee.score}</div>
                    <div className="collection_description">
                        {trainee.metrics.map((metric, index) => (
                            <div key={metric.id}>
                                {metric.name} - {weightMap[metric.id]}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="collection" onClick={onClick}>
                <div className="collection_info">
                    <div className="collection_title">id: {trainee.id} | Обучение...
                    </div>
                </div>
            </div>
        );
    }
}