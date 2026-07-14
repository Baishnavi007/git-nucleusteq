/**
 * Admin Results Page
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";
import Pagination from "../../components/common/Pagination";

import { FaSearch } from "react-icons/fa";

import { getAllResults } from "../../services/resultService";

import "./AdminResults.css";

function AdminResults() {

    const [results, setResults] = useState([]);

    const [loading, setLoading] = useState(true);

    const [search, setSearch] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(6);

    const navigate = useNavigate();

    useEffect(() => {

        fetchResults();

    }, []);

    useEffect(() =>{
        setCurrentPage(1);
    },[search]);

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
    const lastIndex = currentPage * itemsPerPage;
    const firstIndex = lastIndex - itemsPerPage;
    const currentResults = filteredResults.slice(
        firstIndex,
        lastIndex
    )

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

                            currentResults.map((result) => (

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
                    <Pagination
                        currentPage={currentPage}
                        totalItems={filteredResults.length}
                        itemsPerPage={itemsPerPage}
                        onPageChange={setCurrentPage}
                        onItemsPerPageChange={(value) => {
                            setItemsPerPage(value);
                            setCurrentPage(1);
                        }} />

                </div>

            </div>

        </div>

    );

}

export default AdminResults;