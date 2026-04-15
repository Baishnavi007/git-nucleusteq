package com.baishnavi.advancedUserManagement.controller;

import com.baishnavi.advancedUserManagement.model.User;
import com.baishnavi.advancedUserManagement.service.UserService;
import com.baishnavi.advancedUserManagement.exception.BadRequestException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// Controller layer: Handles HTTP requests and returns responses
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Constructor-based Dependency Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // GET API: Search users based on optional filters
    // If no parameters are provided,returns all users
    // If parameters are provided,filters users accordingly
    @GetMapping("/search")
    public List<User> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role
    ) {
        return userService.searchUsers(name, age, role);
    }

    // POST API: Add a new user
    // Accepts JSON input using @RequestBody
    // Returns 201 (CREATED) on successful creation
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
        // Delegate user creation to service layer
        userService.addUser(user);

        return "User created successfully";
    }


    // DELETE API: Delete user only if confirm=true. If confirm is missing or false, do not delete
    @DeleteMapping("/{id}")
    public String deleteUser(
            @PathVariable int id,
            @RequestParam(required = false) Boolean confirm
    ) {


        // Check confirmation before deleting
        if (confirm == null || !confirm) {
            return "Confirmation required";
        }


        // Call service layer to delete user
        boolean deleted = userService.deleteUser(id);


        // Return appropriate response
        if (deleted) {
            return "User deleted successfully";
        } else {
            return "User not found";
        }
    }
}