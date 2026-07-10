/**
 * Assessment Management Page
 *
 * Responsibilities:
 * - Fetch all quizzes
 * - Display quizzes
 * - Search quizzes
 * - Open add/edit drawer
 */

import { useEffect, useState } from "react";

import {
    FaClipboardList,
    FaPlus,
    FaSearch
} from "react-icons/fa";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import AssessmentList from "../../components/assessment/AssessmentList";
import AssessmentForm from "../../components/assessment/AssessmentForm";

import {
    getAllQuizzes
} from "../../services/quizService";

import "./AssessmentManagement.css";

function AssessmentManagement() {

    /**
     * Stores all quizzes.
     */
    const [quizzes, setQuizzes] = useState([]);

    /**
     * Stores search text.
     */
    const [searchText, setSearchText] = useState("");

    /**
     * Controls drawer visibility.
     */
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    /**
     * Stores selected quiz while editing.
     */
    const [selectedQuiz, setSelectedQuiz] = useState(null);

    /**
     * Fetch all quizzes.
     */
    const fetchQuizzes = async () => {

        try {

            const response = await getAllQuizzes();

            setQuizzes(response);

        }

        catch (error) {

            console.error(

                "Failed to fetch quizzes.",

                error

            );

        }

    };

    /**
     * Load quizzes.
     */
    useEffect(() => {

        fetchQuizzes();

    }, []);

    /**
     * Open drawer for creating quiz.
     */
    const handleAddQuiz = () => {

        setSelectedQuiz(null);

        setIsDrawerOpen(true);

    };

    /**
     * Open drawer for editing quiz.
     */
    const handleEditQuiz = (quiz) => {

        setSelectedQuiz(quiz);

        setIsDrawerOpen(true);

    };

    /**
     * Close drawer.
     */
    const handleCloseDrawer = () => {

        setSelectedQuiz(null);

        setIsDrawerOpen(false);

    };

    return (

        <div className="assessment-page">

            <SideBar />

            <div className="assessment-content">

                <TopBar />

                <div className="assessment-container">

                    {/* Header */}

                    <div className="assessment-header">

                        <div>

                            <div className="page-title">

                                <FaClipboardList />

                                <h1>

                                    Assessment Management

                                </h1>

                            </div>

                            <p>

                                Create and manage quizzes.

                            </p>

                        </div>

                        <button
                            className="add-assessment-btn"
                            onClick={handleAddQuiz}
                        >

                            <FaPlus />

                            Add Assessment

                        </button>

                    </div>

                    {/* Search */}

                    <div className="search-box">

                        <FaSearch />

                        <input
                            type="text"
                            placeholder="Search assessment..."
                            value={searchText}
                            onChange={(event) =>
                                setSearchText(
                                    event.target.value
                                )
                            }
                        />

                    </div>

                    {/* Assessment Table */}

                    <AssessmentList
                        quizzes={quizzes}
                        searchText={searchText}
                        onEdit={handleEditQuiz}
                        fetchQuizzes={fetchQuizzes}
                    />

                </div>

            </div>

            {

                isDrawerOpen && (

                    <AssessmentForm

                        selectedQuiz={selectedQuiz}

                        fetchQuizzes={fetchQuizzes}

                        onClose={handleCloseDrawer}

                    />

                )

            }

        </div>

    );

}

export default AssessmentManagement;