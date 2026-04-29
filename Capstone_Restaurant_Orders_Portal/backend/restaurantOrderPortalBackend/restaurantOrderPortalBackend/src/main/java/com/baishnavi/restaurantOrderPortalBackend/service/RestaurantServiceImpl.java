package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.dto.CategoryResponse;
import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.enums.RestaurantStatus;
import com.baishnavi.restaurantOrderPortalBackend.repository.CategoryRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.MenuItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.RestaurantRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
/**
 * Service implementation for managing restaurant-related operations.
 *
 */
@Service
public class RestaurantServiceImpl implements RestaurantService {

    private final RestaurantRepository restaurantRepository;
    private final UserRepository userRepository;
    private final CategoryRepository categoryRepository;
    private final MenuItemRepository menuItemRepository;

    /**
     * Constructor for injecting required repositories.
     *
     * @param restaurantRepository repository for restaurant operations
     * @param userRepository       repository for user operations
     * @param categoryRepository   repository for category operations
     * @param menuItemRepository   repository for menu item operations
     */
    public RestaurantServiceImpl(RestaurantRepository restaurantRepository,
                                 UserRepository userRepository,
                                 CategoryRepository categoryRepository,
                                 MenuItemRepository menuItemRepository) {
        this.restaurantRepository = restaurantRepository;
        this.userRepository = userRepository;
        this.categoryRepository = categoryRepository;
        this.menuItemRepository = menuItemRepository;
    }

    /**
     * Creates a new restaurant.
     *
     * @param restaurant the restaurant entity to be created
     * @return saved restaurant entity
     */
    @Override
    public Restaurant createRestaurant(Restaurant restaurant) {
        return restaurantRepository.save(restaurant);
    }

    /**
     * Retrieves all restaurants from the database.
     *
     * @return list of all restaurants
     */
    @Override
    public List<Restaurant> getAllRestaurants() {
        return restaurantRepository.findAll();
    }

    /**
     * Retrieves all restaurants owned by the currently authenticated user.
     *
     * @return list of restaurants belonging to the logged-in owner
     */
    @Override
    public List<Restaurant> getMyRestaurants() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String email = authentication.getName();

        User owner = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        return restaurantRepository.findByOwner(owner);
    }
    /**
     * Updates the status of a specific restaurant.
     *
     * @param restaurantId the ID of the restaurant
     * @param status       new status value (must match RestaurantStatus enum)
     * @return updated restaurant entity
     */

    @Override
    public Restaurant updateStatus(Long restaurantId, String status) {
        Restaurant restaurant = restaurantRepository.findById(restaurantId)
                .orElseThrow(() -> new RuntimeException("Restaurant not found"));

        restaurant.setStatus(RestaurantStatus.valueOf(status));
        return restaurantRepository.save(restaurant);
    }

    /**
     * Searches restaurants by name using a keyword.
     *
     * @param keyword search keyword
     * @return list of matching restaurants
     */
    @Override
    public List<Restaurant> searchRestaurants(String keyword) {
        return restaurantRepository.findByNameContainingIgnoreCase(keyword);
    }

    /**
     * Retrieves menu grouped by categories for a specific restaurant.

     * @param restaurantId the ID of the restaurant
     * @return list of CategoryResponse containing category name and its items
     */
    @Override
    public List<CategoryResponse> getMenuByRestaurant(Long restaurantId) {

        List<Category> categories = categoryRepository.findByRestaurantId(restaurantId);
        List<CategoryResponse> response = new ArrayList<>();

        for (Category category : categories) {

            List<MenuItem> items =
                    menuItemRepository.findByCategoryIdAndIsAvailableTrue(category.getId());

            response.add(new CategoryResponse(
                    category.getName(),
                    items
            ));
        }

        return response;
    }
}