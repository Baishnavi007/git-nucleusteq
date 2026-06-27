/**
 * Category Management Page
 *
 * Responsibilities:
 * - Fetch all categories
 * - Display categories
 * - Open/Close drawer
 * - Handle search
 * - Pass data to child components
 */

import { useEffect, useState } from "react";

import {
    FaFolderOpen,
    FaPlus,
    FaSearch
} from "react-icons/fa";

import SideBar from "../components/Sidebar/SideBar";
import TopBar from "../components/Topbar/TopBar";

import CategoryForm from "../components/Category/CategoryForm";
import CategoryList from "../components/Category/CategoryList";


import {
    getAllCategories
} from "../services/categoryService";

import "./CategoryManagement.css";

function CategoryManagement() {

    /**
     * Stores all categories.
     */
    const [categories, setCategories] = useState([]);

    /**
     * Controls drawer visibility.
     */
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    /**
     * Stores search text.
     */
    const [searchText, setSearchText] = useState("");

    /**
     * Stores selected category while editing.
     */
    const [selectedCategory, setSelectedCategory] =
        useState(null);

    /**
     * Fetch all categories from backend.
     */
    const fetchCategories = async () => {

        try {

            const response =
                await getAllCategories();

            setCategories(response);

        }

        catch (error) {

            console.error(
                "Failed to fetch categories.",
                error
            );

        }

    };

    /**
     * Runs only once when page loads.
     */
    useEffect(() => {

        fetchCategories();

    }, []);

    /**
     * Open drawer for creating category.
     */
    const handleAddCategory = () => {

        setSelectedCategory(null);

        setIsDrawerOpen(true);

    };

    /**
     * Open drawer for editing category.
     */
    const handleEditCategory = (
        category
    ) => {

        setSelectedCategory(category);

        setIsDrawerOpen(true);

    };

    /**
     * Close drawer.
     */
    const handleCloseDrawer = () => {

        setSelectedCategory(null);

        setIsDrawerOpen(false);

    };

    return (

        <div className="category-page">

            <SideBar />

            <div className="category-content">

                <TopBar />

                <div className="category-container">

                    {/* Header */}

                    <div className="category-header">

                        <div>

                            <div className="page-title">

                                <FaFolderOpen />

                                <h1>

                                    Category Management

                                </h1>

                            </div>

                            <p>

                                Create, update and manage
                                assessment categories.

                            </p>

                        </div>

                        <button
                            className="add-category-btn"
                            onClick={
                                handleAddCategory
                            }
                        >

                            <FaPlus />

                            Add Category

                        </button>

                    </div>

                    {/* Search */}

                    <div className="search-box">

                        <FaSearch />

                        <input
                            type="text"
                            placeholder="Search category..."
                            value={searchText}
                            onChange={(event) =>
                                setSearchText(
                                    event.target.value
                                )
                            }
                        />

                    </div>

                    {/* Category Table */}

                    <CategoryList

                        categories={categories}

                        searchText={searchText}

                        onEdit={
                            handleEditCategory
                        }

                        fetchCategories={
                            fetchCategories
                        }

                    />

                </div>

            </div>

            {

                isDrawerOpen && (

                    <CategoryForm

                        selectedCategory={
                            selectedCategory
                        }

                        fetchCategories={
                            fetchCategories
                        }

                        onClose={
                            handleCloseDrawer
                        }

                    />

                )

            }

        </div>

    );

}

export default CategoryManagement;