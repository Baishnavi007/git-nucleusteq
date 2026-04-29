package com.baishnavi.restaurantOrderPortalBackend.constants;

/**
 * Application level constants
 */
public class AppConstants {

    /**
     * Default wallet balance for new users
     */
    public static final int DEFAULT_WALLET_BALANCE = 1000;

    /**
     * JWT expiration time (24 hours)
     */
    public static final long JWT_EXPIRATION_MS = 86400000;
    /**
     * Order cancel time limit
     */
    public static final long ORDER_CANCEL_TIME_SECONDS = 30;
}