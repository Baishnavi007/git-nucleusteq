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
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Service implementation for managing restaurant-related operations.
 */
@Service
public class RestaurantServiceImpl implements RestaurantService {

    private final RestaurantRepository restaurantRepository;
    private final UserRepository userRepository;
    private final CategoryRepository categoryRepository;
    private final MenuItemRepository menuItemRepository;

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
     * Create restaurant with optional image upload
     */
    @Override
    public Restaurant createRestaurant(Restaurant restaurant, MultipartFile image) {

        try {

            if (image != null && !image.isEmpty()) {

                String fileName = System.currentTimeMillis() + "_" + image.getOriginalFilename();

                Path uploadPath = Paths.get("uploads/");

                if (!Files.exists(uploadPath)) {
                    Files.createDirectories(uploadPath);
                }

                Path filePath = uploadPath.resolve(fileName);

                Files.write(filePath, image.getBytes());

                restaurant.setImageUrl("http://localhost:8080/uploads/" + fileName);

            } else {

                restaurant.setImageUrl(
                        "https://images.unsplash.com/photo-1414235077428-338989a2e8c0"
                );
            }

            return restaurantRepository.save(restaurant);

        } catch (IOException e) {
            throw new RuntimeException("Image upload failed");
        }
    }

    /**
     * Get all restaurants
     */
    @Override
    public List<Restaurant> getAllRestaurants() {
        return restaurantRepository.findAll();
    }

    /**
     * Get restaurants of logged-in owner
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
     * Update restaurant status
     */
    @Override
    public Restaurant updateStatus(Long restaurantId, String status) {

        Restaurant restaurant = restaurantRepository.findById(restaurantId)
                .orElseThrow(() -> new RuntimeException("Restaurant not found"));

        restaurant.setStatus(RestaurantStatus.valueOf(status));

        return restaurantRepository.save(restaurant);
    }

    /**
     * Search restaurants
     */
    @Override
    public List<Restaurant> searchRestaurants(String keyword) {
        return restaurantRepository.findByNameContainingIgnoreCase(keyword);
    }

    /**
     * Delete Restaurant
     * @param restaurantId
     */
    @Override
    public void deleteRestaurant(Long restaurantId) {

        Restaurant restaurant = restaurantRepository.findById(restaurantId)
                .orElseThrow(() -> new RuntimeException("Restaurant not found"));

        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String email = auth.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        if (!restaurant.getOwner().getId().equals(user.getId())) {
            throw new RuntimeException("You are not allowed to delete this restaurant");
        }

        List<Category> categories = categoryRepository.findByRestaurantIdAndIsDeletedFalse(restaurantId);

        for (Category category : categories) {

            List<MenuItem> items = menuItemRepository.findByCategory(category);
            menuItemRepository.deleteAll(items);

            categoryRepository.delete(category);
        }

        restaurantRepository.delete(restaurant);
    }
    /**
     * Get menu grouped by category
     */
    @Override
    public List<CategoryResponse> getMenuByRestaurant(Long restaurantId) {

        List<Category> categories = categoryRepository.findByRestaurantIdAndIsDeletedFalse(restaurantId);
        List<CategoryResponse> response = new ArrayList<>();

        for (Category category : categories) {

            List<MenuItem> items =
                    menuItemRepository.findByCategoryIdAndIsAvailableTrueAndIsDeletedFalse(category.getId());

            response.add(new CategoryResponse(
                    category.getName(),
                    items
            ));
        }

        return response;
    }
}