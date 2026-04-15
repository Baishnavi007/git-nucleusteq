package com.baishnavi.advancedUserManagement.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

// Handles exceptions globally
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BadRequestException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public String handleBadRequest(BadRequestException ex) {
        return ex.getMessage();
    }
}