package com.baishnavi.todo.exception;

// Thrown when an invalid status value is provided
public class InvalidStatusException extends RuntimeException {

    public InvalidStatusException(String message) {
        super(message);
    }
}