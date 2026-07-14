/**
 * Question List
 *
 * Responsibilities:
 * - Display all questions
 * - Search questions
 * - Show question details
 */

import {

    FaInbox,

    FaEdit,

    FaTrash

} from "react-icons/fa";

import "./QuestionList.css";
import { deleteQuestion } from "../../services/questionService";

import {toast} from "react-toastify"
import { getErrorMessage } from "../../utils/errorHandler";
import Swal from "sweetalert2";
function QuestionList({

    questions,

    searchText,

    onEdit,

    fetchQuestions

}) {
    /**
 * Delete Question.
 */
const handleDeleteQuestion = async (

    questionId

) => {

    const result = await Swal.fire({

        title: "Delete Question?",

        text: "This action cannot be undone.",

        icon: "warning",

        showCancelButton: true,

        confirmButtonColor: "#ef4444",

        cancelButtonColor: "#64748b",

        confirmButtonText: "Delete"

    });

    if (

        !result.isConfirmed

    ) {

        return;

    }

    try {

        await deleteQuestion(

            questionId

        );

        toast.success(

            "Question deleted successfully."

        );

        await fetchQuestions();

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

};

    /**
     * Filter questions according to search.
     */
    const filteredQuestions = questions.filter(

        (question) =>

            question.question

                .toLowerCase()

                .includes(

                    searchText.toLowerCase()

                )

    );

    return (

        <div className="question-table-container">

            <table className="question-table">

                <thead>

                    <tr>

                        <th>Question</th>

                        <th>Type</th>

                        <th>Difficulty</th>

                        <th>Marks</th>

                        <th>Correct Answer</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        filteredQuestions.length > 0 ?

                            filteredQuestions.map(

                                (question) => (

                                    <tr

                                        key={question.id}

                                    >

                                        <td>

                                            {question.question}

                                        </td>

                                        <td>

                                            {question.question_type}

                                        </td>

                                        <td>

                                            {question.difficulty}

                                        </td>

                                        <td>

                                            {question.marks}

                                        </td>

                                        <td>

                                            {question.correct_answer}

                                        </td>

                                        <td>

                                            <button

                                                className="edit-btn"

                                                onClick={() =>

                                                    onEdit(question)

                                                }

                                            >

                                                <FaEdit />

                                            </button>

                                            <button

                                                className="delete-btn"
                                                onClick={() =>
                                                    handleDeleteQuestion(question.id)
                                                }

                                            >

                                                <FaTrash />

                                            </button>

                                        </td>

                                    </tr>

                                )

                            )

                        :

                        <tr>

                            <td

                                colSpan="6"

                                className="empty-state"

                            >

                                <FaInbox />

                                <p>

                                    No questions found.

                                </p>

                            </td>

                        </tr>

                    }

                </tbody>

            </table>

        </div>

    );

}

export default QuestionList;