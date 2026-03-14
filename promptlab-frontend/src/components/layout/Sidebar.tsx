import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar: React.FC = () => {
    return (
        <aside className="sidebar">
            <nav className="sidebar-nav" aria-label="Sidebar Navigation">
                <ul className="sidebar-nav-list">
                    <li>
                        <NavLink to="/prompts" className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}>
                            Prompts
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/collections" className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}>
                            Collections
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/health" className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}>
                            API Health
                        </NavLink>
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default Sidebar;