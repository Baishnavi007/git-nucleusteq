/**
 * Quiz Service
 * Responsibilities:
 *  -Fetch all quizzes
 *  -Fetch quizzes by category
 *  -Create quiz
 *  -Update quiz
 *  -Delete quiz
 *  -Publish quiz
 *  -Unpublish quiz
 */
import api from "./api";

/**
 * Fetch all quizzes
 */
export const getAllQuizzes = async () =>
{
    const response = await api.get("/quizzes");
    return response.data;
};

/**
 * Fetch quizzes by category
 */
export const getQuizzesByCategory = async (categoryId) =>{
    const response = await api.get(`/quizzes/category/${categoryId}`);

    return response.data;
};

/**
 * Create quiz
 */
export const createQuiz = async (
    categoryId,
    quizData
)=> {
    const response = await api.post(`/quizzes/category/${categoryId}`, quizData);

    return response.data;
};

/**
 * Update quiz
 */
export const updateQuiz = async (
    quizId,
    quizData
) => {

    const response = await api.put(
        `/quizzes/${quizId}`,
        quizData
    );

    return response.data;

};

/**
 * Delete quiz
 */
export const deleteQuiz = async (
    quizId
) => {

    const response = await api.delete(
        `/quizzes/${quizId}`
    );

    return response.data;

};

/**
 * Publish quiz
 */
export const publishQuiz = async (
    quizId
) => {

    const response = await api.patch(
        `/quizzes/${quizId}/publish`
    );

    return response.data;

};

/**
 * Unpublish quiz
 */
export const unpublishQuiz = async (
    quizId
) => {

    const response = await api.patch(
        `/quizzes/${quizId}/unpublish`
    );

    return response.data;

};
