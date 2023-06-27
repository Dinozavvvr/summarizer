import Header from "../../components/header/Header";
import {getMenuItems} from "../../utils";
import {useEffect, useState} from "react";
import {HOST} from "../../config/config";
import {useNavigate, useParams} from "react-router-dom";

export default function CollectionTraineePage() {
    const [metrics, setMetrics] = useState([]);
    const token = localStorage.getItem('accessToken');
    const [iterationCount, setIterationCount] = useState(10000)
    const [popSize, setPopSize] = useState(10)
    const [traineeMetrics, setTraineeMetrics] = useState([])

    useEffect(() => {
        // Fetch the collection data based on the ID
        fetch(`http://${HOST}/metric/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
        })
            .then(response => response.json())
            .then(data => {
                setMetrics(data);
                setTraineeMetrics(data.map(metric => metric.id));
            })
            .catch(error => console.error('An error occurred:', error));
    }, []);

    const { id } = useParams();
    const navigate = useNavigate();
    const [collection, setCollection] = useState({});

    useEffect(() => {
        // Fetch the collection data based on the ID
        fetch(`http://${HOST}/collection/${id}/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
        })
            .then(response => response.json())
            .then(data => setCollection(data))
            .catch(error => console.error('An error occurred:', error));
    }, [id]);

    const handleIterationCountChange = (e) => {
        setIterationCount(e.target.value);
    };

    const handlePopSizeChange = (e) => {
        setPopSize(e.target.value);
    };

    const handleClickOnMetric = (e, metricId) => {
        const isChecked = e.target.checked;

        if (isChecked) {
            // Add metric to traineeMetrics
            setTraineeMetrics(prevMetrics => [...prevMetrics, metricId]);
        } else {
            // Remove metric from traineeMetrics
            setTraineeMetrics(prevMetrics => prevMetrics.filter(id => id !== metricId));
        }
    };

    const startTrainee = async (e) => {
        e.preventDefault()

        if (traineeMetrics.length === 0) {
            alert("Выберите как минимум одну метрику")
            return;
        }

        const traineeData = {
            'population_size': popSize,
            'iteration_count': iterationCount,
            'metrics': traineeMetrics
        }

        try {
            alert('Обучение начато. Результаты обучения через некоторое время появятся на странице коллеции')
            fetch(`http://${HOST}/collection/${collection.id}/traine/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify(traineeData)
            });
            navigate('/collection/' + collection.id)
        } catch (error) {
            console.error('An error occurred:', error);
        }
    }

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_title">Обучение:</div>
                <div className="content_title">{collection.name}</div>
                <form className="content_form form">
                    <div className="form_field">
                        <label htmlFor="iteration_num" className="form_label">Количество итераций</label>
                        <input id="iteration_num" className="from_input" type="number" value={iterationCount} onChange={handleIterationCountChange}/>
                    </div>
                    <div className="form_field">
                        <label htmlFor="population_size" className="form_label">Размер популяции</label>
                        <input id="population_size" className="from_input" type="number" value={popSize} onChange={handlePopSizeChange}/>
                    </div>
                    <div className="form_field">
                        <label className="form_label">Метрики обучения</label>
                        {metrics.map((metric) => (
                            <label className="from_checkbox-label" key={metric.id}>
                                <input
                                    className="from_checkbox"
                                    type="checkbox"
                                    value={metric.id}
                                    checked={traineeMetrics.includes(metric.id)}
                                    onChange={(e) => handleClickOnMetric(e, metric.id)}
                                />
                                {metric.name}
                            </label>
                        ))}
                    </div>
                    <div className="form_field">
                        <button className="content_button" onClick={startTrainee}>Начать обучение</button>
                    </div>
                </form>
            </div>
        </div>
    </>
}