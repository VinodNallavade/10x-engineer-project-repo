# PromptLab Frontend

## Overview

PromptLab is a React frontend application built with Vite that interacts with the PromptLab backend APIs. This application allows users to manage prompts and collections, providing features such as CRUD operations, filtering, searching, and pagination.

## Features

- **Prompt Management**: Create, read, update, and delete prompts.
- **Collection Management**: Browse and filter prompts by collections.
- **Tag-based Filtering**: Filter prompts using tags.
- **API Health Check**: View the health status of the API.

## Tech Stack

- **Framework**: React (Vite)
- **Language**: TypeScript
- **Routing**: `react-router-dom`
- **HTTP Client**: Fetch API
- **Styling**: CSS Modules
- **State Management**: React state and custom hooks

## Project Structure

The project is organized as follows:

```
promptlab-frontend
├── src
│   ├── api                # API client and services
│   ├── components         # UI components
│   ├── hooks              # Custom hooks
│   ├── pages              # Application pages
│   ├── types              # Type definitions
│   ├── utils              # Utility functions
│   ├── styles             # CSS styles
│   ├── App.tsx            # Main application component
│   └── main.tsx           # Entry point
├── .env.example           # Environment variables example
├── .eslintrc.cjs         # ESLint configuration
├── .gitignore             # Git ignore file
├── index.html             # Main HTML file
├── package.json           # Project metadata and dependencies
├── tsconfig.json          # TypeScript configuration
├── tsconfig.node.json     # Node.js TypeScript configuration
└── vite.config.ts         # Vite configuration
```

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (Node package manager)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/SarasAI-Institute/10x-engineer-project-repo.git
   ```

2. Navigate to the frontend directory:

   ```
   cd 10x-engineer-project-repo/frontend
   ```

3. Install dependencies:

   ```
   npm install
   ```

4. Create a `.env` file based on the `.env.example`:

   ```
   cp .env.example .env
   ```

   Update the `VITE_API_BASE_URL` with your backend API URL.

### Running the Application

To start the development server, run:

```
npm run dev
```

Open your browser and navigate to `http://localhost:3000` to view the application.

### Building for Production

To build the application for production, run:

```
npm run build
```

The production files will be generated in the `dist` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.