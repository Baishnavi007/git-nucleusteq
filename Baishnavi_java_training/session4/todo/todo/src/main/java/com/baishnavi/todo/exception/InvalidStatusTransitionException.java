package com.baishnavi.todo.exception;

// Thrown when invalid status transition is attempted
public class InvalidStatusTransitionException extends RuntimeException {

    public InvalidStatusTransitionException(String message) {
        super(message);
    }
}