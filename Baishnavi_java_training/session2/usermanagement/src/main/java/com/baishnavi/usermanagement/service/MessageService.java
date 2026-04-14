package com.baishnavi.usermanagement.service;
import com.baishnavi.usermanagement.component.MessageFormatter;
import com.baishnavi.usermanagement.exception.InvalidMessageTypeException;
import org.springframework.stereotype.Service;
import java.util.Map;

// Service which decides which formatter to use
@Service
public class MessageService {

    private final Map<String, MessageFormatter> formatterMap;


    // Spring injects all formatter components automatically
    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    //Get message based on type
    public String getMessage(String type) {

        MessageFormatter formatter = formatterMap.get(type.toUpperCase());
        if (formatter == null) {
            throw new InvalidMessageTypeException(type);
        }

        return formatter.formatMessage();
    }
}