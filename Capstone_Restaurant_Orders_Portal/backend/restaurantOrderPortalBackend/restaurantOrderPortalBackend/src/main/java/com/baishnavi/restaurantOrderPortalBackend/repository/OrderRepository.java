package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Order;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Repository for Order entity
 */
public interface OrderRepository extends JpaRepository<Order, Long> {

    /**
     * Get all orders of a user
     *
     * @param user user entity
     * @return list of orders
     */
    List<Order> findByUser(User user);
}