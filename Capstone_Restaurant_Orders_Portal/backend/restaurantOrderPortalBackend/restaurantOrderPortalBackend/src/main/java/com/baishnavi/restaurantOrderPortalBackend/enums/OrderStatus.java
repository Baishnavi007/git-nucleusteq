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
     * Restaurant accepted order
     */
    CONFIRMED,

    /**
     * Food is being prepared
     */
    PREPARING,

    /**
     * Out for delivery
     */
    OUT_FOR_DELIVERY,

    /**
     * Delivered to user
     */
    DELIVERED,

    /**
     * Cancelled order
     */
    CANCELLED
}