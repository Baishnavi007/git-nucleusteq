/**
 * Student Dashboard
 */

import { useNavigate } from "react-router-dom";

import {
    FaBook,
    FaFolderOpen,
    FaArrowRight
} from "react-icons/fa";

import SideBar from "../components/Sidebar/SideBar";
import TopBar from "../components/Topbar/TopBar";

import "./StudentDashboard.css";

function StudentDashboard() {

    const navigate = useNavigate();

    return (

        <div className="dashboard-page">

            <SideBar />

            <div className="dashboard-content">

                <TopBar />

                <div className="dashboard-container">

                    <div className="dashboard-header">

                        <h1>

                            Welcome Student 👋

                        </h1>

                        <p>

                            Browse available categories and start your learning journey.

                        </p>

                    </div>

                    <div className="dashboard-card">

                        <div className="card-icon">

                            <FaFolderOpen />

                        </div>

                        <div className="card-content">

                            <h2>

                                Categories

                            </h2>

                            <p>

                                Explore all available assessment categories.

                            </p>

                        </div>

                        <button
                            className="dashboard-btn"
                            onClick={() =>
                                navigate("/student/categories")
                            }
                        >

                            Browse

                            <FaArrowRight />

                        </button>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default StudentDashboard;