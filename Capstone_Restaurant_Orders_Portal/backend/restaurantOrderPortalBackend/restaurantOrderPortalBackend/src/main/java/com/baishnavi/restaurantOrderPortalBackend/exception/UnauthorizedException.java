package com.baishnavi.restaurantOrderPortalBackend.exception;

/**
 * Exception for unauthorized access
 */
public class UnauthorizedException extends RuntimeException {

    /**
     * Constructor with message
     */
    public UnauthorizedException(String message) {
        super(message);
    }
}