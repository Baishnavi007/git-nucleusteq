/**
 * Authentication APIs
 */

import api from "./api";


/**
 * Login API
 */

export const loginUser = async (loginData) => {

    const response = await api.post(

        "/auth/login",

        loginData

    );

    return response.data;

};


/**
 * Register API
 */

export const registerUser = async (registerData) => {

    const response = await api.post(

        "/auth/register",

        registerData

    );

    return response.data;

};
/**
 * Fetch RSA public key
 */

export const getPublicKey = async () => {

    const response = await api.get(

        "/auth/public-key"

    );

    return response.data;

};