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