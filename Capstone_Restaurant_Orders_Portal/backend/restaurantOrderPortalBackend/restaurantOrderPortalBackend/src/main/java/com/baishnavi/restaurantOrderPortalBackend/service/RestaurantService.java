package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.dto.CategoryResponse;
import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * Service interface for handling restaurant-related operations.
 */
public interface RestaurantService {

    /**
     * Creates a new restaurant.
     *
     * @param restaurant the restaurant entity to be created
     * @return the saved restaurant entity
     */
    Restaurant createRestaurant(Restaurant restaurant, MultipartFile image);

    /**
     * Retrieves all restaurants available in the system.
     *
     * @return list of all restaurants
     */
    List<Restaurant> getAllRestaurants();

    /**
     * Retrieves all restaurants owned by the currently authenticated user.
     *
     * @return list of restaurants belonging to the logged-in owner
     */
    List<Restaurant> getMyRestaurants();

    /**
     * Updates the status of a specific restaurant.
     *
     * @param restaurantId the ID of the restaurant
     * @param status       the new status value (e.g., OPEN, CLOSED)
     * @return updated restaurant entity
     */
    Restaurant updateStatus(Long restaurantId, String status);

    /**
     * Searches for restaurants based on a keyword.
     *
     * @param keyword the search keyword
     * @return list of matching restaurants
     */
    List<Restaurant> searchRestaurants(String keyword);

    /**
     * Retrieves the menu of a specific restaurant grouped by categories.
     *
     * @param restaurantId the ID of the restaurant
     * @return list of CategoryResponse containing categories and their menu items
     */
    List<CategoryResponse> getMenuByRestaurant(Long restaurantId);

    void deleteRestaurant(Long restaurantId);
}