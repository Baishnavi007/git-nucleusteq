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
const BASE_URL = import.meta.env.VITE_API_URL;
const api = axios.create({

    baseURL: BASE_URL,

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