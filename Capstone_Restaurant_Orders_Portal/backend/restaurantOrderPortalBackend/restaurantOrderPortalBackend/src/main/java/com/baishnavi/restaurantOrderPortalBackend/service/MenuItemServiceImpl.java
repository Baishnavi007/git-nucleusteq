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
 * Menu Item Service Class
 */
@Service
public class MenuItemServiceImpl implements MenuItemService {

    private final MenuItemRepository menuItemRepository;
    private final CategoryRepository categoryRepository;
    private final UserRepository userRepository;

    public MenuItemServiceImpl(MenuItemRepository menuItemRepository,
                               CategoryRepository categoryRepository,
                               UserRepository userRepository) {
        this.menuItemRepository = menuItemRepository;
        this.categoryRepository = categoryRepository;
        this.userRepository = userRepository;
    }

    /**
     * Add Menu Item
     * @param categoryId
     * @param name
     * @param description
     * @param price
     * @return
     */
    @Override
    public MenuItem addMenuItem(Long categoryId, String name, String description, Double price) {

        User user = getLoggedInUser();

        Category category = categoryRepository.findById(categoryId)
                .orElseThrow(() -> new ResourceNotFoundException("Category not found"));

        if (!category.getRestaurant().getOwner().getId().equals(user.getId())) {
            throw new RuntimeException("Unauthorized");
        }

        MenuItem item = new MenuItem();
        item.setName(name);
        item.setDescription(description);
        item.setPrice(price);
        item.setCategory(category);
        item.setRestaurant(category.getRestaurant());
        item.setIsAvailable(true);   // default ON
        item.setDeleted(false);

        return menuItemRepository.save(item);
    }

    /**
     * Get Menu Items
     * @param categoryId
     * @return menuItems
     */
    @Override
    public List<MenuItem> getAllMenuItems(Long categoryId) {
        return menuItemRepository.findByCategoryIdAndIsDeletedFalse(categoryId);
    }

    @Override
    public List<MenuItem> getAvailableMenuItems(Long categoryId) {
        return menuItemRepository.findByCategoryIdAndIsAvailableTrueAndIsDeletedFalse(categoryId);
    }

    /**
     * Update the Item Availability
     * @param itemId
     * @param isAvailable
     * @return
     */
    @Override
    public MenuItem updateAvailability(Long itemId, Boolean isAvailable) {

        MenuItem item = menuItemRepository.findById(itemId)
                .orElseThrow(() -> new ResourceNotFoundException("Item not found"));

        User user = getLoggedInUser();

        if (!item.getRestaurant().getOwner().getId().equals(user.getId())) {
            throw new RuntimeException("Unauthorized");
        }

        item.setIsAvailable(isAvailable);
        return menuItemRepository.save(item);
    }

    /**
     * Update Menu Item
     * @param itemId
     * @param name
     * @param description
     * @param price
     * @return
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
     * Delete Menu Item
     * @param itemId
     */
    @Override
    public void deleteMenuItem(Long itemId) {

        MenuItem item = menuItemRepository.findById(itemId)
                .orElseThrow(() -> new RuntimeException("Item not found"));

        User user = getLoggedInUser();

        if (!item.getRestaurant().getOwner().getId().equals(user.getId())) {
            throw new RuntimeException("Unauthorized");
        }

        item.setDeleted(true);

        item.setIsAvailable(false);

        menuItemRepository.save(item);
    }

    /**
     * Fetch logged-in user
     * @return
     */

    private User getLoggedInUser() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return userRepository.findByEmail(auth.getName())
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }
}