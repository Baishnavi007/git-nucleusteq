package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Order;

import java.util.List;

/**
 * Service for order operations
 */
public interface OrderService {

    /**
     * Place order from cart
     *
     * @return created order
     */
    Order placeOrder();

    /**
     * Get all orders of logged-in user
     *
     * @return list of orders
     */
    List<Order> getMyOrders();

    /**
     * Update order status
     */
    Order updateOrderStatus(Long orderId, String status);

    /**
     * Cancel order by user
     */
    Order cancelOrder(Long orderId);
    /**
     * Get order status by ID
     *
     * @param orderId order ID
     * @return status string
     */
    String getOrderStatus(Long orderId);
}