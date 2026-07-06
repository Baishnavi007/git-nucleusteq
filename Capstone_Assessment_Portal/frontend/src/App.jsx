/**
 * Application Routes
 */

import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import StudentDashboard from "./pages/StudentDashboard";
import AdminDashBoard from "./pages/AdminDashBoard";
import CategoryManagement from "./pages/CategoryManagement";

function App() {

    return (

        <Routes>

            <Route
                path="/"
                element={<Login />}
            />

            <Route
                path="/register"
                element={<Register />}
            />

            <Route
                path="/student/dashboard"
                element={<StudentDashboard />}
            />

            <Route
                path="/admin/dashboard"
                element={<AdminDashBoard />}
            />

            <Route
                path="/admin/categories"
                element={<CategoryManagement />}
            />
            <Route
                path="/student/categories"
                element={<CategoryManagement />}
            />

        </Routes>

    );

}

export default App;