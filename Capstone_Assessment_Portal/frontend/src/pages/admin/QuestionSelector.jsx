/**
 * Question Selector Page
 *
 * Responsibilities:
 * - Fetch all assessments
 * - Search assessments
 * - Select assessment to manage questions
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    FaSearch,
    FaClipboardList,
    FaListAlt,
} from "react-icons/fa";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";
import Pagination from "../../components/common/Pagination";

import { getAllQuizzes } from "../../services/quizService";

import "./QuestionSelector.css";

function QuestionSelector() {

    const navigate = useNavigate();

    const [quizzes, setQuizzes] = useState([]);

    const [searchText, setSearchText] = useState("");

    /**
     * Pagination
     */
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(6);

    const fetchQuizzes = async () => {

        try {

            const response = await getAllQuizzes();

            setQuizzes(response);

        }

        catch (error) {

            console.error(error);

        }

    };

    useEffect(() => {

        fetchQuizzes();

    }, []);

    useEffect(() => {
        setCurrentPage(1);
    }, [searchText]);

    const filteredQuizzes = quizzes.filter(

        (quiz) =>

            quiz.title
                .toLowerCase()
                .includes(searchText.toLowerCase())

    );

    /**
     * Pagination
     */
    const lastIndex = currentPage * itemsPerPage;
    const firstIndex = lastIndex - itemsPerPage;
    const currentQuizzes = filteredQuizzes.slice(
        firstIndex,
        lastIndex
    );

    return (

        <div className="question-selector-page">

            <SideBar />

            <div className="question-selector-content">

                <TopBar title="Questions" />

                <div className="question-selector-container">

                    <div className="selector-header">

                        <div>

                            <div className="selector-title">

                                <FaClipboardList />

                                <h1>

                                    Select Assessment

                                </h1>

                            </div>

                            <p>

                                Select an assessment to manage its questions.

                            </p>

                        </div>

                    </div>

                    <div className="selector-search">

                        <FaSearch />

                        <input

                            type="text"

                            placeholder="Search assessment..."

                            value={searchText}

                            onChange={(event) =>

                                setSearchText(event.target.value)

                            }

                        />

                    </div>

                    <div className="quiz-card-container">

                        {

                            currentQuizzes.map(

                                (quiz) => (

                                    <div

                                        key={quiz.id}

                                        className="quiz-card"

                                    >

                                        <div>

                                            <h2>

                                                {quiz.title}

                                            </h2>

                                            <p>

                                                {quiz.category_name}

                                            </p>

                                            <span>

                                                {quiz.total_questions} Questions

                                            </span>

                                        </div>
                                        


                                        <button

                                            className="manage-btn"

                                            onClick={() =>

                                                navigate(

                                                    `/admin/questions/${quiz.id}`

                                                )

                                            }

                                        >

                                            <FaListAlt />

                                            Manage Questions

                                        </button>

                                    </div>

                                    

                                )

                            )

                        }

                    </div>
                    <Pagination
                        currentPage={currentPage}
                        totalItems={filteredQuizzes.length}
                        itemsPerPage={itemsPerPage}
                        onPageChange={setCurrentPage}
                        onItemsPerPageChange={(value) => {
                            setItemsPerPage(value);
                            setCurrentPage(1);

                        }}

                            />

                </div>

            </div>

        </div>

    );

}

export default QuestionSelector;