import React from 'react';
import { Link } from 'react-router-dom';
import './Header.module.css'; // Assuming you will use CSS Modules for styling

const Header: React.FC = () => {
    return (
        <header className="header">
            <div className="logo">
                <Link to="/">PromptLab</Link>
            </div>
            <nav className="navigation">
                <ul>
                    <li>
                        <Link to="/prompts">Prompts</Link>
                    </li>
                    <li>
                        <Link to="/collections">Collections</Link>
                    </li>
                    <li>
                        <Link to="/health">Health</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;