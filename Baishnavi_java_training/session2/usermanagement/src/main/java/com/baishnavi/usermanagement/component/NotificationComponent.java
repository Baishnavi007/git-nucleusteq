package com.baishnavi.usermanagement.component;
import org.springframework.stereotype.Component;

// This class handles notification related logic
@Component //marks this class as reusable spring bean, managed by Spring (IoC)
public class NotificationComponent {

   // Method to send notification

    public String sendNotification() {
        return "Notification sent successfully!";
    }
}