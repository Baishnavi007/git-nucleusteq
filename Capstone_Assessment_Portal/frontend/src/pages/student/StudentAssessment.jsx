/**
 * Student Assessment Page
 */

import { useEffect, useState } from "react";

import {
    useNavigate,
    useParams,
    useLocation
} from "react-router-dom";

import {
    FaClipboardList,
    FaClock,
    FaQuestionCircle,
    FaCheckCircle,
    FaPlay
} from "react-icons/fa";

import { toast } from "react-toastify";

import { startQuizAttempt } from "../../services/quizAttemptService";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";
import Pagination from "../../components/common/Pagination";
import {
    getPublishedQuizzesByCategory
} from "../../services/quizService";

import "./StudentAssessment.css";

function StudentAssessment() {

    const navigate = useNavigate();

    const { categoryId } = useParams();

    const location = useLocation();

    const categoryName =
        location.state?.categoryName || "Assessments";

    const [quizzes, setQuizzes] = useState([]);

    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(6);

    const fetchQuizzes = async () => {

        try {

            const response =
                await getPublishedQuizzesByCategory(
                    categoryId
                );

            setQuizzes(response);
            setCurrentPage(1);

        }

        catch (error) {

            console.error(error);

        }

    };
    useEffect(() => {

        fetchQuizzes();

    }, [categoryId]);

    const lastIndex = currentPage * itemsPerPage;
    const firstIndex = lastIndex - itemsPerPage;
    const currentQuizzes = quizzes.slice(
        firstIndex,
        lastIndex
    );



    const handleStartQuiz = async (

    quiz

) => {

    try {

        const attempt = await startQuizAttempt(

            quiz.id

        );
        console.log(attempt);
        localStorage.setItem(

    "activeQuiz",

    JSON.stringify({

        duration: quiz.duration,

        startedAt: attempt.started_at,

        quizTitle: quiz.title

    })

);

        navigate(

            `/student/questions/${attempt.id}`,
            {
                state: {
                    duration: quiz.duration,
                    startedAt: attempt.started_at,
                    quizTitle: quiz.title
                }
            }

        );

    }

    catch (error) {

        toast.error(

            error.response?.data?.detail ||

            "Unable to start quiz."

        );

    }

};

    return (

        <div className="student-assessment-page">

            <SideBar />

            <div className="student-assessment-content">

                <TopBar title="Assessments" />

                <div className="student-assessment-container">

                    <div className="assessment-header">

                        <h1>

                            {categoryName}

                        </h1>

                        <p>

                            Select a quiz and begin your assessment.

                        </p>

                    </div>

                    {

                        quizzes.length === 0 ?

                        (

                            <div className="empty-box">

                                No published quizzes available.

                            </div>

                        )

                        :

                        (

                            <div className="assessment-grid">

                                {

                                    currentQuizzes.map(

                                        (quiz) => (

                                            <div

                                                key={quiz.id}

                                                className="assessment-card"

                                            >

                                                <div className="assessment-icon">

                                                    <FaClipboardList />

                                                </div>

                                                <h2>

                                                    {quiz.title}

                                                </h2>

                                                <p>

                                                    {quiz.description}

                                                </p>

                                                <div className="quiz-details">

                                                    <div>

                                                        <FaClock />

                                                        <span>

                                                            {quiz.duration} mins

                                                        </span>

                                                    </div>

                                                    <div>

                                                        <FaQuestionCircle />

                                                        <span>

                                                            {quiz.total_questions} Questions

                                                        </span>

                                                    </div>

                                                    <div>

                                                        <FaCheckCircle />

                                                        <span>

                                                            {quiz.total_marks} Marks

                                                        </span>

                                                    </div>

                                                    <div>

                                                        🎯

                                                        <span>

                                                            Pass {quiz.passing_percentage}%

                                                        </span>

                                                    </div>

                                                </div>
                                                <Pagination 
                                                    currentPage={currentPage}
                                                    totalItems={quizzes.length}
                                                    itemsPerPage={itemsPerPage}
                                                    onPageChange={setCurrentPage}
                                                    onItemsPerPageChange={(value) => {
                                                        setItemsPerPage(value);
                                                        setCurrentPage(1);
                                                    }}
                                                    
                                                    />

                                                <button

                                                    className="start-btn"

                                                    onClick={() =>

                                                        handleStartQuiz(

                                                            quiz

                                                        )

                                                    }

                                                >

                                                    <FaPlay />

                                                    Start Quiz

                                                </button>

                                            </div>

                                        )

                                    )

                                }

                            </div>

                        )

                    }

                </div>

            </div>

        </div>

    );

}

export default StudentAssessment;