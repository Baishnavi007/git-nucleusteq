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
import StudentQuestion from "./pages/student/StudentQuestion";

import { ToastContainer} from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import StudentCategories from "./pages/student/StudentCategories";
import StudentAssessment from "./pages/student/StudentAssessment";

import StudentResult from "./pages/student/StudentResult";
import StudentResults from "./pages/student/StudentResults";

import AdminResults from "./pages/admin/AdminResults";
import AdminResult from "./pages/admin/AdminResult";

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
                element={<StudentCategories />}
            />
            <Route
                path="/student/assessments/:categoryId"
                element={<StudentAssessment />}
            />
            <Route
                path="/student/questions/:attemptId"
                element={<StudentQuestion />}
            />
            <Route
                path="/admin/assessments"
                element={<AssessmentManagement />}
            />
            <Route
                 path="/admin/questions/:quizId"
                 element={<QuestionManagement />}
            />
            <Route
                  path="/student/results"
                  element={<StudentResults />}
             />

             <Route
                  path="/student/results/:attemptId"
                  element={<StudentResult />}
            />

            <Route
                  path="/admin/results"
                  element={<AdminResults />}
            />

            <Route
                  path="/admin/results/:attemptId"
                  element={<AdminResult />}
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