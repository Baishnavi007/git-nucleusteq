package com.baishnavi.restaurantOrderPortalBackend.mapper;

import com.baishnavi.restaurantOrderPortalBackend.dto.CartDTO;
import com.baishnavi.restaurantOrderPortalBackend.dto.CartItemDTO;
import com.baishnavi.restaurantOrderPortalBackend.entity.Cart;
import com.baishnavi.restaurantOrderPortalBackend.entity.CartItem;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Mapper for Cart
 */
public class CartMapper {

    /**
     * Convert Cart → CartDTO
     */
    public static CartDTO toDTO(Cart cart) {

        List<CartItemDTO> items = cart.getCartItems()
                .stream()
                .map(CartMapper::toItemDTO)
                .collect(Collectors.toList());

        return new CartDTO(
                cart.getTotalAmount(),
                items
        );
    }

    /**
     * Convert CartItem → CartItemDTO
     */
    public static CartItemDTO toItemDTO(CartItem item) {
        return new CartItemDTO(
                item.getMenuItem().getName(),
                item.getQuantity(),
                item.getPrice()
        );
    }
}