/**
 * Application Routes
 */

import { Routes, Route } from "react-router-dom";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import StudentDashboard from "./pages/student/StudentDashboard";
import AdminDashBoard from "./pages/admin/AdminDashBoard";
import CategoryManagement from "./pages/admin/CategoryManagement";
import AssessmentManagement from "./pages/admin/AssessmentManagement";
import QuestionManagement from "./pages/admin/QuestionManagement";

import { ToastContainer} from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
function App() {

    return (
        <>

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
            <Route
                path="/admin/assessments"
                element={<AssessmentManagement />}
            />
            <Route
                 path="/admin/questions/:quizId"
                 element={<QuestionManagement />}
            />

        </Routes>

        <ToastContainer
            position="top-right"
            autoClose={3000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            pauseOnHover
            draggable
            theme="colored"
            />
        </>

    );

}

export default App;