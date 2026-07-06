/**
 * Category List
 *
 * Responsibilities:
 * - Display all categories
 * - Search categories
 * - Delete category
 * - Open edit drawer
 */

import {
    FaEdit,
    FaTrash,
    FaInbox,
    FaEye
} from "react-icons/fa";

import { useNavigate } from "react-router-dom";

import {
    deleteCategory
} from "../../services/categoryService";

import "./CategoryList.css";

function CategoryList({

    categories,

    searchText,

    onEdit,

    fetchCategories

}) {

    const navigate = useNavigate();

    /**
     * Logged in user role.
     */
    const role = localStorage.getItem("role");

    const isAdmin = role === "admin";

    /**
     * Delete category.
     */
    const handleDeleteCategory = async (
        categoryId
    ) => {

        const isConfirmed = window.confirm(

            "Are you sure you want to delete this category?"

        );

        if (!isConfirmed) {

            return;

        }

        try {

            await deleteCategory(categoryId);

            await fetchCategories();

        }

        catch (error) {

            console.error(

                "Failed to delete category.",

                error

            );

        }

    };

    /**
     * Filter categories according to search.
     */
    const filteredCategories = categories.filter(

        (category) =>

            category.name
                .toLowerCase()
                .includes(
                    searchText.toLowerCase()
                )

    );

    return (

        <div className="category-table-container">

            <table className="category-table">

                <thead>

                    <tr>

                        <th>Name</th>

                        <th>Description</th>

                        <th>Created By</th>

                        <th>Created On</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        filteredCategories.length > 0 ?

                            filteredCategories.map(

                                (category) => (

                                    <tr
                                        key={category.id}
                                    >

                                        <td>

                                            {category.name}

                                        </td>

                                        <td>

                                            {category.description}

                                        </td>

                                        <td>

                                            {category.created_by}

                                        </td>

                                        <td>

                                            {

                                                new Date(

                                                    category.created_at

                                                ).toLocaleDateString()

                                            }

                                        </td>

                                        <td>

                                            {

                                                isAdmin ? (

                                                    <>

                                                        <button
                                                            className="edit-btn"
                                                            onClick={() =>
                                                                onEdit(category)
                                                            }
                                                        >

                                                            <FaEdit />

                                                        </button>

                                                        <button
                                                            className="delete-btn"
                                                            onClick={() =>
                                                                handleDeleteCategory(
                                                                    category.id
                                                                )
                                                            }
                                                        >

                                                            <FaTrash />

                                                        </button>

                                                    </>

                                                ) : (

                                                    <button
                                                        className="view-btn"
                                                        onClick={() =>
                                                            navigate(
                                                                `/student/categories/${category.id}`
                                                            )
                                                        }
                                                    >

                                                        <FaEye />

                                                    </button>

                                                )

                                            }

                                        </td>

                                    </tr>

                                )

                            )

                            :

                            <tr>

                                <td
                                    colSpan="5"
                                    className="empty-state"
                                >

                                    <FaInbox />

                                    <p>

                                        No categories found.

                                    </p>

                                </td>

                            </tr>

                    }

                </tbody>

            </table>

        </div>

    );

}

export default CategoryList;