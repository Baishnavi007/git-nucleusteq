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

        validateRequiredField(

            formData.first_name,

            "First Name"

        )

    );

    addError(

        errors,

        "last_name",

        validateRequiredField(

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