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

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";

import CategoryForm from "../../components/category/CategoryForm";
import CategoryList from "../../components/category/CategoryList";
import Pagination from "../../components/common/Pagination";

import {
    getAllCategories
} from "../../services/categoryService";

import "./CategoryManagement.css";

function CategoryManagement() {

    /**
     * Logged in user role.
     */
    const role = localStorage.getItem("role");

    const isAdmin = role === "admin";

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
    const [selectedCategory, setSelectedCategory] = useState(null);
    /**
     * Pagination
     */
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(5);
    /**
     * Fetch all categories from backend.
     */
    const fetchCategories = async () => {

        try {

            const response = await getAllCategories();

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

    useEffect(() =>{
        setCurrentPage(1);
    }, [searchText]);

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
    const handleEditCategory = (category) => {

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
    const filteredCategories = categories.filter(
        (category) =>
            category.name
                .toLowerCase()
                .includes(
                    searchText.toLowerCase()
                )
    );

    /**
     * Pagination
     */
    const lastIndex = currentPage * itemsPerPage;
    const firstIndex = lastIndex - itemsPerPage;
    const currentCategories = filteredCategories.slice(
        firstIndex,
        lastIndex
    
    );
    console.log("Total:", categories.length);

console.log("Filtered:", filteredCategories.length);

console.log("Current:", currentCategories.length);
    return (

        <div className="category-page">

            <SideBar />

            <div className="category-content">

                <TopBar title="Categories"  />

                <div className="category-container">

                    {/* Header */}

                    <div className="category-header">

                        <div>

                            <div className="page-title">

                                <FaFolderOpen />

                                <h1>

                                    {
                                        isAdmin
                                            ? "Category Management"
                                            : "Categories"
                                    }

                                </h1>

                            </div>

                            <p>

                                {
                                    isAdmin
                                        ? "Create, update and manage assessment categories."
                                        : "Browse all available assessment categories."
                                }

                            </p>

                        </div>

                        {

                            isAdmin && (

                                <button
                                    className="add-category-btn"
                                    onClick={handleAddCategory}
                                >

                                    <FaPlus />

                                    Add Category

                                </button>

                            )

                        }

                    </div>

                    {/* Search */}

                    <div className="search-box">

                        <FaSearch />

                        <input
                            type="text"
                            placeholder="Search category..."
                            value={searchText}
                            onChange={(event) =>
                                setSearchText(event.target.value)
                            }
                        />

                    </div>

                    {/* Category Table */}

                    <CategoryList
                        categories={currentCategories}
                        onEdit={handleEditCategory}
                        fetchCategories={fetchCategories}
                    />
                    <Pagination
                        currentPage={currentPage}
                        totalItems={filteredCategories.length}
                        itemsPerPage={itemsPerPage}
                        onPageChange={setCurrentPage}
                        onItemsPerPageChange={(value) => {
                            setItemsPerPage(value);
                            setCurrentPage(1);
                        }}
                        
                        />


                </div>

            </div>

            {

                isAdmin &&

                isDrawerOpen && (

                    <CategoryForm
                        selectedCategory={selectedCategory}
                        fetchCategories={fetchCategories}
                        onClose={handleCloseDrawer}
                    />

                )

            }

        </div>

    );

}

export default CategoryManagement;