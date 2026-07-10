/**
 * Validation utility functions.
 */

/**
 * Check whether email format is valid.
 */
const isEmailValid = (email) => {

    const emailRegex =

        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return emailRegex.test(email);

};

/**
 * Check whether password is strong.
 */
const isPasswordValid = (password) => {

    const passwordRegex =

        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

    return passwordRegex.test(password);

};
/**
 * Check whether name contains only alphabets.
 */
const isNameValid = (name) => {

    const nameRegex = /^[A-Za-z\s]+$/;

    return nameRegex.test(name);

};

/**
 * Validate required field.
 */
const validateRequiredField = (
    value,
    fieldName
) => {

    if (!value.trim()) {

        return `${fieldName} is required.`;

    }

    return "";

};


/**
 * Validate username.
 */
const validateUsername = (username) => {

    const requiredError = validateRequiredField(

        username,

        "Username"

    );

    if (requiredError) {

        return requiredError;

    }

    if (username.length < 3) {

        return "Username must contain at least 3 characters.";

    }

    return "";

};
/**
 * Validate first name / last name.
 */
const validateName = (
    name,
    fieldName
) => {

    const requiredError = validateRequiredField(

        name,

        fieldName

    );

    if (requiredError) {

        return requiredError;

    }

    if (!isNameValid(name)) {

        return `${fieldName} should contain only letters.`;

    }

    return "";

};

/**
 * Validate email.
 */
const validateEmail = (email) => {

    const requiredError = validateRequiredField(

        email,

        "Email"

    );

    if (requiredError) {

        return requiredError;

    }

    if (!isEmailValid(email)) {

        return "Please enter a valid email address.";

    }

    return "";

};

/**
 * Validate password.
 */
const validatePassword = (password) => {

    const requiredError = validateRequiredField(

        password,

        "Password"

    );

    if (requiredError) {

        return requiredError;

    }

    if (!isPasswordValid(password)) {

        return (

            "Password must contain at least 8 characters, " +

            "one uppercase letter, one lowercase letter " +

            "and one number."

        );

    }

    return "";

};

/**
 * Validate confirm password.
 */
const validateConfirmPassword = (
    password,
    confirmPassword
) => {

    const requiredError = validateRequiredField(

        confirmPassword,

        "Confirm Password"

    );

    if (requiredError) {

        return requiredError;

    }

    if (password !== confirmPassword) {

        return "Passwords do not match.";

    }

    return "";

};

/**
 * Add validation error.
 */
const addError = (
    errors,
    key,
    message
) => {

    if (message) {

        errors[key] = message;

    }

};

/**
 * Validate register form.
 */
export const validateRegisterForm = (
    formData
) => {

    const errors = {};

    addError(

        errors,

        "first_name",

        validateName(

            formData.first_name,

            "First Name"

        )

    );

    addError(

        errors,

        "last_name",

        validateName(

            formData.last_name,

            "Last Name"

        )

    );

    addError(

        errors,

        "username",

        validateUsername(

            formData.username

        )

    );

    addError(

        errors,

        "email",

        validateEmail(

            formData.email

        )

    );

    addError(

        errors,

        "password",

        validatePassword(

            formData.password

        )

    );

    addError(

        errors,

        "confirm_password",

        validateConfirmPassword(

            formData.password,

            formData.confirm_password

        )

    );

    return errors;

};

/**
 * Validate login form.
 */
export const validateLoginForm = (
    formData
) => {

    const errors = {};

    addError(

        errors,

        "email_or_username",

        validateRequiredField(

            formData.email_or_username,

            "Username / Email"

        )

    );

    addError(

        errors,

        "password",

        validateRequiredField(

            formData.password,

            "Password"

        )

    );

    return errors;

};

/**
 * Validate category name.
 */
const validateCategoryName = (name) => {

    const requiredError = validateRequiredField(

        name,

        "Category Name"

    );

    if (requiredError) {

        return requiredError;

    }

    if (!isNameValid(name)) {

        return "Category name should contain only letters.";

    }

    return "";

};

/**
 * Validate category description.
 */
const validateCategoryDescription = (description) => {

    const requiredError = validateRequiredField(

        description,

        "Description"

    );

    if (requiredError) {

        return requiredError;

    }

    if (/^\d+$/.test(description.trim())) {

        return "Description cannot contain only numbers.";

    }

    return "";

};

/**
 * Validate category form.
 */
export const validateCategoryForm = (formData) => {

    const errors = {};

    addError(

        errors,

        "name",

        validateCategoryName(

            formData.name

        )

    );

    addError(

        errors,

        "description",

        validateCategoryDescription(

            formData.description

        )

    );

    return errors;

};

/**
 * Validate quiz title.
 */
const validateQuizTitle = (title) => {

    const requiredError = validateRequiredField(

        title,

        "Quiz Title"

    );

    if (requiredError) {

        return requiredError;

    }

    if (title.trim().length < 3) {

        return "Quiz title must contain at least 3 characters.";

    }

    if (title.trim().length > 100) {

        return "Quiz title cannot exceed 100 characters.";

    }

    return "";

};

/**
 * Validate quiz description.
 */
const validateQuizDescription = (description) => {

    const requiredError = validateRequiredField(

        description,

        "Description"

    );

    if (requiredError) {

        return requiredError;

    }

    if (description.trim().length < 10) {

        return "Description must contain at least 10 characters.";

    }

    if (description.trim().length > 300) {

        return "Description cannot exceed 300 characters.";

    }

    return "";

};

/**
 * Validate duration.
 */
const validateDuration = (duration) => {

    if (!duration) {

        return "Duration is required.";

    }

    if (Number(duration) <= 0) {

        return "Duration must be greater than 0.";

    }

    return "";

};

/**
 * Validate passing percentage.
 */
const validatePassingPercentage = (percentage) => {

    if (!percentage) {

        return "Passing Percentage is required.";

    }

    if (

        Number(percentage) < 1 ||

        Number(percentage) > 100

    ) {

        return "Passing Percentage must be between 1 and 100.";

    }

    return "";

};

/**
 * Validate category.
 */
const validateCategory = (categoryId) => {

    if (!categoryId) {

        return "Category is required.";

    }

    return "";

};

/**
 * Validate assessment form.
 */
export const validateAssessmentForm = (

    formData

) => {

    const errors = {};

    addError(

        errors,

        "category_id",

        validateCategory(

            formData.category_id

        )

    );

    addError(

        errors,

        "title",

        validateQuizTitle(

            formData.title

        )

    );

    addError(

        errors,

        "description",

        validateQuizDescription(

            formData.description

        )

    );

    addError(

        errors,

        "duration",

        validateDuration(

            formData.duration

        )

    );

    addError(

        errors,

        "passing_percentage",

        validatePassingPercentage(

            formData.passing_percentage

        )

    );

    return errors;

};