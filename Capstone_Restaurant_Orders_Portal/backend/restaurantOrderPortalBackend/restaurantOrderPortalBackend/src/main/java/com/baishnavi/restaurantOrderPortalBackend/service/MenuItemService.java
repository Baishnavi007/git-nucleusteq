package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;

import java.util.List;

/**
 * Service for menu item operations
 */
public interface MenuItemService {

    /**
     * Add new menu item (OWNER)
     */
    MenuItem addMenuItem(Long categoryId,
                         String name,
                         String description,
                         Double price);

    /**
     * USER: Get only available items
     */
    List<MenuItem> getAvailableMenuItems(Long categoryId);

    /**
     * OWNER: Get all items
     */
    List<MenuItem> getAllMenuItems(Long categoryId);
    /**
     * OWNER: Update availability (ON/OFF)
     */
    MenuItem updateAvailability(Long itemId, Boolean isAvailable);

    /**
     * OWNER: Update menu
     */
    MenuItem updateMenuItem(Long itemId, String name, String description, Double price);

    /**
     * OWNER: Delete item from menu
     * @param itemId
     */
    void deleteMenuItem(Long itemId);
}