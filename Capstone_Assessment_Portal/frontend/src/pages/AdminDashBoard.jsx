/**
 * Admin Dashboard
 */

import SideBar from "../components/SideBar/SideBar";
import TopBar from "../components/Topbar/TopBar";

import "./AdminDashBoard.css";

function AdminDashboard() {

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

            </div>

        </div>

    );

}

export default AdminDashboard;