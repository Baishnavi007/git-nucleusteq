package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.repository.CategoryRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.MenuItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Implementation of MenuItemService.
 *
 * Handles:
 * - Adding menu items (secure owner-based)
 * - Fetching menu items (filtered for user / full for owner)
 */
@Service
public class MenuItemServiceImpl implements MenuItemService {

    private final MenuItemRepository menuItemRepository;
    private final CategoryRepository categoryRepository;
    private final UserRepository userRepository;

    /**
     * Constructor injection
     */
    public MenuItemServiceImpl(MenuItemRepository menuItemRepository,
                               CategoryRepository categoryRepository,
                               UserRepository userRepository) {
        this.menuItemRepository = menuItemRepository;
        this.categoryRepository = categoryRepository;
        this.userRepository = userRepository;
    }

    /**
     * Add menu item (OWNER ONLY)
     */
    @Override
    public MenuItem addMenuItem(Long categoryId,
                                String name,
                                String description,
                                Double price) {

        // Logged-in user
        Authentication authentication =
                SecurityContextHolder.getContext().getAuthentication();

        String email = authentication.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        //  Category
        Category category = categoryRepository.findById(categoryId)
                .orElseThrow(() -> new RuntimeException("Category not found"));

        //  SECURITY CHECK
        if (!category.getRestaurant().getOwner().getId().equals(user.getId())) {
            throw new RuntimeException("You are not allowed to modify this restaurant");
        }

        //  Create item
        MenuItem item = new MenuItem();
        item.setName(name);
        item.setDescription(description);
        item.setPrice(price);
        item.setCategory(category);

        // Default availability
        item.setIsAvailable(true);

        return menuItemRepository.save(item);
    }

    /**
     * USER: Only available items
     */
    @Override
    public List<MenuItem> getAvailableMenuItems(Long categoryId) {
        return menuItemRepository.findByCategoryIdAndIsAvailableTrue(categoryId);
    }

    /**
     * OWNER: All items (even unavailable)
     */
    @Override
    public List<MenuItem> getAllMenuItems(Long categoryId) {
        return menuItemRepository.findByCategoryId(categoryId);
    }
    /**
     * OWNER: Toggle availability
     */
    @Override
    public MenuItem updateAvailability(Long itemId, Boolean isAvailable) {

        Authentication authentication =
                SecurityContextHolder.getContext().getAuthentication();

        String email = authentication.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        MenuItem item = menuItemRepository.findById(itemId)
                .orElseThrow(() -> new RuntimeException("Item not found"));


        if (!item.getCategory().getRestaurant().getOwner().getId().equals(user.getId())) {
            throw new RuntimeException("You are not allowed to modify this item");
        }

        item.setIsAvailable(isAvailable);

        return menuItemRepository.save(item);
    }
    /**
     * Update menu item details
     */
    @Override
    public MenuItem updateMenuItem(Long itemId, String name, String description, Double price) {

        MenuItem item = menuItemRepository.findById(itemId)
                .orElseThrow(() -> new ResourceNotFoundException("Menu item not found"));

        item.setName(name);
        item.setDescription(description);
        item.setPrice(price);

        return menuItemRepository.save(item);
    }

    /**
     * Delete menu item
     */
    @Override
    public void deleteMenuItem(Long itemId) {

        MenuItem item = menuItemRepository.findById(itemId)
                .orElseThrow(() -> new ResourceNotFoundException("Menu item not found"));

        menuItemRepository.delete(item);
    }
}