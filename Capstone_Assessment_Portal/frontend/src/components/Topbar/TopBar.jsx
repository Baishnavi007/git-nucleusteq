/**
 * Admin Top Bar
 */

import {
    FaBell,
    FaUserCircle
} from "react-icons/fa";

import "./TopBar.css";

function TopBar() {

    const today = new Date().toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        }
    );

    return (

        <header className="topbar">

            <div>

                <h2>

                    Dashboard

                </h2>

                <p>

                    {today}

                </p>

            </div>

            <div className="topbar-right">

                <button className="notification-btn">

                    <FaBell />

                </button>

                <div className="profile">

                    <FaUserCircle />

                    <div>

                        <h4>

                            Admin

                        </h4>

                        <span>

                            Administrator

                        </span>

                    </div>

                </div>

            </div>

        </header>

    );

}

export default TopBar;