import { createBrowserRouter } from 'react-router-dom'

import Home from './routes/Home'
import App from './App'
import Dashboard from './routes/Dashboard'

export const router = createBrowserRouter([
    { path: '*', element: <App /> },
    { path: '/home', element: <App /> },
    { path: '/dashboard', element: <Dashboard /> },
])
