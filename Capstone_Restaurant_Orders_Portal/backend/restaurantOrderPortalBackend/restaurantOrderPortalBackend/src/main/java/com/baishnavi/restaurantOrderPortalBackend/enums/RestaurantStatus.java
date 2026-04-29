package com.baishnavi.restaurantOrderPortalBackend.enums;

/**
 * Enum representing the status of a restaurant.
 * Defines whether the restaurant is operational or not.
 */
public enum RestaurantStatus {

    /**
     * Restaurant is open and accepting orders.
     */
    OPEN,

    /**
     * Restaurant is closed.
     */
    CLOSED,

    /**
     * Restaurant is temporarily closed.
     */
    TEMP_CLOSED
}