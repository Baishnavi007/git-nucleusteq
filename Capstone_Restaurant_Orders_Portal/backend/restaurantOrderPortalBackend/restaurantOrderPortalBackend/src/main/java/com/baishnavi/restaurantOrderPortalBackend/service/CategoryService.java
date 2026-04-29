package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Category;

import java.util.List;

/**
 * Service for Category operations
 */
public interface CategoryService {

    /**
     * Add category to a restaurant
     *
     * @param restaurantId restaurant ID
     * @param name category name
     * @return saved category
     */
    Category addCategory(Long restaurantId, String name);

    /**
     * Get categories of a restaurant
     *
     * @param restaurantId restaurant ID
     * @return list of categories
     */
    List<Category> getCategoriesByRestaurant(Long restaurantId);
}