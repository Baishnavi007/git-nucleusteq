package com.baishnavi.restaurantOrderPortalBackend.enums;

/**
 * Enum representing order lifecycle stages
 */
public enum OrderStatus {

    /**
     * Order placed by user
     */
    PLACED,

    /**
     * Order accepted by restaurant
     */
    PENDING,

    /**
     * Delivered to user
     */
    DELIVERED,

    /**
     * Order completed
     */
    COMPLETED,

    /**
     * Cancelled order
     */
    CANCELLED
}