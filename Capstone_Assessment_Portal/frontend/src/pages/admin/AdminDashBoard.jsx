/**
 * Admin Dashboard
 */
import { useEffect, useState } from "react";
import { getAllCategories } from "../../services/categoryService";
import { getAllQuizzes } from "../../services/quizService";
import { getAllResults } from "../../services/resultService";
import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import "./AdminDashBoard.css";
import { FaFolderOpen, FaClipboardList, FaChartBar } from "react-icons/fa";
function AdminDashboard() {

    const [categoryCount, setCategoryCount] = useState(0);
    const [quizCount, setQuizCount] = useState(0);
    const [attemptCount, setAttemptCount] = useState(0);
    useEffect(() => {
        const fetchDashboardData = async () => {
            try{
                const categories = await getAllCategories();
                const quizzes = await getAllQuizzes();
                const results = await getAllResults();
                setCategoryCount(categories.length);
                setQuizCount(quizzes.length);
                setAttemptCount(results.length);
            }
            catch (error){
                console.error("Failed to load dashboard data",
                error
                );
            }
        };
        fetchDashboardData();
    },[]);

    return (

        <div className="admin-dashboard">

            <SideBar />

            <div className="dashboard-content">

                <TopBar />

                <div className="dashboard-body">

                    <h1>
                        Welcome Back, Admin 👋
                    </h1>

                    <p>
                        Manage categories, assessments,
                        questions and monitor portal statistics.
                    </p>

                </div>
                <div className="stats-container">
                    <div className="stat-card">
                        <div className="stat-icon">
                            <FaFolderOpen />
                        </div>
                        <h3>Categories</h3>
                        <h2>{categoryCount}</h2>
                    </div>
                    <div className="stat-card">
                        <div className="stat-icon">
                            <FaClipboardList />
                        </div>
                        <h3>Total Quizzes</h3>
                        <h2>{quizCount}</h2>
                    </div>
                    <div className="stat-card">
                        <div className="stat-icon">
                            <FaChartBar />
                        </div>
                        <h3>Attempts</h3>
                        <h2>{attemptCount}</h2>
                    </div>
                </div>

            </div>

        </div>

    );

}

export default AdminDashboard;