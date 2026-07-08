"""
Database repository

Responsibilities:
- Handle all database operations.
- Keep database queries separate from business logic.
"""

from bson import ObjectId

from app.config.database import db
from app.utils.constants import QuizAttemptStatus

class Repository:
    """
    Handles database operations.
    """

    @staticmethod
    async def get_user_by_email(
            email: str
    ):
        """
        Retrieve user by email.
        """

        return await db.users.find_one(
            {
                "email": email
            }
        )

    @staticmethod
    async def get_user_by_username(
            username: str
    ):
        """
        Retrieve user by username.
        """

        return await db.users.find_one(
            {
                "username": username
            }
        )

    @staticmethod
    async def get_user_by_email_or_username(
            email_or_username: str
    ):
        """
        Retrieve user using email or username.
        """

        return await db.users.find_one(
            {
                "$or": [
                    {
                        "email": email_or_username
                    },
                    {
                        "username": email_or_username
                    }
                ]
            }
        )

    @staticmethod
    async def create_user(
            user_data: dict
    ):
        """
        Save new user.
        """

        return await db.users.insert_one(
            user_data
        )

    @staticmethod
    async def get_category_by_id(
            category_id: ObjectId
    ):
        """
        Retrieve category by id.
        """

        return await db.categories.find_one(
            {
                "_id": category_id
            }
        )

    @staticmethod
    async def get_category_by_name(
            name: str
    ):
        """
        Retrieve category by name.
        """

        return await db.categories.find_one(
            {
                "name": {
                    "$regex": f"^{name}$",
                    "$options": "i"
                }
            }
        )
    
    @staticmethod
    async def get_all_categories():
        """
        Retrieve all categories.
        """

        return await db.categories.find().to_list(
            length=None
        )
    
    @staticmethod
    async def create_category(
            category_data: dict
    ):
        """
        Save new category.
        """

        return await db.categories.insert_one(
            category_data
        )
    
    @staticmethod
    async def update_category(
            category_id: ObjectId,
            category_data: dict
    ):
        """
        Update an existing category.
        """

        return await db.categories.update_one(
            {
                "_id": category_id
            },
            {
                "$set": category_data
            }
        )
    
    @staticmethod
    async def delete_category(
            category_id: ObjectId
    ):
        """
        Delete a category.
        """

        return await db.categories.delete_one(
            {
                "_id": category_id
            }
        )
    
    @staticmethod
    async def get_duplicate_category(
            name: str,
            category_id: ObjectId
    ):
        """
        Retrieve duplicate category while updating.
        """

        return await db.categories.find_one(
            {
                "name": {
                    "$regex": f"^{name}$",
                    "$options": "i"
                },
                "_id": {
                    "$ne": category_id
                }
            }
        )

    @staticmethod
    async def get_quiz_by_title(
            title: str,
            category_id: str
    ):
        """
        Retrieve quiz by title within a category.
        """

        return await db.quizzes.find_one(
            {
                "title": {
                    "$regex": f"^{title}$",
                    "$options": "i"
                },
                "category_id": category_id
            }
        )
    @staticmethod
    async def get_duplicate_quiz(
            title: str,
            category_id: str,
            quiz_id: ObjectId
    ):
        """
        Retrieve duplicate quiz while updating.
        """

        return await db.quizzes.find_one(
            {
                "title": {
                    "$regex": f"^{title}$",
                    "$options": "i"
                },
                "category_id": category_id,
                "_id": {
                    "$ne": quiz_id
                }
            }
        )

    @staticmethod
    async def create_quiz(
            quiz_data: dict
    ):
        """
        Save new quiz.
        """

        return await db.quizzes.insert_one(
            quiz_data
        )

    @staticmethod
    async def get_quizzes_by_category(
            category_id: str
    ):
        """
        Retrieve all quizzes of a category.
        """

        return await db.quizzes.find(
            {
                "category_id": category_id
            }
        ).to_list(
            length=None
        )

    @staticmethod
    async def get_quiz_by_id(
            quiz_id: ObjectId
    ):
        """
        Retrieve quiz by id.
        """

        return await db.quizzes.find_one(
            {
                "_id": quiz_id
            }
        )

    @staticmethod
    async def update_quiz(
            quiz_id: ObjectId,
            quiz_data: dict
    ):
        """
        Update an existing quiz.
        """

        return await db.quizzes.update_one(
            {
                "_id": quiz_id
            },
            {
                "$set": quiz_data
            }
        )

    @staticmethod
    async def delete_quiz(
            quiz_id: ObjectId
    ):
        """
        Delete a quiz.
        """

        return await db.quizzes.delete_one(
            {
                "_id": quiz_id
            }
        )
    @staticmethod
    async def create_question(
            question_data: dict
    ):
        """
        Save new question.
        """

        return await db.questions.insert_one(
            question_data
        )

    @staticmethod
    async def get_question_by_id(
            question_id: ObjectId
    ):
        """
        Retrieve question by id.
        """

        return await db.questions.find_one(
            {
                "_id": question_id
            }
        )

    @staticmethod
    async def get_questions_by_quiz(
            quiz_id: str
    ):
        """
        Retrieve all questions of a quiz.
        """

        return await db.questions.find(
            {
                "quiz_id": quiz_id
            }
        ).to_list(
            length=None
        )

    @staticmethod
    async def update_quiz_statistics(
            quiz_id: ObjectId,
            total_questions: int,
            total_marks: int
    ):
        """
        Update total questions and total marks of a quiz.
        """

        return await db.quizzes.update_one(
            {
                "_id": ObjectId(quiz_id)
            },
            {
                "$set": {
                    "total_questions": total_questions,
                    "total_marks": total_marks
                }
            }
        )
    
    @staticmethod
    async def calculate_quiz_statistics(
            quiz_id: str
    ):
        """
        Calculate total questions and total marks of a quiz.
        """

        questions = await db.questions.find(
            {
                "quiz_id": quiz_id
            }
        ).to_list(
            length=None
        )

        total_questions = len(questions)
        total_marks = sum(
            question["marks"] for question in questions
        )

        return total_questions, total_marks

    @staticmethod
    async def get_duplicate_question(
            question: str,
            quiz_id: str
    ):
        """
        Retrieve duplicate question.
        """

        return await db.questions.find_one(
            {
                "question": question,
                "quiz_id": quiz_id
            }
        )
        

    @staticmethod
    async def get_duplicate_question_for_update(
            question: str,
            quiz_id: str,
            question_id: ObjectId
    ):
        """
        Retrieve duplicate question while updating.
        """

        return await db.questions.find_one(
            {
                "question": {
                    "$regex": f"^{question}$",
                    "$options": "i"
                },
                "quiz_id": quiz_id,
                "_id": {
                    "$ne": question_id
                }
            }
        )

    @staticmethod
    async def update_question(
            question_id: ObjectId,
            question_data: dict
    ):
        """
        Update an existing question.
        """

        return await db.questions.update_one(
            {
                "_id": question_id
            },
            {
                "$set": question_data
            }
        )

    @staticmethod
    async def delete_question(
            question_id: ObjectId
    ):
        """
        Delete a question.
        """

        return await db.questions.delete_one(
            {
                "_id": question_id
            }
        )
    
    @staticmethod
    async def delete_questions_by_quiz(
            quiz_id: str
    ):
        """
        Delete all questions of a quiz.
        """

        return await db.questions.delete_many(
            {
                "quiz_id": quiz_id
            }
        )


    @staticmethod
    async def publish_quiz(
            quiz_id: ObjectId
    ):
        """
        Publish a quiz.
        """

        return await db.quizzes.update_one(
            {
                "_id": quiz_id
            },
            {
                "$set": {
                    "is_published": True
                }
            }
        )
    
    @staticmethod
    async def unpublish_quiz(
            quiz_id: ObjectId
    ):
        """
        Unpublish a quiz.
        """

        return await db.quizzes.update_one(
            {
                "_id": quiz_id
            },
            {
                "$set": {
                    "is_published": False
                }
            }
        )

    @staticmethod
    async def get_published_quizzes_by_category(
            category_id: str
    ):
        """
        Retrieve all published quizzes of a category.
        """

        return await db.quizzes.find(
            {
                "category_id": category_id,
                "is_published": True
            }
        ).to_list(
            length=None
        )

    
    @staticmethod
    async def create_attempt(
            attempt_data: dict
    ):
        """
        Save new quiz attempt.
        """

        return await db.attempts.insert_one(
            attempt_data
        )
    
    @staticmethod
    async def get_attempt_by_id(
            attempt_id: ObjectId
    ):
        """
        Retrieve quiz attempt by id.
        """

        return await db.attempts.find_one(
            {
                "_id": attempt_id
            }
        )
    
    @staticmethod
    async def get_student_attempts(
            student_id: str,
            quiz_id: str
    ):
        """
        Retrieve all attempts of a student for a quiz.
        """

        return await db.attempts.find(
            {
                "student_id": student_id,
                "quiz_id": quiz_id
            }
        ).to_list(
            length=None
        )
    
    @staticmethod
    async def get_active_attempt(
            student_id: str,
            quiz_id: str
    ):
        """
        Retrieve active attempt of a student for a quiz.
        """

        return await db.attempts.find_one(
            {
                "student_id": student_id,
                "quiz_id": quiz_id,
                "status": QuizAttemptStatus.IN_PROGRESS
            }
        )
    
    @staticmethod
    async def update_attempt(
            attempt_id: ObjectId,
            attempt_data: dict
    ):
        """
        Update an existing quiz attempt.
        """

        return await db.attempts.update_one(
            {
                "_id": attempt_id
            },
            {
                "$set": attempt_data
            }
        )

    @staticmethod
    async def get_result_by_attempt_id(
        attempt_object_id: ObjectId
    ):
        """
        Retreive a submitted quiz attempt by ID.
        """
        return await db.attempts.find_one(
            {
                "_id": attempt_object_id,
                "status": {
                    "$in": [
                        QuizAttemptStatus.SUBMITTED,
                        QuizAttemptStatus.TIME_EXPIRED
                    ]
                }

            }
        )
    
    @staticmethod
    async def get_student_results(
        student_id: str
    ):
        """
        Retreive all submitted attempts of student
        """
        return await db.attempts.find(
            {
                "student_id": student_id,
                "status":{
                    "$in": [
                        QuizAttemptStatus.SUBMITTED,
                        QuizAttemptStatus.TIME_EXPIRED
                    ]
                }
            }
        ).to_list(
            length=None
        )
    
    @staticmethod
    async def get_all_results():
        """
        Retreive all submitted quiz attempts
        """

        return await db.attempts.find(
            {
                "status": {
                    "$in": [
                        QuizAttemptStatus.SUBMITTED,
                        QuizAttemptStatus.TIME_EXPIRED
                    ]
                }
            }
        ).to_list(
            length=None
        )
    