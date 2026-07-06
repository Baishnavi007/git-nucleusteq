/**
 * Sidebar
 */

import { NavLink, useNavigate } from "react-router-dom";

import {
    FaHome,
    FaFolderOpen,
    FaClipboardList,
    FaQuestionCircle,
    FaChartBar,
    FaSignOutAlt,
    FaGraduationCap
} from "react-icons/fa";

import "./SideBar.css";

function SideBar() {

    const navigate = useNavigate();

    const role = localStorage.getItem("role");

    const isAdmin = role === "admin";

    const menuItems = isAdmin
        ? [
            {
                title: "Dashboard",
                icon: <FaHome />,
                path: "/admin/dashboard"
            },
            {
                title: "Categories",
                icon: <FaFolderOpen />,
                path: "/admin/categories"
            },
            {
                title: "Assessments",
                icon: <FaClipboardList />,
                path: "/admin/assessments"
            },
            {
                title: "Questions",
                icon: <FaQuestionCircle />,
                path: "/admin/questions"
            },
            {
                title: "Results",
                icon: <FaChartBar />,
                path: "/admin/results"
            }
        ]
        : [
            {
                title: "Dashboard",
                icon: <FaHome />,
                path: "/student/dashboard"
            },
            {
                title: "Categories",
                icon: <FaFolderOpen />,
                path: "/student/categories"
            },
            {
                title: "Results",
                icon: <FaChartBar />,
                path: "/student/results"
            }
        ];

    /**
     * Logout current user.
     */
    const handleLogout = () => {

        localStorage.removeItem("access_token");

        localStorage.removeItem("refresh_token");

        localStorage.removeItem("role");

        navigate("/", {
            replace: true
        });

    };

    return (

        <aside className="sidebar">

            <div>

                <div className="sidebar-logo">

                    <div className="logo-circle">

                        <FaGraduationCap />

                    </div>

                    <div>

                        <h2>

                            Assessment

                        </h2>

                        <span>

                            {
                                isAdmin
                                    ? "Admin Portal"
                                    : "Student Portal"
                            }

                        </span>

                    </div>

                </div>

                <nav className="sidebar-menu">

                    {

                        menuItems.map((item) => (

                            <NavLink
                                key={item.title}
                                to={item.path}
                                className={({ isActive }) =>
                                    isActive
                                        ? "menu-item active"
                                        : "menu-item"
                                }
                            >

                                <span className="menu-icon">

                                    {item.icon}

                                </span>

                                <span>

                                    {item.title}

                                </span>

                            </NavLink>

                        ))

                    }

                </nav>

            </div>

            <button
                className="logout-button"
                onClick={handleLogout}
            >

                <FaSignOutAlt />

                Logout

            </button>

        </aside>

    );

}

export default SideBar;