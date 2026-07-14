/**
 * Student Question Page
 */

import { useEffect, useState } from "react";

import {
    useNavigate,
    useParams,
    useLocation
} from "react-router-dom";

import {
    FaArrowLeft,
    FaArrowRight,
    FaCheck
} from "react-icons/fa";

import { toast } from "react-toastify";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import {

    getAttemptQuestions,

    saveAnswer,

    submitQuiz

} from "../../services/quizAttemptService";

import "./StudentQuestion.css";

function StudentQuestion() {

    const navigate = useNavigate();

    const { attemptId } = useParams();

    const location = useLocation();

    const storedQuiz = JSON.parse(
        localStorage.getItem(
            "activeQuiz"
        ),
    );

    const duration = location.state?.duration || storedQuiz?.duration || 0;

    const startedAt = location.state?.startedAt || storedQuiz?.startedAt;

    const quizTitle = location.state?.quizTitle || storedQuiz?.quizTitle || "Quiz";

    const [questions, setQuestions] = useState([]);

    const [currentIndex, setCurrentIndex] = useState(0);

    const [loading, setLoading] = useState(true);

    const [timeLeft, setTimeLeft] = useState(0);

    const currentQuestion = questions[currentIndex];

    if (!loading && !currentQuestion) {

    return (

        <div>

            No Questions Found

        </div>

    );

}

    useEffect(() => {

        fetchQuestions();

    }, []);

    useEffect(() => {
        if (loading) return;

        if (!loading && timeLeft <= 0) {

            handleSubmit();

            return;

        }
        

        const timer = setInterval(() => {

            setTimeLeft((previous) => previous - 1);

        }, 1000);

        return () => clearInterval(timer);

    }, [timeLeft, loading]);

    const fetchQuestions = async () => {

        try {

            const response =

                await getAttemptQuestions(

                    attemptId

                );

            setQuestions(response);

            setLoading(false);
            console.log("startedAt :", startedAt);

console.log("duration :", duration);

console.log("attemptId :", attemptId);

console.log("questions :", response);

            /**
             * Timer
             */
            const startTime = new Date(
                `${startedAt}Z`
            ).getTime();

            const endTime =
                 startTime +
                 duration * 60 * 1000;

            const remaining = Math.max(
                0,
                Math.floor(
                    (endTime - Date.now()) /1000
                )
            );

            setTimeLeft(

                remaining

            );
            console.log("startTime", startTime);

console.log("endTime", endTime);

console.log("now", Date.now());

console.log("remaining", remaining);

        }

        catch (error) {

            toast.error(

                "Unable to load quiz."

            );

        }

    };

    const handleOptionSelect = async (

        option

    ) => {

        try {

            await saveAnswer(

                attemptId,

                currentQuestion.id,

                option

            );

            const updated = [...questions];

            updated[currentIndex].selected_answer = option;

            setQuestions(updated);

        }

        catch (error) {

            toast.error(

                "Unable to save answer."

            );

        }

    };

    const nextQuestion = () => {

        if (

            currentIndex <

            questions.length - 1

        ) {

            setCurrentIndex(

                currentIndex + 1

            );

        }

    };

    const previousQuestion = () => {

        if (

            currentIndex > 0

        ) {

            setCurrentIndex(

                currentIndex - 1

            );

        }

    };

    const handleSubmit = async () => {

        try {

            await submitQuiz(

                attemptId

            );

            localStorage.removeItem("activeQuiz")

            toast.success(

                "Quiz Submitted"

            );

            navigate(

                `/student/results/${attemptId}`

            );

        }

        catch (error) {

            toast.error(

                "Unable to submit quiz."

            );

        }

    };
        const formatTime = () => {

        const minutes = Math.floor(
            timeLeft / 60
        );

        const seconds = timeLeft % 60;

        return `${minutes}:${seconds
            .toString()
            .padStart(2, "0")}`;

    };

    if (loading) {

        return (

            <div>

                Loading...

            </div>

        );

    }

    return (

        <div className="student-question-page">

            <SideBar />

            <div className="student-question-content">

                <TopBar title={quizTitle} />

                <div className="question-container">

                    <div className="question-top">
                        <div className="progress-section">

    <div className="progress-info">

        Answered {

            questions.filter(

                (question) =>

                    question.selected_answer

            ).length

        }

        {" / "}

        {

            questions.length

        }

    </div>

    <div className="progress-bar">

        <div

            className="progress-fill"

            style={{

                width: `${

                    questions.length === 0

                    ? 0

                    :

                    (

                        questions.filter(

                            question =>

                                question.selected_answer

                        ).length

                        /

                        questions.length

                    ) * 100

                }%`

            }}

        />

    </div>

</div>

                        <h2>

                            Question

                            {

                                currentIndex + 1

                            }

                            {" "}

                            of

                            {" "}

                            {

                                questions.length

                            }

                        </h2>

                        <div className="timer">

                            ⏱

                            {

                                formatTime()

                            }

                        </div>

                    </div>

                    <div className="question-card">

                        <h3>

                            {

                                currentQuestion.question

                            }

                        </h3>

                        <div className="difficulty">

                            Difficulty :
                            <strong>
                                {
                                    currentQuestion.difficulty
                                }
                            </strong>
                        </div>

                        <div className="options">

                            {

                                currentQuestion.options.map(

                                    (option) => (

                                        <button

                                            key={option}

                                            className={

                                                currentQuestion.selected_answer === option

                                                ?

                                                "option selected"

                                                :

                                                "option"

                                            }

                                            onClick={() =>

                                                handleOptionSelect(

                                                    option

                                                )

                                            }

                                        >

                                            {

                                                option

                                            }

                                        </button>

                                    )

                                )

                            }

                        </div>

                    </div>

                    <div className="question-footer">

                        <button

                            className="nav-btn"

                            onClick={

                                previousQuestion

                            }

                            disabled={

                                currentIndex === 0

                            }

                        >

                            <FaArrowLeft />

                            Previous

                        </button>

                        <div className="question-palette">

                            {

                                questions.map(

                                    (

                                        question,

                                        index

                                    ) => (

                                        <button

                                            key={

                                                question.id

                                            }

                                            className={

                                                index === currentIndex

                                                ?

                                                "palette-btn active"

                                                :

                                                question.selected_answer

                                                ?

                                                "palette-btn answered"

                                                :

                                                "palette-btn"

                                            }

                                            onClick={() =>

                                                setCurrentIndex(

                                                    index

                                                )

                                            }

                                        >

                                            {

                                                index + 1

                                            }

                                        </button>

                                    )

                                )

                            }

                        </div>

                        {

                            currentIndex ===

                            questions.length - 1

                            ?

                            (

                                <button

                                    className="submit-btn"

                                    onClick={

                                        handleSubmit

                                    }

                                >

                                    <FaCheck />

                                    Submit

                                </button>

                            )

                            :

                            (

                                <button

                                    className="nav-btn"

                                    onClick={

                                        nextQuestion

                                    }

                                >

                                    Next

                                    <FaArrowRight />

                                </button>

                            )

                        }

                    </div>

                </div>

            </div>

        </div>

    );

}

export default StudentQuestion;