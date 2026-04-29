package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Repository for Restaurant entity
 */
public interface RestaurantRepository extends JpaRepository<Restaurant, Long> {

    /**
     * Find restaurants by city (case-insensitive)
     */
    List<Restaurant> findByCityIgnoreCase(String city);

    /**
     * Find restaurants by owner
     */
    List<Restaurant> findByOwner(User owner);

    /**
     * Search restaurants by name
     */
    List<Restaurant> findByNameContainingIgnoreCase(String name);
}