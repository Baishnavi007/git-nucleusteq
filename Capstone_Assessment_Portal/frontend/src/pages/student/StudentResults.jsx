/**
 * Student Results History
 */

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import { useEffect, useState } from "react";
import { getStudentResults } from "../../services/resultService";
import { useNavigate } from "react-router-dom";

import { FaSearch } from "react-icons/fa";

import "./StudentResults.css";


function StudentResults() {

    const [results, setResults] = useState([]);
    const [search, setSearch] = useState("");
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const filteredResults = results.filter((result) =>
    result.quiz_title
        .toLowerCase()
        .includes(search.toLowerCase())
);
    useEffect(() => {
        fetchResults();
        
    }, []);

    const fetchResults = async () => {
        try {
            const response = await getStudentResults();
            console.log("Student Results:",response)
            setResults(response);
        }
        catch(error){
            console.error(error);
        }
        finally{
            setLoading(false);
        }
    };
    if(loading){
        return <h2>Loading...</h2>
    }

    return (

        <div className="student-dashboard">

            <SideBar />

            <div className="main-content">

                <TopBar title="Results" />

                <div className="student-results-container">

                    <div className="student-results-header">

                        <h1>Learning Journey</h1>

                        <p>
                            View all your quiz attempts and scores.
                        </p>
                        <div className="results-search">

    <FaSearch className="search-icon" />

    <input
        type="text"
        placeholder="Search quiz..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
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
                    {result.quiz_title}
                </h3>

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

                        navigate(`/student/results/${result.attempt_id}`)

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

        </div>

    );

}

export default StudentResults;