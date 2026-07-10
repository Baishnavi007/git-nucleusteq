/**
 * Assessment List
 *
 * Responsibilities:
 * - Display all quizzes
 * - Search quizzes
 * - Show quiz details
 */

import {
    FaInbox,
    FaCheckCircle,
    FaTimesCircle,
    FaEdit,
    FaTrash
} from "react-icons/fa";

import "./AssessmentList.css";
import { deleteQuiz, publishQuiz, unpublishQuiz } from "../../services/quizService";
import { toast } from "react-toastify";
import { getErrorMessage } from "../../utils/errorHandler";

import Swal from "sweetalert2";
function AssessmentList({

    quizzes,

    searchText,
    onEdit,
    fetchQuizzes

}) {
    const handleDeleteQuiz = async (

    quizId

) => {

    const result = await Swal.fire({
        title: "Delete Assessment?",
        text: "This action cannot be undone.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#ef4444",
        cancelButtonColor: "#64748b",
        confirmButtonText: "Delete"

    });
    if(!result.isConfirmed){
        return;
    }

    try {

        await deleteQuiz(quizId);

        toast.success(
            "Assessment deleted successfully."
        );

        await fetchQuizzes();

    }

    catch (error) {

        toast.error(
            getErrorMessage(error)
        );

    }

};
   /**
 * Publish / Unpublish assessment.
 */
    const handlePublishToggle = async (quiz) => {

    try {

        if (quiz.is_published) {

            await unpublishQuiz(

                quiz.id

            );

            toast.success(

                "Assessment unpublished successfully."

            );

        }

        else {

            await publishQuiz(

                quiz.id

            );

            toast.success(

                "Assessment published successfully."

            );

        }

        fetchQuizzes();

    }

    catch (error) {

        toast.error(

            getErrorMessage(error)

        );

    }

};

    /**
     * Filter quizzes according to search.
     */
    const filteredQuizzes = quizzes.filter(

        (quiz) =>

            quiz.title
                .toLowerCase()
                .includes(
                    searchText.toLowerCase()
                )

    );

    return (

        <div className="assessment-table-container">

            <table className="assessment-table">

                <thead>

                    <tr>

                        <th>Title</th>

                        <th>Category</th>

                        <th>Duration</th>

                        <th>Passing %</th>

                        <th>Questions</th>

                        <th>Status</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        filteredQuizzes.length > 0 ?

                            filteredQuizzes.map(

                                (quiz) => (

                                    <tr
                                        key={quiz.id}
                                    >

                                        <td>

                                            {quiz.title}

                                        </td>

                                        <td>

                                            {quiz.category_name}

                                        </td>

                                        <td>

                                            {quiz.duration} mins

                                        </td>

                                        <td>

                                            {quiz.passing_percentage}%

                                        </td>

                                        <td>

                                            {quiz.total_questions}

                                        </td>

                                        <td>
                                            <button className={
                                                quiz.is_published
                                                ? "published"
                                                : "unpublished"
                                            }

                                            onClick={() =>
                                                handlePublishToggle(
                                                    quiz
                                                )
                                            }
                                            >

                                            {

                                                quiz.is_published ?

                                                <>
                                                   <FaCheckCircle />
                                                   Published
                                                </>
                                                :
                                                <>
                                                   <FaTimesCircle />
                                                     Draft
                                                </> 
                                            }
                                            </button>
                                            </td>
                                            
                                        <td>

                                            <button
                                                className="edit-btn"
                                                onClick={() => onEdit(quiz)}
                                            >

                                                <FaEdit />

                                            </button>

                                            <button
                                                className="delete-btn"
                                                onClick={() =>
                                                    handleDeleteQuiz(quiz.id)
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
                                    colSpan="7"
                                    className="empty-state"
                                >

                                    <FaInbox />

                                    <p>

                                        No assessments found.

                                    </p>

                                </td>

                            </tr>

                    }

                </tbody>

            </table>

        </div>

    );

}

export default AssessmentList;