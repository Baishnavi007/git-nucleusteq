package com.baishnavi.usermanagement.controller;

import com.baishnavi.usermanagement.service.NotificationService;
import org.springframework.web.bind.annotation.*;

// Controller for Notification APIs
@RestController
@RequestMapping("/notifications")
public class NotificationController {

    private final NotificationService notificationService;


   // Constructor Injection
    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }


    // API to trigger notification
    @GetMapping
    public String sendNotification() {
        return notificationService.triggerNotification();
    }
}