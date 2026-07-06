/**
 * Category Service
 *
 * Responsibilities:
 * - Create category
 * - Get all categories
 * - Update category
 * - Delete category
 */

import api from "./api";

/**
 * Fetch all categories
 */
export const getAllCategories = async () => {

    const response = await api.get(
        "/categories"
    );

    return response.data;

};


/**
 * Create a new category
 */
export const createCategory = async (
    categoryData
) => {

    const response = await api.post(
        "/categories",
        categoryData
    );

    return response.data;

};


/**
 * Update existing category
 */
export const updateCategory = async (
    categoryId,
    categoryData
) => {

    const response = await api.put(
        `/categories/${categoryId}`,
        categoryData
    );

    return response.data;

};


/**
 * Delete category
 */
export const deleteCategory = async (
    categoryId
) => {

    const response = await api.delete(
        `/categories/${categoryId}`
    );

    return response.data;

};