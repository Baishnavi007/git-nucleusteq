/**
 * Quiz Attempt Service
 */

import api from "./api";

/**
 * Start Quiz Attempt
 */

export const startQuizAttempt = async (
    quizId
) => {

    const response = await api.post(

        "/quiz-attempts/",

        {
            quiz_id: quizId
        }

    );

    return response.data;

};


/**
 * Fetch Questions
 */

export const getAttemptQuestions = async (
    attemptId
) => {

    const response = await api.get(

        `/quiz-attempts/${attemptId}/questions`

    );

    return response.data;

};


/**
 * Save Answer
 */

export const saveAnswer = async (

    attemptId,

    questionId,

    selectedAnswer

) => {

    const response = await api.patch(

        `/quiz-attempts/${attemptId}/answer`,

        {

            question_id: questionId,

            selected_answer: selectedAnswer

        }

    );

    return response.data;

};


/**
 * Submit Quiz
 */

export const submitQuiz = async (

    attemptId

) => {

    const response = await api.post(

        `/quiz-attempts/${attemptId}/submit`

    );

    return response.data;

};


/**
 * Fetch Student Attempts
 */

export const getStudentAttempts = async (

    quizId

) => {

    const response = await api.get(

        `/quiz-attempts/quiz/${quizId}`

    );

    return response.data;

};