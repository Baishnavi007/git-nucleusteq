package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Repository for Category entity
 */
public interface CategoryRepository extends JpaRepository<Category, Long> {

    /**
     * Get ONLY active (not deleted) categories by restaurant
     */
    List<Category> findByRestaurantIdAndIsDeletedFalse(Long restaurantId);

    /**
     * (Optional - for debug/admin)
     * Get all categories including deleted
     */
    List<Category> findByRestaurantId(Long restaurantId);
}