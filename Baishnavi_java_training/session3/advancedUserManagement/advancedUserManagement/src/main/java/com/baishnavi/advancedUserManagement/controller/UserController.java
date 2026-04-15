package com.baishnavi.advancedUserManagement.controller;

import com.baishnavi.advancedUserManagement.model.User;
import com.baishnavi.advancedUserManagement.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// Controller layer: handles API requests
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // Search API with filters
    @GetMapping("/search")
    public List<User> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role
    ) {
        return userService.searchUsers(name, age, role);
    }
}