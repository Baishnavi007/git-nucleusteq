package com.baishnavi.todo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

// Dummy external service to simulate notification sending
@Component
public class NotificationServiceClient {

    private static final Logger logger = LoggerFactory.getLogger(NotificationServiceClient.class);

    // Simulate sending notification
    public void sendNotification(String message) {
        logger.info("Notification sent: {}", message);
    }
}