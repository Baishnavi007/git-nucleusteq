package com.baishnavi.advancedUserManagement.controller;

import com.baishnavi.advancedUserManagement.model.User;
import com.baishnavi.advancedUserManagement.service.UserService;
import com.baishnavi.advancedUserManagement.exception.BadRequestException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// Controller layer: handles incoming HTTP requests and sends responses
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Constructor Injection (Dependency Injection)
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // GET API → Search users with optional filters
    // If no parameters → returns all users
    // If parameters provided → filters based on conditions
    @GetMapping("/search")
    public List<User> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role
    ) {
        return userService.searchUsers(name, age, role);
    }

    // POST API → Add a new user
    // Accepts JSON input using @RequestBody
    // Returns 201 status if user is created successfully
    @PostMapping("/submit")
    @ResponseStatus(HttpStatus.CREATED)
    public String submitUser(@RequestBody User user) {

        // Validate name (must not be null or empty)
        if (user.getName() == null || user.getName().trim().isEmpty()) {
            throw new BadRequestException("Name is required");
        }

        // Validate age (must be greater than 0)
        if (user.getAge() <= 0) {
            throw new BadRequestException("Valid age is required");
        }

        // Validate role (must not be null or empty)
        if (user.getRole() == null || user.getRole().trim().isEmpty()) {
            throw new BadRequestException("Role is required");
        }

        // Call service layer to save user
        userService.addUser(user);

        return "User created successfully";
    }
}