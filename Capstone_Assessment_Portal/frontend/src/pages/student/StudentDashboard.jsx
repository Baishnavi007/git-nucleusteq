/**
 * Student Dashboard
 */
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    FaFolderOpen,
    FaClipboardList,
    FaChartLine
} from "react-icons/fa";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import {
    getAllCategories
} from "../../services/categoryService";

import {
    getPublishedQuizzesByCategory
} from "../../services/quizService";

import {
    getStudentResults
} from "../../services/resultService";

import "./StudentDashboard.css";

function StudentDashboard() {

    const navigate = useNavigate();

    const username = localStorage.getItem("username");

    const [stats, setStats] = useState({
        categories: 0,
        quizzes: 0,
        attempts: 0,
        averageScore: 0
    });

    const[recentAttempts, setRecentAttempts] = useState([]);

    useEffect(() => {

        const fetchDashboardStats = async () => {

            try {

                const categories = await getAllCategories();

                let publishedQuizCount = 0;

                for (const category of categories) {

                    const quizzes =
                        await getPublishedQuizzesByCategory(category.id);

                    publishedQuizCount += quizzes.length;
                }

                const attempts = await getStudentResults();
                const averageScore =
                    attempts.length > 0
                    ?(
                        attempts.reduce(
                            (sum, item) =>
                                sum + item.percentage,
                                0
                            )/attempts.length
                    ).toFixed(1)
                    :0;
                
                const recent = [...attempts]
                     .sort(
                        (a,b) =>
                            new Date(b.submitted_at)-
                            new Date(a.submitted_at)
                    
                     )
                     .slice(0,5);

                setStats({

                    categories: categories.length,

                    quizzes: publishedQuizCount,

                    attempts: attempts.length,

                    averageScore

                });
            setRecentAttempts(recent);

            }

            catch (error) {

                console.error(error);

            }

        };

        fetchDashboardStats();

    }, []);

    return (

        <div className="dashboard-page">

            <SideBar />

            <div className="dashboard-content">

                <TopBar title="Dashboard" />

                <div className="dashboard-container">

                    <div className="dashboard-header">

                        <h1>

                            Welcome {username} 👋

                        </h1>

                        <p>

                            Access categories, attempt quizzes, and track your assessment performance.

                        </p>

                    </div>

                    <div className="dashboard-stats">

    <div
        className="stat-card"
        onClick={() => navigate("/student/categories")}
    >

        <div className="stat-icon">

            <FaFolderOpen />

        </div>
        <div className="stat-info">
            <h3>
                Categories
            </h3>
            <h2>
                {stats.categories}
            </h2>
        </div>

    </div>

    <div
        className="stat-card"
        onClick={() => navigate("/student/categories")}
    >

        <div className="stat-icon">

            <FaClipboardList />

        </div>

        <div className="info">
            <h3>
                Published Quizzes
            </h3>

           <h2>

               {stats.quizzes}

            </h2>

        </div>    

    </div>

    <div
        className="stat-card"
        onClick={() => navigate("/student/results")}
    >

        <div className="stat-icon">

            <FaChartLine />

        </div>

        <div className="stat-info">
            <h3>
                My Attempts
            </h3>
            <h2>

                {stats.attempts}
            </h2>
        </div>

    </div>

    <div
        className="stat-card"
        onClick={() => navigate("/student/results")}
    >

        <div className="stat-icon">

            ⭐

        </div>

        <div className="stat-info">
            <h3>
                Average Score
            </h3>

            <h2>
                {stats.averageScore}
            </h2>

        </div>

        

    </div>

</div>

<div className="recent-activity">

    <h2>

        Recent Activity

    </h2>

    {

        recentAttempts.length === 0 ? (

            <p>

                No quiz attempts yet.

            </p>

        ) : (

            recentAttempts.map((attempt) => (

                <div
                    key={attempt.attempt_id}
                    className="activity-row"
                >

                    <div>

                        <strong>

                            {attempt.quiz_title}

                        </strong>

                        <p>

                            Attempt {attempt.attempt_number}

                        </p>

                    </div>

                    <div className="activity-score">

                        {attempt.percentage}%

                    </div>

                </div>

            ))

        )

    }

</div>

                </div>

            </div>

        </div>

    );

}

export default StudentDashboard;