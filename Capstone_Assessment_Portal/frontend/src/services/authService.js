/**
 * Authentication APIs
 */

import api from "./api";
import { API_ENDPOINTS } from "../utils/constants";

/**
 * Login API
 */

export const loginUser = async (loginData) => {

    const response = await api.post(

        API_ENDPOINTS.AUTH.LOGIN,

        loginData

    );

    return response.data;

};


/**
 * Register API
 */

export const registerUser = async (registerData) => {

    const response = await api.post(

        API_ENDPOINTS.AUTH.REGISTER,

        registerData

    );

    return response.data;

};
/**
 * Fetch RSA public key
 */

export const getPublicKey = async () => {

    const response = await api.get(

        API_ENDPOINTS.AUTH.PUBLIC_KEY

    );

    return response.data;

};