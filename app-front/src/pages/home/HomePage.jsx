import Header from "../../components/header/Header";
import "./index.css"
import {Link} from "react-router-dom";
import {getMenuItems} from "../../utils";

export default function HomePage() {

    return <>
        <Header menuItems={getMenuItems()}/>
        <div className="content-wrapper">
            <div className="content">
                <div className="content_menu">
                    <Link to="/collection/create" className="content_menu__item"><span>Создать коллекцию обучения</span></Link>
                    <Link to="/profile" className="content_menu__item"><span>Профиль</span></Link>
                </div>
                <div className="content_description">
                    <b>Lobachevskii DML Summarization Tool</b> - это сервис автоматического аннотированния научных
                    физико-математических документов и статей, применяющий генетический алгоритм для составления
                    аннотаций. Иструмент разработан в рамках выпускной квалификационной
                    работы студентом Казанского Федерального Унивеситета (КФУ) Института Информационных Технологий и
                    Интеллектуальных систем (ИТИС) группы 11-904 Шагалиевым Динаром
                </div>
            </div>
        </div>
    </>
}