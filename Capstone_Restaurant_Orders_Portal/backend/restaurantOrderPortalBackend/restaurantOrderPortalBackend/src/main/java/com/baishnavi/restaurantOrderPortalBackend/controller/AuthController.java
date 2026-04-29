package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.*;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.enums.Role;
import com.baishnavi.restaurantOrderPortalBackend.mapper.UserMapper;
import com.baishnavi.restaurantOrderPortalBackend.service.UserService;

import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

/**
 * Controller for Authentication APIs
 */
@RestController
@RequestMapping("/auth")
public class AuthController {

    private static final Logger logger =
            LoggerFactory.getLogger(AuthController.class);

    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    /**
     * Register user
     */
    @PostMapping("/register")
    public UserDTO register(@Valid @RequestBody RegisterRequestDTO request) {

        logger.info("Register request for email: {}", request.getEmail());

        User user = new User();

        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setPhoneNumber(request.getPhoneNumber());
        user.setEmail(request.getEmail());
        user.setPassword(request.getPassword());
        user.setRole(Role.valueOf(request.getRole()));

        User saved = userService.registerUser(user);

        return UserMapper.toDTO(saved);
    }

    /**
     * Login user
     */
    @PostMapping("/login")
    public AuthResponseDTO login(@RequestBody AuthRequestDTO request) {

        logger.info("Login attempt for email: {}", request.getEmail());

        User user = userService.validateUser(
                request.getEmail(),
                request.getPassword()
        );

        String token = userService.generateToken(user);

        return new AuthResponseDTO(
                token,
                user.getRole().name(),
                user.getEmail()
        );
    }
}