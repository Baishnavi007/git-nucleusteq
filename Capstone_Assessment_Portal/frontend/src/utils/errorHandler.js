/**
 * Error handling utility.
 */

import {

    ApiErrorMessage

} from "./constants";

/**
 * Returns a user-friendly error
 * message from backend responses.
 */
export const getErrorMessage = (error) => {

    const detail = error.response?.data?.detail;

    /**
     * Handle custom exceptions
     * returned by backend.
     */
    if (!Array.isArray(detail)) {

        return (

            detail ||

            ApiErrorMessage.DEFAULT

        );

    }

    /**
     * Handle FastAPI validation errors.
     */
    const validationError = detail[0];

    const field = validationError.loc[1]

        .replace("_", " ");

    switch (validationError.type) {

        case "missing":

            return `${field} ${ApiErrorMessage.REQUIRED}`;

        case "string_pattern_mismatch":

            return `${field} ${ApiErrorMessage.ONLY_LETTERS}`;

        case "string_too_short":

            return `${field} ${ApiErrorMessage.TOO_SHORT}`;

        case "string_too_long":

            return `${field} ${ApiErrorMessage.TOO_LONG}`;

        case "value_error":

            return ApiErrorMessage.INVALID_EMAIL;

        default:

            return validationError.msg;

    }

};