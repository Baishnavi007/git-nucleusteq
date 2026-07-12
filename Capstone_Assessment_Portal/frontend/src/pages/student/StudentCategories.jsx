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

import {
    getAllCategories
} from "../../services/categoryService";

import "./StudentCategories.css";

function StudentCategories() {

    const navigate = useNavigate();

    const [categories, setCategories] = useState([]);

    const [searchText, setSearchText] = useState("");

    useEffect(() => {

        fetchCategories();

    }, []);

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

                            filteredCategories.map(

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

                </div>

            </div>

        </div>

    );

}

export default StudentCategories;