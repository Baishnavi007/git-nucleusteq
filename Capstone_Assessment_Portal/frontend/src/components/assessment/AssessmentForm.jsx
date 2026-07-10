/**
 * Assessment Form
 *
 * Responsibilities:
 * - Add assessment
 * - Edit assessment
 * - Display as right-side drawer
 */

import { useEffect, useState } from "react";

import {
    FaClipboardList,
    FaTimes
} from "react-icons/fa";

import Input from "../common/Input";
import Button from "../common/Button";

import {createQuiz, updateQuiz} from "../../services/quizService";
import { validateAssessmentForm } from "../../utils/validation";
import { getErrorMessage } from "../../utils/errorHandler";

import { toast } from "react-toastify";
import {
    getAllCategories
} from "../../services/categoryService";

import "./AssessmentForm.css";

function AssessmentForm({

    selectedQuiz,

    fetchQuizzes,

    onClose

}) {

    /**
     * Stores assessment form data.
     */
    const [assessmentData, setAssessmentData] = useState({

        category_id: "",

        title: "",

        description: "",

        duration: "",

        passing_percentage: ""

    });

    /**
     * Stores all categories.
     */
    const [categories, setCategories] = useState([]);

    /**
     * Stores validation errors
     */
    const [errors, setErrors] = useState({});

    /**
     * LOading state
     */
    const[loading, setLoading] = useState(false);
    /**
     * Fetch all categories.
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
     * Load categories when drawer opens.
     */
    useEffect(() => {

        fetchCategories();

    }, []);

    /**
     * Populate form while editing.
     * (Will be useful later)
     */
    useEffect(() => {

        if (selectedQuiz) {

            setAssessmentData({

                category_id:
                    selectedQuiz.category_id,

                title:
                    selectedQuiz.title,

                description:
                    selectedQuiz.description,

                duration:
                    selectedQuiz.duration,

                passing_percentage:
                    selectedQuiz.passing_percentage

            });

        }

    }, [selectedQuiz]);

    /**
     * Handle input changes.
     */
    const handleInputChange = (

        event

    ) => {

        const {

            name,

            value

        } = event.target;

        setAssessmentData(

            (previousData) => ({

                ...previousData,

                [name]: value

            })

        );
        setErrors((previousErrros) => ({
            ...previousErrros,
            [name]: ""
        }) );

    };

    /**
     * Handle form submit.
     * (API integration in next step)
     */
    const handleSubmit = async (

        event

    ) => {

        event.preventDefault();
        /**
         * Validate assessment form
         */
        const validationErrors = validateAssessmentForm(assessmentData);
        if(Object.keys(validationErrors).length>0){
            setErrors(validationErrors);
            return;
        }
        setLoading(true);
        try{
            if(selectedQuiz){
                await updateQuiz(
                    selectedQuiz.id,
                    {
                        title: assessmentData.title,
                        description: assessmentData.description,
                        duration: Number(assessmentData.duration),
                        passing_percentage: Number(assessmentData.passing_percentage)
                    }
                );
                toast.success("Assessment updated successfully.");

            }
            else{
                await createQuiz(
                    assessmentData.category_id,
                {
                    title: assessmentData.title,
                    description: assessmentData.description,
                    duration: Number(assessmentData.duration),
                    passing_percentage: Number(assessmentData.passing_percentage)
                });
                toast.success("Assessment create successfully");
            }
            await fetchQuizzes();
            onClose();
        }
        catch(error){
            toast.error(getErrorMessage(error));
        }
        finally{
            setLoading(false);
        }

    };

    return (

        <>

            {/* Overlay */}

            <div

                className="drawer-overlay"

                onClick={onClose}

            ></div>

            {/* Drawer */}

            <div className="assessment-drawer">

                <div className="drawer-header">

                    <div className="drawer-title">

                        <FaClipboardList />

                        <h2>

                            {

                                selectedQuiz

                                    ? "Edit Assessment"

                                    : "Add Assessment"

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

                    {/* Category */}

                    <div className="input-group">

                        <label>

                            Category

                        </label>

                        <select

                            name="category_id"

                            value={assessmentData.category_id}

                            onChange={handleInputChange}

                            disabled={selectedQuiz}

                        >

                            <option value="">

                                Select Category

                            </option>

                            {

                                categories.map(

                                    (category) => (

                                        <option

                                            key={category.id}

                                            value={category.id}

                                        >

                                            {category.name}

                                        </option>

                                    )

                                )

                            }

                        </select>
                        {
                            errors.category_id && (
                                <p className="input-error">
                                    {errors.category_id}
                                </p>
                            )
                        }

                    </div>

                    {/* Quiz Title */}

                    <Input

                        label="Quiz Title"

                        name="title"

                        value={assessmentData.title}

                        placeholder="Enter quiz title"

                        onChange={handleInputChange}
                        
                        error={errors.title}

                    />

                    {/* Description */}

                    <div className="input-group">

                        <label>

                            Description

                        </label>

                        <textarea

                            name="description"

                            value={assessmentData.description}

                            placeholder="Enter quiz description"

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

                    {/* Duration */}

                    <Input

                        label="Duration (Minutes)"

                        type="number"

                        name="duration"

                        value={assessmentData.duration}

                        placeholder="Enter duration"

                        onChange={handleInputChange}

                        error={errors.duration}

                    />

                    {/* Passing Percentage */}

                    <Input

                        label="Passing Percentage"

                        type="number"

                        name="passing_percentage"

                        value={assessmentData.passing_percentage}

                        placeholder="Enter passing percentage"

                        onChange={handleInputChange}
                        error={errors.passing_percentage}

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

                                selectedQuiz

                                    ? "Update Assessment"

                                    : "Save Assessment"

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

export default AssessmentForm;