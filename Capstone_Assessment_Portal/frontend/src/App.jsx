/**
 * Application Routes
 */

import { Routes, Route } from "react-router-dom";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import StudentDashboard from "./pages/student/StudentDashboard";
import AdminDashBoard from "./pages/admin/AdminDashBoard";
import CategoryManagement from "./pages/admin/CategoryManagement";

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