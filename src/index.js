import React from 'react';
import { createRoot } from 'react-dom/client'; // Import createRoot
import App from './App';

// Replace ReactDOM.render with createRoot
const root = createRoot(document.getElementById('root')); // Create a root
root.render(<App />); // Render your app