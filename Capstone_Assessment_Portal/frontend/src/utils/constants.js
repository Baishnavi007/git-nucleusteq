/**
 * API Endpoints
 */

export const API_ENDPOINTS = {

    AUTH: {
        LOGIN: "/auth/login",
        REGISTER: "/auth/register",
        PUBLIC_KEY: "/auth/public-key",
    },

};
/**
 * Application constants.
 */

/**
 * Frontend validation messages.
 */
export const ValidationMessage = {

    FIRST_NAME_REQUIRED:
        "First Name is required.",

    LAST_NAME_REQUIRED:
        "Last Name is required.",

    USERNAME_REQUIRED:
        "Username is required.",

    USERNAME_MIN_LENGTH:
        "Username must contain at least 3 characters.",

    EMAIL_REQUIRED:
        "Email is required.",

    INVALID_EMAIL:
        "Please enter a valid email address.",

    PASSWORD_REQUIRED:
        "Password is required.",

    INVALID_PASSWORD:
        "Password must contain at least 8 characters, one uppercase letter, one lowercase letter and one number.",

    CONFIRM_PASSWORD_REQUIRED:
        "Confirm Password is required.",

    PASSWORD_MISMATCH:
        "Passwords do not match."

};

/**
 * API error messages.
 */
export const ApiErrorMessage = {

    DEFAULT:
        "Something went wrong.",

    REQUIRED:
        "is required.",

    ONLY_LETTERS:
        "should contain only letters.",

    TOO_SHORT:
        "is too short.",

    TOO_LONG:
        "is too long.",

    INVALID_EMAIL:
        "Please enter a valid email address."

};