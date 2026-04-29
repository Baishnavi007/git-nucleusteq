package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Cart;
import com.baishnavi.restaurantOrderPortalBackend.entity.CartItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

/**
 * Repository for CartItem entity
 */
public interface CartItemRepository extends JpaRepository<CartItem, Long> {
    /**
     * For deleting the cart items fully from DB
     * @param cart
     */
    @Modifying
    @Query("DELETE FROM CartItem c WHERE c.cart = :cart")
    void deleteByCart(Cart cart);
}