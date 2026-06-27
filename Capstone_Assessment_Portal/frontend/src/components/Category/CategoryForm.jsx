/**
 * Category Form
 *
 * Responsibilities:
 * - Add new category
 * - Edit existing category
 * - Display as a right-side drawer
 */

import { useEffect, useState } from "react";

import {
    FaTimes,
    FaFolderOpen
} from "react-icons/fa";

import Input from "../Input";
import Button from "../Button";

import {
    createCategory,
    updateCategory
} from "../../services/categoryService";

import "./CategoryForm.css";

function CategoryForm({

    selectedCategory,

    fetchCategories,

    onClose

}) {

    /**
     * Stores category form data.
     */
    const [categoryData, setCategoryData] = useState({

        name: "",

        description: ""

    });

    /**
     * Populate form while editing.
     */
    useEffect(() => {

        if (selectedCategory) {

            setCategoryData({

                name: selectedCategory.name,

                description: selectedCategory.description

            });

        }

    }, [selectedCategory]);


    /**
     * Handles input changes.
     */
    const handleInputChange = (event) => {

        const {

            name,

            value

        } = event.target;

        setCategoryData((previousData) => ({

            ...previousData,

            [name]: value

        }));

    };


    /**
     * Handles form submission.
     */
    const handleSubmit = async (event) => {

        event.preventDefault();

        try {

            if (selectedCategory) {

                await updateCategory(

                    selectedCategory.id,

                    categoryData

                );

            }

            else {

                await createCategory(

                    categoryData

                );

            }

            /**
             * Refresh category list.
             */
            await fetchCategories();

            /**
             * Close drawer.
             */
            onClose();

        }

        catch (error) {

            console.error(

                "Failed to save category.",

                error

            );

            alert(

                error.response?.data?.detail ||

                "Something went wrong."

            );

        }

    };


    return (

        <>

            {/* Dark Overlay */}

            <div

                className="drawer-overlay"

                onClick={onClose}

            ></div>


            {/* Drawer */}

            <div className="category-drawer">

                <div className="drawer-header">

                    <div className="drawer-title">

                        <FaFolderOpen />

                        <h2>

                            {

                                selectedCategory

                                    ? "Edit Category"

                                    : "Add Category"

                            }

                        </h2>

                    </div>

                    <button

                        className="close-btn"

                        onClick={onClose}

                    >

                        <FaTimes />

                    </button>

                </div>


                <form

                    onSubmit={handleSubmit}

                >

                    <Input

                        label="Category Name"

                        name="name"

                        value={categoryData.name}

                        placeholder="Enter category name"

                        onChange={handleInputChange}

                        required

                    />

                    <Input

                        label="Description"

                        name="description"

                        value={categoryData.description}

                        placeholder="Enter description"

                        onChange={handleInputChange}

                        required

                    />

                    <div className="drawer-buttons">

                        <button

                            type="button"

                            className="cancel-btn"

                            onClick={onClose}

                        >

                            Cancel

                        </button>

                        <Button

                            text={

                                selectedCategory

                                    ? "Update Category"

                                    : "Save Category"

                            }

                            type="submit"

                        />

                    </div>

                </form>

            </div>

        </>

    );

}

export default CategoryForm;