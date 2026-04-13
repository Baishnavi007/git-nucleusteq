package com.baishnavi.usermanagement.controller;

import com.baishnavi.usermanagement.service.MessageService;
import org.springframework.web.bind.annotation.*;

//Controller for managing message APIs
@RestController
@RequestMapping("/message")
public class MessageController {

    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }


    @GetMapping
    public String getMessage(@RequestParam String type) {
        return messageService.getMessage(type);
    }
}