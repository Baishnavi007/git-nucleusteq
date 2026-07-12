/**
 * Admin Result Page
 */

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import { getAdminResult } from "../../services/resultService";

import "./AdminResult.css";

function AdminResult() {

    const { attemptId } = useParams();

    const navigate = useNavigate();

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(true);

    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {

        fetchResult();

    }, []);

    const fetchResult = async () => {

        try {

            const response = await getAdminResult(

                attemptId

            );

            setResult(response);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    };

    if (loading) {

        return <h2>Loading...</h2>;

    }

    const currentQuestion = result.questions[currentIndex];

    return (

        <div className="student-result-page">

            <SideBar />

            <div className="student-result-content">

                <TopBar title="Student Result" />

                <div className="result-container">

                    <div className="result-card">

                        <h1>

                            {result.quiz_title}

                        </h1>

                        <h2>

                            {

                                result.is_pass

                                    ? "🎉 PASS"

                                    : "❌ FAIL"

                            }

                        </h2>

                        <div className="score-circle">

                            {result.percentage.toFixed(0)}%

                        </div>

                        {/* Student Details */}

                        <div className="student-details">

                            <h3>

                                👤 {result.student_name}

                            </h3>

                            <p>

                                📧 {result.student_email}

                            </p>

                        </div>

                        <div className="result-grid">

                            <div>

                                <span>

                                    Score

                                </span>

                                <h3>

                                    {result.score} / {result.total_marks}

                                </h3>

                            </div>

                            <div>

                                <span>

                                    Attempt

                                </span>

                                <h3>

                                    #{result.attempt_number}

                                </h3>

                            </div>

                            <div>

                                <span>

                                    Passing %

                                </span>

                                <h3>

                                    {result.passing_percentage}%

                                </h3>

                            </div>

                            <div>

                                <span>

                                    Status

                                </span>

                                <h3>

                                    {

                                        result.is_pass

                                            ? "Passed"

                                            : "Failed"

                                    }

                                </h3>

                            </div>

                        </div>

                        <div className="result-times">

                            <div>

                                <strong>

                                    Started

                                </strong>

                                <p>

                                    {

                                        new Date(

                                            result.started_at

                                        ).toLocaleString()

                                    }

                                </p>

                            </div>

                            <div>

                                <strong>

                                    Submitted

                                </strong>

                                <p>

                                    {

                                        new Date(

                                            result.submitted_at

                                        ).toLocaleString()

                                    }

                                </p>

                            </div>

                            <div>

                                <strong>

                                    Passing Marks

                                </strong>

                                <p>

                                    {

                                        result.passing_marks

                                    }

                                </p>

                            </div>

                        </div>

                        <div className="question-palette">

                            <h2>

                                Attempt Review

                            </h2>

                            {

                                result.questions.map(

                                    (question, index) => (

                                        <button

                                            key={index}

                                            className={

                                                currentIndex === index

                                                    ? "palette-btn active"

                                                    : question.is_correct

                                                        ? "palette-btn correct"

                                                        : "palette-btn wrong"

                                            }

                                            onClick={() =>

                                                setCurrentIndex(index)

                                            }

                                        >

                                            {index + 1}

                                        </button>

                                    )

                                )

                            }

                        </div>

                        <div className="question-review">

                            <h2>

                                Question {currentIndex + 1}

                            </h2>

                            <p className="question-text">

                                {currentQuestion.question}

                            </p>

                            <div className="options-review">

                                {

                                    currentQuestion.options.map(

                                        (option, index) => (

                                            <div

                                                key={index}

                                                className={

                                                    option === currentQuestion.correct_answer

                                                        ? "option-box correct"

                                                        : option === currentQuestion.selected_answer

                                                            ? "option-box wrong"

                                                            : "option-box"

                                                }

                                            >

                                                {option}

                                            </div>

                                        )

                                    )

                                }

                            </div>

                            <div className="review-info">

                                <p>

                                    <strong>

                                        Student Answer :

                                    </strong>

                                    {

                                        currentQuestion.selected_answer ||

                                        "Not Attempted"

                                    }

                                </p>

                                <p>

                                    <strong>

                                        Correct Answer :

                                    </strong>

                                    {

                                        currentQuestion.correct_answer

                                    }

                                </p>

                                <p>

                                    <strong>

                                        Marks :

                                    </strong>

                                    {

                                        currentQuestion.obtained_marks

                                    }

                                    /

                                    {

                                        currentQuestion.marks

                                    }

                                </p>

                            </div>

                        </div>

                        <div className="result-actions">

                            <button

                                className="dashboard-btn"

                                onClick={() =>

                                    navigate("/admin/results")

                                }

                            >

                                Back

                            </button>

                            <button

                                className="category-btn"

                                onClick={() =>

                                    navigate("/admin/dashboard")

                                }

                            >

                                Dashboard

                            </button>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default AdminResult;