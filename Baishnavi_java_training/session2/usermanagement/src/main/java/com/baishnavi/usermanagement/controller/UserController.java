package com.baishnavi.usermanagement.controller;

import com.baishnavi.usermanagement.model.User;
import com.baishnavi.usermanagement.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

//Controller Layer: Handles HTTP requests and returns responses

@RestController // Converts response to JSON automatically
@RequestMapping("/users") // Base url
public class UserController {

    private final UserService userService;
    // Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }


     //GET /users: used to fetch all users

    @GetMapping // API Endpoint
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }


     // POST /users: creating new user

    @PostMapping // API Endpoint
    public User createUser(@RequestBody User user) {
        return userService.createUser(user);
    }


     // GET /users/{id} → retrieving the user by ID

    @GetMapping("/{id}") // API Endpoint
    public User getUserById(@PathVariable int id) {
        return userService.getUserById(id);
    }
}