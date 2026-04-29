package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Repository for MenuItem entity
 */
public interface MenuItemRepository extends JpaRepository<MenuItem, Long> {

    /**
     * OWNER: Get all items (including unavailable)
     */
    List<MenuItem> findByCategoryId(Long categoryId);

    /**
     * USER: Get only available items
     */
    List<MenuItem> findByCategoryIdAndIsAvailableTrue(Long categoryId);
}