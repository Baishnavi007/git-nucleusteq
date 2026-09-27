package com.baishnavi.usermanagement.service;

import com.baishnavi.usermanagement.component.MessageFormatter;
import com.baishnavi.usermanagement.exception.InvalidMessageTypeException;
import org.springframework.stereotype.Service;

import java.util.Map;


// Service which decides which formatter to use
@Service
public class MessageService {

    private final Map<String, MessageFormatter> formatterMap;

    // Constructor Injection
    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    // Get message based on type
    public String getMessage(String type) {

        // Handle null or empty input
        if (type == null || type.isBlank()) {
            throw new InvalidMessageTypeException("null/empty");
        }

        // Convert input to uppercase to match component keys
        MessageFormatter formatter = formatterMap.get(type.toUpperCase());

        // Handle invalid type
        if (formatter == null) {
            throw new InvalidMessageTypeException(type);
        }

        // Return formatted message
        return formatter.formatMessage();
    }
}