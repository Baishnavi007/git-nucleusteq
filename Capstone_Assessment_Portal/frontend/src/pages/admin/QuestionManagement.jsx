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

                        questions={questions}

                        searchText={searchText}

                        onEdit={handleEditQuestion}

                        fetchQuestions={fetchQuestions}

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