package com.baishnavi.usermanagement.service;

import com.baishnavi.usermanagement.component.NotificationComponent;
import org.springframework.stereotype.Service;

// Service layer for notification use case
@Service
public class NotificationService {

    private final NotificationComponent notificationComponent;

    // Constructor Injection
    public NotificationService(NotificationComponent notificationComponent) {
        this.notificationComponent = notificationComponent;
    }

    // Trigger notification
    public String triggerNotification() {

        return notificationComponent.sendNotification();
    }

}
