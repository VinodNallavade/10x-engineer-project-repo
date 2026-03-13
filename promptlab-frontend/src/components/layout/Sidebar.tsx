import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar: React.FC = () => {
    return (
        <aside className="sidebar">
            <nav>
                <ul>
                    <li>
                        <Link to="/prompts">Prompts</Link>
                    </li>
                    <li>
                        <Link to="/collections">Collections</Link>
                    </li>
                    <li>
                        <Link to="/health">API Health</Link>
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default Sidebar;