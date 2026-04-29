package com.baishnavi.restaurantOrderPortalBackend.exception;

/**
 * Exception when resource is not found
 */
public class ResourceNotFoundException extends RuntimeException {

    /**
     * Constructor with message
     */
    public ResourceNotFoundException(String message) {
        super(message);
    }
}