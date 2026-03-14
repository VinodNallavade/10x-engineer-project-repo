import React from 'react';
import { Link } from 'react-router-dom';
import './Header.module.css'; // Assuming you will use CSS Modules for styling

const Header: React.FC = () => {
    return (
        <header className="header">
            <div className="logo">
                <Link to="/" aria-label="PromptLab Home">
                    <span className="logo-mark" aria-hidden="true">
                        <svg viewBox="0 0 48 48" role="img" focusable="false">
                            <rect x="4" y="6" width="32" height="26" rx="7" fill="currentColor" />
                            <path d="M14 18h12M14 23h16" stroke="#7c3aed" strokeWidth="3" strokeLinecap="round" />
                            <path d="M18 32l-1 8 8-8" fill="currentColor" />
                            <circle cx="37" cy="13" r="7" fill="#c4b5fd" />
                            <path d="M37 8.8v8.4M32.8 13h8.4" stroke="#5b21b6" strokeWidth="2" strokeLinecap="round" />
                        </svg>
                    </span>
                    <span className="logo-text-wrap">
                        <span className="logo-text">PromptLab</span>
                        <span className="logo-subtext">AI Prompt Workspace</span>
                    </span>
                </Link>
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