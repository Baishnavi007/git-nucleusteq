/**
 * Category Form
 *
 * Responsibilities:
 * - Add new category
 * - Edit existing category
 * - Display as a right-side drawer
 */

import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { validateCategoryForm} from "../../utils/validation";
import { getErrorMessage} from "../../utils/errorHandler";

import {
    FaTimes,
    FaFolderOpen
} from "react-icons/fa";

import Input from "../common/Input";
import Button from "../common/Button";

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
    * Stores validation errors.
   */
    const [errors, setErrors] = useState({});

    /**
     * Controls submit button loading.
    */
    const [loading, setLoading] = useState(false);  

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
        else{
            setCategoryData({
                name: "",
                description: ""
            })
        }
        /**
         * Clear previous validation errors
         */
        setErrors({});

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

        /**
         * Remove validation errors while user types
         */
        setErrors((previousErrors) => ({
            ...previousErrors,
            [name]: ""
        }));
                

    };


    /**
     * Handles form submission.
     */
    const handleSubmit = async (event) => {

        event.preventDefault();
        const validationErrors = validateCategoryForm(categoryData);
        if (Object.keys(validationErrors).length>0){
            setErrors(validationErrors);
            return;
        }
        setLoading(true);

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
            toast.success(
                selectedCategory
                ? "Category updated successfully"
                :"Category created successfully"
            );

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

            toast.error(

                getErrorMessage(error)

            );

        }
        finally{
            setLoading(false);
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

                        error={errors.name}

                    />
                    <div className="input-group">
                        <label>
                            Description
                        </label>
                        <textarea
                            name="description"
                            value={categoryData.description}
                            placeholder="Enter description"
                            onChange={handleInputChange}
                            rows="4"
                         />
                         {
                            errors.description && (
                                <p className="input-error">
                                    {errors.description}
                                </p>
                            )
                         }

                    </div>

                    

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
                            loading={loading}

                        />

                    </div>

                </form>

            </div>

        </>

    );

}

export default CategoryForm;