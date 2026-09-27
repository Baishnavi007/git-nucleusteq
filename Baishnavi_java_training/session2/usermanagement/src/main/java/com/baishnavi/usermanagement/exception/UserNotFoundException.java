
package com.baishnavi.usermanagement.exception;

// Custom Exception : defines the error and GlobalExceptionHandler handles it centrally to return a proper response

public class UserNotFoundException extends RuntimeException {

    public UserNotFoundException(String message) {
        super(message);
    }
}