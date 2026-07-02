/**
 * Axios Configuration
 *
 * Responsibilities:
 * - Configure Axios instance
 * - Set backend base URL
 * - Attach JWT token to every request
 */

import axios from "axios";

/**
 * Axios instance
 */
const api = axios.create({

    baseURL: "http://127.0.0.1:8000",

    headers: {

        "Content-Type": "application/json"

    }

});


/**
 * Request Interceptor
 *
 * Automatically attaches the JWT access token
 * to every outgoing request.
 */
api.interceptors.request.use(

    (config) => {

        /**
         * Retrieve token from localStorage.
         */
        const accessToken = localStorage.getItem(
            "access_token"
        );

        /**
         * If token exists,
         * attach it to Authorization header.
         */
        if (accessToken) {

            config.headers.Authorization =
                `Bearer ${accessToken}`;

        }

        return config;

    },

    (error) => {

        return Promise.reject(error);

    }

);

export default api;