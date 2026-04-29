package com.baishnavi.restaurantOrderPortalBackend.exception;

/**
 * Exception for bad request errors
 */
public class BadRequestException extends RuntimeException {

    /**
     * Constructor
     */
    public BadRequestException(String message) {
        super(message);
    }
}