import React, { useMemo, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';
import './Layout.module.css'; // Assuming you will create a CSS module for styling

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const location = useLocation();
    const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

    const breadcrumbItems = useMemo(() => {
        const pathSegments = location.pathname.split('/').filter(Boolean);
        const items = [{ label: 'Home', to: '/' }];

        pathSegments.forEach((segment, index) => {
            const to = `/${pathSegments.slice(0, index + 1).join('/')}`;
            const label = segment
                .split('-')
                .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
                .join(' ');
            items.push({ label, to });
        });

        return items;
    }, [location.pathname]);

    return (
        <div className="layout">
            <Header />
            <div className={`main-content${isSidebarCollapsed ? ' sidebar-collapsed' : ''}`}>
                <Sidebar isCollapsed={isSidebarCollapsed} />
                <main>
                    <div className="main-toolbar">
                        <button
                            type="button"
                            className="sidebar-toggle"
                            onClick={() => setIsSidebarCollapsed((collapsed) => !collapsed)}
                            aria-label={isSidebarCollapsed ? 'Open sidebar' : 'Collapse sidebar'}
                            title={isSidebarCollapsed ? 'Open sidebar' : 'Collapse sidebar'}
                        >
                            <span aria-hidden="true" className="sidebar-toggle-icon">
                                {isSidebarCollapsed ? '☰' : '⟨⟨'}
                            </span>
                        </button>

                        <nav className="breadcrumb" aria-label="Breadcrumb">
                            {breadcrumbItems.map((item, index) => {
                                const isLast = index === breadcrumbItems.length - 1;
                                return (
                                    <span key={item.to} className="breadcrumb-item">
                                        {isLast ? (
                                            <span>{item.label}</span>
                                        ) : (
                                            <Link to={item.to}>{item.label}</Link>
                                        )}
                                        {!isLast && <span className="breadcrumb-separator">/</span>}
                                    </span>
                                );
                            })}
                        </nav>
                    </div>

                    {children}
                </main>
            </div>
        </div>
    );
};

export default Layout;