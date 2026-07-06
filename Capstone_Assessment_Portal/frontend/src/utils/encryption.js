/**
 * Utility functions for encrypting
 * sensitive data before sending it
 * to the backend.
 */

import JSEncrypt from "jsencrypt";


/**
 * Encrypt password using
 * the RSA public key.
 */
export const encryptPassword = (

    plainPassword,

    publicKey

) => {

    // Create RSA encryption instance.
    const rsaEncryptor = new JSEncrypt();

    // Load the public key received from backend.
    rsaEncryptor.setPublicKey(

        publicKey

    );

    // Encrypt the password.
    const encryptedValue = rsaEncryptor.encrypt(

        plainPassword

    );

    if (!encryptedValue) {

        throw new Error(

            "Unable to encrypt password."

        );

    }

    return encryptedValue;

};