/**
 * Application Top Bar
 */

import {
    FaUserCircle
} from "react-icons/fa";

import "./TopBar.css";

function TopBar({

    title = "Dashboard"

}) {

    const today = new Date().toLocaleDateString(

        "en-IN",

        {

            weekday: "long",

            day: "numeric",

            month: "long",

            year: "numeric"

        }

    );

    const role = localStorage.getItem(

        "role"

    );

    const username = localStorage.getItem(

        "username"

    );

    return (

        <header className="topbar">

            <div>

                <h2>

                    {title}

                </h2>

                <p>

                    {today}

                </p>

            </div>

            <div className="topbar-right">

                <div className="profile">

                    <FaUserCircle />

                    <div>

                        <h4>

                            {username || "User"}

                        </h4>

                        <span>

                            {

                                role === "admin"

                                    ? "Administrator"

                                    : "Student"

                            }

                        </span>

                    </div>

                </div>

            </div>

        </header>

    );

}

export default TopBar;