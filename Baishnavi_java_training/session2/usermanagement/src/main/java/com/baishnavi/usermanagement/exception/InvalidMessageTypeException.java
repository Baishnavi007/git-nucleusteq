package com.baishnavi.usermanagement.exception;

public class InvalidMessageTypeException extends RuntimeException {

    public InvalidMessageTypeException(String type) {
        super("Invalid message type: " + type + ". Allowed values are SHORT or LONG");
    }
}