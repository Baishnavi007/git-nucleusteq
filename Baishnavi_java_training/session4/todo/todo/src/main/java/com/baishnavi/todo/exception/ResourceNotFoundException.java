package com.baishnavi.todo.exception;

// Thrown when a resource is not found in DB
public class ResourceNotFoundException extends RuntimeException {

    public ResourceNotFoundException(String message) {
        super(message);
    }
}