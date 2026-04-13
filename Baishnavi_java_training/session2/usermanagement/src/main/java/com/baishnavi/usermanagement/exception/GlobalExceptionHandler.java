package com.baishnavi.usermanagement.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// GlobalExceptionHandler: Handles the exception across the whole application
@RestControllerAdvice
public class GlobalExceptionHandler {

    // Handles the user not found exception
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<String> handleUserNotFoundException(UserNotFoundException ex) {

        return new ResponseEntity<>(ex.getMessage(), HttpStatus.NOT_FOUND);
    }
    @ExceptionHandler(InvalidMessageTypeException.class)
    public ResponseEntity<String> handleInvalidMessageType(InvalidMessageTypeException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }
}