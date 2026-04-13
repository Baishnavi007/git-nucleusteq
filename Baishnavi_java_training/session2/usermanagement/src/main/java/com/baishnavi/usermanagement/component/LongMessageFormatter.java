package com.baishnavi.usermanagement.component;
import org.springframework.stereotype.Component;

@Component("LONG")

public class LongMessageFormatter implements MessageFormatter {

    @Override
    public String formatMessage() {
        return "This is a detailed long message for the user.";
    }
}