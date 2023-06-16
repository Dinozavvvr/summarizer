import {Link} from "react-router-dom";

export default function Header({menuItems}) {
    return <div className="header-wrapper">
        <header className="header">
            <div className="header_content">
                <div className="header_logo-wrapper">
                    <div className="header_logo">
                        <div className="header_logo__title">
                            <Link to="/">Summarization Tool</Link>
                        </div>
                        <div className="header_logo__subtitle">
                            Lobachevskii Digital Mathematics Library
                        </div>
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