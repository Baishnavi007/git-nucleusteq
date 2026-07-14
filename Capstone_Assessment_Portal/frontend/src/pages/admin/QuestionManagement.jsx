/**
 * Question Management Page
 *
 * Responsibilities:
 * - Fetch all questions of a quiz
 * - Display questions
 * - Search questions
 * - Open add/edit drawer
 */

import { useEffect, useState } from "react";

import {
    useParams
} from "react-router-dom";

import {
    FaQuestionCircle,
    FaPlus,
    FaSearch
} from "react-icons/fa";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import QuestionList from "../../components/question/QuestionList";
import QuestionForm from "../../components/question/QuestionForm";
import Pagination from "../../components/common/Pagination";

import {

    getQuestionsByQuiz

} from "../../services/questionService";

import "./QuestionManagement.css";

function QuestionManagement() {

    /**
     * Quiz Id from URL.
     */
    const { quizId } = useParams();

    /**
     * Stores all questions.
     */
    const [questions, setQuestions] = useState([]);

    /**
     * Search text.
     */
    const [searchText, setSearchText] = useState("");

    /**
     * Drawer visibility.
     */
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    /**
     * Selected question.
     */
    const [selectedQuestion, setSelectedQuestion] = useState(null);

    /**
     * Pagination
     */
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(5);

    /**
     * Fetch questions.
     */
    const fetchQuestions = async () => {

        try {

            const response = await getQuestionsByQuiz(

                quizId

            );

            setQuestions(

                response

            );

        }

        catch (error) {

            console.error(

                "Failed to fetch questions.",

                error

            );

        }

    };

    /**
     * Load questions.
     */
    useEffect(() => {

        fetchQuestions();

    }, []);

    useEffect(() => {
        setCurrentPage(1);
    }, [searchText]);

    /**
     * Open add drawer.
     */
    const handleAddQuestion = () => {

        setSelectedQuestion(null);

        setIsDrawerOpen(true);

    };

    /**
     * Open edit drawer.
     */
    const handleEditQuestion = (question) => {

        setSelectedQuestion(question);

        setIsDrawerOpen(true);

    };

    /**
     * Close drawer.
     */
    const handleCloseDrawer = () => {

        setSelectedQuestion(null);

        setIsDrawerOpen(false);

    };
    /**
     * Filter questions according to search.
     */
    const filteredQuestions = questions.filter(
        (question) =>
            question.question
                .toLowerCase()
                .includes(
                    searchText.toLowerCase()
                )

    );

    /**
     * Pagination
     */
    const lastIndex = currentPage * itemsPerPage;
    const firstIndex = lastIndex - itemsPerPage;
    const currentQuestions = filteredQuestions.slice(
        firstIndex,
        lastIndex
    );



    return (

        <div className="question-page">

            <SideBar />

            <div className="question-content">

                <TopBar title="Questions" />

                <div className="question-container">

                    {/* Header */}

                    <div className="question-header">

                        <div>

                            <div className="page-title">

                                <FaQuestionCircle />

                                <h1>

                                    Question Management

                                </h1>

                            </div>

                            <p>

                                Create and manage questions.

                            </p>

                        </div>

                        <button

                            className="add-question-btn"

                            onClick={handleAddQuestion}

                        >

                            <FaPlus />

                            Add Question

                        </button>

                    </div>

                    {/* Search */}

                    <div className="search-box">

                        <FaSearch />

                        <input

                            type="text"

                            placeholder="Search question..."

                            value={searchText}

                            onChange={(event) =>

                                setSearchText(

                                    event.target.value

                                )

                            }

                        />

                    </div>

                    <QuestionList

                        questions={currentQuestions}

                        onEdit={handleEditQuestion}

                        fetchQuestions={fetchQuestions}

                    />
                    <Pagination
                        currentPage={currentPage}
                        totalItems={filteredQuestions.length}
                        itemsPerPage={itemsPerPage}
                        onPageChange={setCurrentPage}
                        onItemsPerPageChange={(value) => {
                            setItemsPerPage(value);
                            setCurrentPage(1);

                        }}
                        />

                </div>

            </div>

            {

                isDrawerOpen && (

                    <QuestionForm

                        quizId={quizId}

                        selectedQuestion={selectedQuestion}

                        fetchQuestions={fetchQuestions}

                        onClose={handleCloseDrawer}

                    />

                )

            }

        </div>

    );

}

export default QuestionManagement;