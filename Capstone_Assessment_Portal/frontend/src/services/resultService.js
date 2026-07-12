/**
 * Result Service
 * Responsibilities:
 *  -fetch all quiz attempt/results
 */
import api from "./api";

/**
 * Fetch all quiz attempts
 */
export const getAllResults = async () =>
{
    const response = await api.get("/results/admin");
    return response.data;
}
/**
 * Fetch logged in student's results
 */
export const getStudentResults = async () =>
{

    const response = await api.get(
        "/results/history"
    );

    return response.data;

};
/**
 * Fetch single quiz result
 */
export const getResult = async (attemptId) => {

    const response = await api.get(

        `/results/${attemptId}`

    );

    return response.data;

};
