/**
 * Admin Results Page
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import { FaSearch } from "react-icons/fa";

import { getAllResults } from "../../services/resultService";

import "./AdminResults.css";

function AdminResults() {

    const [results, setResults] = useState([]);

    const [loading, setLoading] = useState(true);

    const [search, setSearch] = useState("");

    const navigate = useNavigate();

    useEffect(() => {

        fetchResults();

    }, []);

    const fetchResults = async () => {

        try {

            const response = await getAllResults();

            console.log("Admin Results:", response);

            setResults(response);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    };

    const filteredResults = results.filter(

        (result) =>

            result.student_name
                .toLowerCase()
                .includes(search.toLowerCase())

            ||

            result.student_email
                .toLowerCase()
                .includes(search.toLowerCase())

            ||

            result.quiz_title
                .toLowerCase()
                .includes(search.toLowerCase())

    );

    if (loading) {

        return <h2>Loading...</h2>;

    }

    return (

        <div className="admin-dashboard">

            <SideBar />

            <div className="main-content">

                <TopBar title="Results" />

                <div className="admin-results-container">

                    <div className="admin-results-header">

                        <h1>

                            Student Results

                        </h1>

                        <p>

                            View all quiz attempts submitted by students.

                        </p>

                    </div>

                    <div className="results-search">

                        <FaSearch className="search-icon" />

                        <input

                            type="text"

                            placeholder="Search by student, email or quiz..."

                            value={search}

                            onChange={(e) =>

                                setSearch(e.target.value)

                            }

                        />

                    </div>

                    <div className="results-grid">

                        {

                            filteredResults.map((result) => (

                                <div

                                    key={result.attempt_id}

                                    className="result-history-card"

                                >

                                    <h3>

                                        {result.student_name}

                                    </h3>

                                    <p>

                                        {result.student_email}

                                    </p>

                                    <h4>

                                        {result.quiz_title}

                                    </h4>

                                    <div className="history-score">

                                        {result.score} / {result.total_marks}

                                    </div>

                                    <p>

                                        Attempt #{result.attempt_number}

                                    </p>

                                    <p>

                                        {result.percentage.toFixed(0)}%

                                    </p>

                                    <p

                                        className={

                                            result.is_pass

                                                ? "pass-status"

                                                : "fail-status"

                                        }

                                    >

                                        {

                                            result.is_pass

                                                ? "Passed"

                                                : "Failed"

                                        }

                                    </p>

                                    <button

                                        className="view-result-btn"

                                        onClick={() =>

                                            navigate(

                                                `/admin/results/${result.attempt_id}`

                                            )

                                        }

                                    >

                                        View Result

                                    </button>

                                </div>

                            ))

                        }

                    </div>

                </div>

            </div>

        </div>

    );

}

export default AdminResults;