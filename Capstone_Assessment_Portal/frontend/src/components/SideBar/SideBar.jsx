/**
 * Admin Sidebar
 */

import { NavLink } from "react-router-dom";

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

    const menuItems = [

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

    ];

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

                            Admin Portal

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
            >

                <FaSignOutAlt />

                Logout

            </button>

        </aside>

    );

}

export default SideBar;