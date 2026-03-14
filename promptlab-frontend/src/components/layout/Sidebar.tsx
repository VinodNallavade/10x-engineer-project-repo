import React from 'react';
import { NavLink } from 'react-router-dom';

interface SidebarProps {
    isCollapsed?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ isCollapsed = false }) => {
    return (
        <aside className={`sidebar${isCollapsed ? ' collapsed' : ''}`}>
            <nav className="sidebar-nav" aria-label="Sidebar Navigation">
                <ul className="sidebar-nav-list">
                    <li>
                        <NavLink
                            to="/prompts"
                            end
                            aria-label="Prompts"
                            className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
                        >
                            <span className="sidebar-link-icon" aria-hidden="true">📝</span>
                            <span className="sidebar-link-label">Prompts</span>
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/collections"
                            aria-label="Collections"
                            className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
                        >
                            <span className="sidebar-link-icon" aria-hidden="true">📚</span>
                            <span className="sidebar-link-label">Collections</span>
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/health"
                            aria-label="API Health"
                            className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
                        >
                            <span className="sidebar-link-icon" aria-hidden="true">🩺</span>
                            <span className="sidebar-link-label">API Health</span>
                        </NavLink>
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default Sidebar;