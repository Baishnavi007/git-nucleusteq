package com.baishnavi.advancedUserManagement.controller;

import com.baishnavi.advancedUserManagement.model.User;
import com.baishnavi.advancedUserManagement.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// Controller layer: handles the API requests
@RestController // returns JSON response
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // Basic API (for now returns all users)
    @GetMapping("/search")
    public List<User> getUsers() {

        return userService.getAllUsers();
    }
}