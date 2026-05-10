package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.OrderItem;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Repository for OrderItem Entity
 */
public interface OrderItemRepository extends JpaRepository<OrderItem, Long> {
}