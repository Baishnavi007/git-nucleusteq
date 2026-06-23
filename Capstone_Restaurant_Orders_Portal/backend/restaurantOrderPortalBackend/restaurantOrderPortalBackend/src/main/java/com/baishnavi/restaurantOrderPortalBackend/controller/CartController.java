package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.CartDTO;
import com.baishnavi.restaurantOrderPortalBackend.mapper.CartMapper;
import com.baishnavi.restaurantOrderPortalBackend.service.CartService;

import org.springframework.web.bind.annotation.*;

/**
 * Controller for Cart APIs
 */
@RestController
@RequestMapping("/cart")
public class CartController {

    private final CartService cartService;

    public CartController(CartService cartService) {
        this.cartService = cartService;
    }


    /**
     * Add item to cart
     */
    @PostMapping("/add")
    public CartDTO addToCart(@RequestParam Long menuItemId,
                             @RequestParam Integer quantity) {
        return CartMapper.toDTO(
                cartService.addItemToCart(menuItemId, quantity)
        );
    }

    /**
     * Get cart
     */
    @GetMapping
    public CartDTO getCart() {
        return CartMapper.toDTO(
                cartService.getCart()
        );
    }

    /**
     * Decrease item quantity
     */
    @PostMapping("/decrease")
    public CartDTO decrease(@RequestParam Long menuItemId) {
        return CartMapper.toDTO(
                cartService.decreaseItem(menuItemId)
        );
    }

    /**
     * Remove item from cart
     */
    @DeleteMapping("/remove")
    public CartDTO remove(@RequestParam Long menuItemId) {
        return CartMapper.toDTO(
                cartService.removeItem(menuItemId)
        );
    }

    /**
     * Clear cart
     */
    @DeleteMapping("/clear")
    public String clearCart() {
        cartService.clearCart();
        return "Cart cleared successfully ";
    }
}