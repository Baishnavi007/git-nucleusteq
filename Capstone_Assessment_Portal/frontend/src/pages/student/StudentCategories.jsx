/**
 * Student Categories Page
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    FaFolderOpen,
    FaSearch,
    FaArrowRight
} from "react-icons/fa";

import SideBar from "../../components/layout/SideBar/SideBar";
import TopBar from "../../components/layout/Topbar/TopBar";
import Pagination from "../../components/common/Pagination";

import {
    getAllCategories
} from "../../services/categoryService";

import "./StudentCategories.css";

function StudentCategories() {

    const navigate = useNavigate();

    const [categories, setCategories] = useState([]);

    const [searchText, setSearchText] = useState("");

    /**
     * Pagination
     */
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(6);

    useEffect(() => {

        fetchCategories();

    }, []);

    useEffect (() => {
        setCurrentPage(1);
    },[searchText]);

    const fetchCategories = async () => {

        try {

            const response = await getAllCategories();

            setCategories(response);

        }

        catch (error) {

            console.error(error);

        }

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
     * PAagination
     */
    const lastIndex = currentPage * itemsPerPage;
    const firstIndex = lastIndex - itemsPerPage;
    const currentCategories = filteredCategories.slice(
        firstIndex,
        lastIndex
    );

    return (

        <div className="student-category-page">

            <SideBar />

            <div className="student-category-content">

                <TopBar title="Categories" />

                <div className="student-category-container">

                    <div className="student-category-header">

                        <div>

                            <h1>

                                Categories

                            </h1>

                            <p>

                                Choose a category to explore
                                available quizzes.

                            </p>

                        </div>

                    </div>

                    <div className="student-search-box">

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

                    <div className="student-category-grid">

                        {

                            currentCategories.map(

                                (category) => (

                                    <div

                                        key={category.id}

                                        className="student-category-card"

                                    >

                                        <div className="category-icon">

                                            <FaFolderOpen />

                                        </div>

                                        <h2>

                                            {category.name}

                                        </h2>

                                        <p>

                                            {category.description}

                                        </p>

                                        <button

                                            className="view-btn"

                                            onClick={() =>

                                                navigate(

                                                    `/student/assessments/${category.id}`,

                                                    {

                                                        state: {

                                                            categoryName:
                                                                category.name

                                                        }

                                                    }

                                                )

                                            }

                                        >

                                            View Assessments

                                            <FaArrowRight />

                                        </button>

                                    </div>

                                )

                            )

                        }

                    </div>
                    <Pagination
                        currentPage={currentPage}
                        totalItems={filteredCategories.length}
                        itemsPerPage={itemsPerPage}
                        onPageChange={setCurrentPage}
                        onItemsPerPageChange={(value) => {
                            setItemsPerPage(value);
                            setCurrentPage(1);


                        }} />


                </div>

            </div>

        </div>

    );

}

export default StudentCategories;