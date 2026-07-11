/**
 * Question Service
 *
 * Responsibilities:
 * - Fetch questions
 * - Create question
 * - Update question
 * - Delete question
 */

import api from "./api";

/**
 * Fetch questions by quiz.
 */
export const getQuestionsByQuiz = async (

    quizId

) => {

    const response = await api.get(

        `/questions/quiz/${quizId}`

    );

    return response.data;

};

/**
 * Create question.
 */
export const createQuestion = async (

    quizId,

    questionData

) => {

    const response = await api.post(

        `/questions/quiz/${quizId}`,

        questionData

    );

    return response.data;

};

/**
 * Update question.
 */
export const updateQuestion = async (

    questionId,

    questionData

) => {

    const response = await api.put(

        `/questions/${questionId}`,

        questionData

    );

    return response.data;

};

/**
 * Delete question.
 */
export const deleteQuestion = async (

    questionId

) => {

    const response = await api.delete(

        `/questions/${questionId}`

    );

    return response.data;

};