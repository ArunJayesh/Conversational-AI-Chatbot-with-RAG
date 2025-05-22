# RAG Chatbot Frontend

This is the frontend for the Conversational AI Chatbot with RAG (Retrieval Augmented Generation) project. The frontend is built with React and Material UI.

## Prerequisites

- Node.js 14+ and npm installed
- Backend server running (see backend README)

## Setup and Installation

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. The application will open in your default browser at [http://localhost:3000](http://localhost:3000)

## Features

- Chat interface for interacting with the RAG-powered chatbot
- Markdown rendering for rich text responses
- Source attribution for information retrieved
- Responsive design for desktop and mobile

## Backend Connection

The frontend connects to the backend API running on http://localhost:8000. Make sure the backend is running before using the frontend.

## Technologies Used

- React.js
- Material UI
- Axios for API requests
- React-Markdown for rendering markdown responses 