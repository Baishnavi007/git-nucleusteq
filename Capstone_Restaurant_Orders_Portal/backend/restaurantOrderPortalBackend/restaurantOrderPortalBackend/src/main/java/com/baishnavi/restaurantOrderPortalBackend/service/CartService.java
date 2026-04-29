package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Cart;

/**
 * Service interface for Cart operations
 */
public interface CartService {

    /**
     * Add item to cart for logged-in user
     *
     * @param menuItemId menu item ID
     * @param quantity quantity to add
     * @return updated cart
     */
    Cart addItemToCart(Long menuItemId, Integer quantity);

    /**
     * Get current user's cart
     *
     * @return cart
     */
    Cart getCart();

    /**
     * Decrease quantity of item in cart
     */
    Cart decreaseItem(Long menuItemId);

    /**
     * Remove item completely from cart
     */
    Cart removeItem(Long menuItemId);
    /**
     * Clear cart
     */
    void clearCart();

}