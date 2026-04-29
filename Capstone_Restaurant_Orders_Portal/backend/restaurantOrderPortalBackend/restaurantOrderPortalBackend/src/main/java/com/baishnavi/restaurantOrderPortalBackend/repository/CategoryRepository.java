package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Repository for Category entity
 */
public interface CategoryRepository extends JpaRepository<Category, Long> {

    /**
     * Get categories by restaurant
     */
    List<Category> findByRestaurantId(Long restaurantId);
}