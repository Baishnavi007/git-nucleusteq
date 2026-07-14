/**
 * Question Form
 *
 * Responsibilities:
 * - Add Question
 * - Edit Question
 */
import {useEffect,useState} from "react";
import {FaQuestionCircle,FaTimes} from "react-icons/fa";
import Input from "../common/Input";

import { createQuestion, updateQuestion } from "../../services/questionService";
import { toast } from "react-toastify";
import { getErrorMessage } from "../../utils/errorHandler";
import { validateQuestionForm } from "../../utils/validation";

import Button from "../common/Button";

import "./QuestionForm.css";

function QuestionForm({

    quizId,

    selectedQuestion,

    fetchQuestions,

    onClose

}) {
    /**
 * Stores question form data.
 */
const [questionData, setQuestionData] = useState({

    question: "",

    question_type: "mcq",

    options: [

        "",

        "",

        "",

        ""

    ],

    correct_answer: "",

    difficulty: "easy",

    tags: "",

    marks: ""

});

/**
 * Stores validation errors.
 */
const [errors, setErrors] = useState({});

/**
 * Loading state.
 */
const [loading, setLoading] = useState(false);

/**
 * Question types.
 */
const questionTypes = [

    "mcq",

    "true_false"

];

/**
 * Difficulty levels.
 */
const difficultyLevels = [

    "easy",

    "medium",

    "hard"

];
/**
 * Populate form while editing.
 */
useEffect(() => {
    

    if (selectedQuestion) {

        setQuestionData({

            question:

                selectedQuestion.question,

            question_type:

                selectedQuestion.question_type,

            options:

                [...selectedQuestion.options],

            correct_answer:

                selectedQuestion.correct_answer,

            difficulty:

                selectedQuestion.difficulty,

            tags:

                selectedQuestion.tags.join(","),

            marks:

                selectedQuestion.marks

        });
    }
 }, [

    selectedQuestion

]);

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

    /**
     * Handle Question Type.
     */
    if (name === "question_type") {

        if (value === "true_false") {

            setQuestionData(

                (previousData) => ({

                    ...previousData,

                    question_type: value,

                    options: [

                        "True",

                        "False"

                    ],

                    correct_answer: "True"

                })

            );

        }

        else {

            setQuestionData(

                (previousData) => ({

                    ...previousData,

                    question_type: value,

                    options: [

                        "",

                        "",

                        "",

                        ""

                    ],

                    correct_answer: ""

                })

            );

        }

    }

    else {

        setQuestionData(

            (previousData) => ({

                ...previousData,

                [name]: value

            })

        );

    }

    setErrors(

        (previousErrors) => ({

            ...previousErrors,

            [name]: ""

        })

    );

};

/**
 * Handle option changes.
 */
const handleOptionChange = (

    index,

    value

) => {

    const updatedOptions = [

        ...questionData.options

    ];

    updatedOptions[index] = value;

    setQuestionData(

        (previousData) => ({

            ...previousData,

            options: updatedOptions

        })

    );

};
/**
 * Submit Question.
 */
const handleSubmit = async (

    event

) => {

    event.preventDefault();
    const validationErrors = validateQuestionForm(questionData);
    setErrors(validationErrors);
    if(Object.keys(validationErrors).length >0){
        return;
    }

    setLoading(

        true

    );

    const payload = {

        ...questionData,

        tags:

            questionData.tags

                .split(",")

                .map(

                    tag=>tag.trim()

                )

    };

    try {

        if (

            selectedQuestion

        ) {

            await updateQuestion(

                selectedQuestion.id,

                payload

            );

            toast.success(

                "Question updated successfully."

            );

        }

        else {

            await createQuestion(

                quizId,

                payload

            );

            toast.success(

                "Question added successfully."

            );

        }

        fetchQuestions();

        onClose();

    }

    catch (

        error

    ) {

        toast.error(

            getErrorMessage(

                error

            )

        );

    }

    finally {

        setLoading(

            false

        );

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

    <div className="question-drawer">

        <div className="drawer-header">

            <div className="drawer-title">

                <FaQuestionCircle />

                <h2>

                    {

                        selectedQuestion

                            ? "Edit Question"

                            : "Add Question"

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

        <form onSubmit={handleSubmit}>

            {/* Question */}

            <Input

                label="Question"

                name="question"

                value={questionData.question}

                placeholder="Enter question"

                onChange={handleInputChange}

                error = {errors.question}

            />

            {/* Question Type */}

            <div className="input-group">

                <label>

                    Question Type

                </label>

                <select

                    name="question_type"

                    value={questionData.question_type}
                    onChange={handleInputChange}

                >

                    {

                        questionTypes.map(

                            (type) => (

                                <option

                                    key={type}

                                    value={type}

                                >

                                    {

                                        type === "mcq"

                                            ? "MCQ"

                                            : "True / False"

                                    }

                                </option>

                            )

                        )

                    }

                </select>

            </div>

            {/* Options */}

            <h4>

                Options

            </h4>

            {

                questionData.options.map(

                    (option, index) => (

                        <div

                            key={index}

                            className="option-box"

                        >

                            <Input

                                label={`Option ${index + 1}`}

                                value={option}

                                onChange={(event) =>
                                    handleOptionChange(index,event.target.value)
                                }
                                disabled ={
                                    questionData.question_type ===
                                    "true_false"
                                }
                                error={
                                    errors[`option${index}`]
                                }

                            />

                        </div>

                    )

                )

            }

            {/* Correct Answer */}

            <div className="input-group">

                <label>

                    Correct Answer

                </label>

                <select

                    name="correct_answer"

                    value={questionData.correct_answer}

                    onChange={handleInputChange}

                >

                    <option value="">

                        Select Correct Answer

                    </option>

                    {

                        questionData.options.filter(
                            (option) => option.trim() !== ""
                        )
                        .map(
                            (option, index) => (
                                <option
                                   key={index}
                                   value={option}
                                >
                                    {option}
                                </option>
                        )
                    )
                }


                </select>
                {
                    errors.correct_answer && (
                        <p className="input-error">
                            {errors.correct_answer}
                        </p>    
                         )
                }

            </div>

            {/* Difficulty */}

            <div className="input-group">

                <label>

                    Difficulty

                </label>

                <select

                    name="difficulty"

                    value={questionData.difficulty}

                    onChange={handleInputChange}

                >

                    {

                        difficultyLevels.map(

                            (level) => (

                                <option

                                    key={level}

                                    value={level}

                                >

                                    {

                                        level.charAt(0)

                                            .toUpperCase()

                                        +

                                        level.slice(1)

                                    }

                                </option>

                            )

                        )

                    }

                </select>

            </div>

            {/* Tags */}

            <Input

                label="Tags"

                name="tags"

                value={questionData.tags}

                placeholder="Enter the relevant tags. For ex:-Java,OOP,Inheritance"

                onChange={handleInputChange}

                error={errors.tags}

            />

            {/* Marks */}

            <Input

                label="Marks"

                type="number"

                name="marks"

                value={questionData.marks}

                placeholder="Enter marks"

                onChange={handleInputChange}

                error={errors.marks}

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

                        selectedQuestion

                            ? "Update Question"

                            : "Save Question"

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

export default QuestionForm;