package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;
import com.baishnavi.restaurantOrderPortalBackend.service.RestaurantService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for Owner APIs
 */
@RestController
public class RestaurantController {

    private static final Logger logger =
            LoggerFactory.getLogger(RestaurantController.class);

    private final RestaurantService restaurantService;
    private final UserRepository userRepository;

    public RestaurantController(RestaurantService restaurantService,
                                UserRepository userRepository) {
        this.restaurantService = restaurantService;
        this.userRepository = userRepository;
    }

    /**
     * Create restaurant for logged-in owner
     */
    @PostMapping("/owner/restaurants")
    public Restaurant createRestaurant(@RequestBody Restaurant restaurant) {

        Authentication auth =
                SecurityContextHolder.getContext().getAuthentication();

        String email = auth.getName();

        logger.info("Creating restaurant for owner: {}", email);

        User owner = userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found"));

        restaurant.setOwner(owner);

        Restaurant saved = restaurantService.createRestaurant(restaurant);

        logger.info("Restaurant created with id: {}", saved.getId());

        return saved;
    }

    /**
     * Get all restaurants of logged-in owner
     */
    @GetMapping("/owner/restaurants")
    public List<Restaurant> getMyRestaurants() {

        logger.info("Fetching restaurants for owner");

        return restaurantService.getMyRestaurants();
    }

    /**
     * Update restaurant status
     */
    @PostMapping("/owner/restaurants/status")
    public Restaurant updateStatus(@RequestParam Long restaurantId,
                                   @RequestParam String status) {

        logger.info("Updating restaurant status: {}", restaurantId);

        return restaurantService.updateStatus(restaurantId, status);
    }
}