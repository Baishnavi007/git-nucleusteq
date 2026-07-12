/**
 * Result Service
 * Responsibilities:
 *  - fetch all quiz attempt/results
 */

import api from "./api";

/**
 * Fetch all quiz attempts (Admin)
 */
export const getAllResults = async () => {

    const response = await api.get(
        "/results/admin"
    );

    return response.data;

};

/**
 * Fetch logged in student's results
 */
export const getStudentResults = async () => {

    const response = await api.get(
        "/results/history"
    );

    return response.data;

};

/**
 * Fetch single quiz result (Student)
 */
export const getResult = async (attemptId) => {

    const response = await api.get(
        `/results/${attemptId}`
    );

    return response.data;

};

/**
 * Fetch any student's result (Admin)
 */
export const getAdminResult = async (attemptId) => {

    const response = await api.get(
        `/results/admin/${attemptId}`
    );

    return response.data;

};