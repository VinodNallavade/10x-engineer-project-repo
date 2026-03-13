import React from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import './Layout.module.css'; // Assuming you will create a CSS module for styling

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <div className="layout">
            <Header />
            <div className="main-content">
                <Sidebar />
                <main>{children}</main>
            </div>
        </div>
    );
};

export default Layout;