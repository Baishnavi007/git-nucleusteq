package com.baishnavi.usermanagement.component;
import org.springframework.stereotype.Component;

@Component("LONG")

public class LongMessageFormatter implements MessageFormatter {

    @Override
    public String formatMessage() {
        return "Hi, your request has been processed successfully. Let us know if you need anything else.";
    }
}