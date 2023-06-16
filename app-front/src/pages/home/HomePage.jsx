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
                    <Link to="/" className="content_menu__item"><span>Создать коллекцию обучения</span></Link>
                    <Link to="/" className="content_menu__item"><span>Сформировать аннотацию</span></Link>
                </div>
                <div className="content_description">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nulla massa, lobortis sit amet pretium
                    a, sagittis quis velit. Vestibulum turpis nulla, porttitor vel ex eu, consectetur fermentum massa. Ut
                    non auctor nisl, vitae euismod nisl. Nam in aliquam mi. Etiam ac pellentesque ex. Suspendisse eu congue
                    lectus. Sed non elit efficitur, iaculis urna sit amet, faucibus lorem. Aenean aliquet pretium eros.
                    Nunc non ornare nibh. Donec eget lacus et libero pellentesque consequat. Curabitur efficitur turpis ac
                    facilisis elementum. Fusce vulputate urna vitae leo pretium, ut vehicula sapien consectetur
                </div>
            </div>
        </div>
    </>
}