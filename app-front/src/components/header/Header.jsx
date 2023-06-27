import {Link} from "react-router-dom";
import "./header.css"

export default function Header({menuItems}) {
    return <div className="header-wrapper">
        <header className="header">
            <div className="header_content">
                <div className="header_logo-wrapper">
                    <div className="header_logo">
                        <div className="header_logo__title">
                            <Link to="/">Summarization Tool</Link>
                        </div>
                        <Link className="header_logo__subtitle" to="https://lobachevskii-dml.ru/">Lobachevskii Digital Mathematics Library</Link>
                    </div>
                </div>
                <div className="header_menu-wrapper">
                    <div className="header_menu">
                        {menuItems.map((menuItem, index) => (
                            <Link key={index}
                                  to={menuItem.path}
                                  className="header_menu__item">
                                <span>{menuItem.label}</span>
                            </Link>
                        ))}
                    </div>
                </div>
            </div>
        </header>
    </div>
}