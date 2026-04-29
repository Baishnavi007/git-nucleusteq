package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Cart;
import com.baishnavi.restaurantOrderPortalBackend.entity.CartItem;
import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.exception.BadRequestException;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.repository.CartItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.CartRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.MenuItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Optional;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Implementation of CartService.
 *
 * Handles:
 * - Add item to cart
 * - Fetch cart
 * - Clear cart
 *
 * Business Rules:
 * - One user = one cart
 * - Cart can contain items from only ONE restaurant
 */
@Service
public class CartServiceImpl implements CartService {

    private static final Logger logger =
            LoggerFactory.getLogger(CartServiceImpl.class);

    private final CartRepository cartRepository;
    private final CartItemRepository cartItemRepository;
    private final MenuItemRepository menuItemRepository;
    private final UserRepository userRepository;

    public CartServiceImpl(CartRepository cartRepository,
                           CartItemRepository cartItemRepository,
                           MenuItemRepository menuItemRepository,
                           UserRepository userRepository) {
        this.cartRepository = cartRepository;
        this.cartItemRepository = cartItemRepository;
        this.menuItemRepository = menuItemRepository;
        this.userRepository = userRepository;
    }

    /**
     * Add item to cart for logged-in user
     */
    @Override
    public Cart addItemToCart(Long menuItemId, Integer quantity) {

        if (quantity == null || quantity <= 0) {
            throw new BadRequestException("Quantity must be greater than zero");
        }

        User user = getLoggedInUser();

        logger.info("Adding item {} to cart for user {}", menuItemId, user.getEmail());

        Cart cart = cartRepository.findByUser(user)
                .orElseGet(() -> {
                    Cart newCart = new Cart();
                    newCart.setUser(user);
                    newCart.setTotalAmount(0.0);
                    newCart.setCartItems(new ArrayList<>());
                    return cartRepository.save(newCart);
                });

        if (cart.getCartItems() == null) {
            cart.setCartItems(new ArrayList<>());
        }

        MenuItem menuItem = menuItemRepository.findById(menuItemId)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Menu item not found"));

        /**
         * Same restaurant Validation
         */
        if (!cart.getCartItems().isEmpty()) {

            Long existingRestaurantId =
                    cart.getCartItems().get(0)
                            .getMenuItem()
                            .getCategory()
                            .getRestaurant()
                            .getId();

            Long newRestaurantId =
                    menuItem.getCategory()
                            .getRestaurant()
                            .getId();

            if (!existingRestaurantId.equals(newRestaurantId)) {
                throw new BadRequestException(
                        "You can order from only one restaurant at a time"
                );
            }
        }

        Optional<CartItem> existingItem =
                cart.getCartItems()
                        .stream()
                        .filter(item -> item.getMenuItem().getId().equals(menuItemId))
                        .findFirst();

        if (existingItem.isPresent()) {

            CartItem item = existingItem.get();
            item.setQuantity(item.getQuantity() + quantity);
            item.setPrice(item.getMenuItem().getPrice() * item.getQuantity());

            cartItemRepository.save(item);

        } else {

            CartItem newItem = new CartItem();
            newItem.setCart(cart);
            newItem.setMenuItem(menuItem);
            newItem.setQuantity(quantity);
            newItem.setPrice(menuItem.getPrice() * quantity);

            cartItemRepository.save(newItem);
            cart.getCartItems().add(newItem);
        }

        double total = cart.getCartItems()
                .stream()
                .mapToDouble(CartItem::getPrice)
                .sum();

        cart.setTotalAmount(total);

        return cartRepository.save(cart);
    }

    /**
     * Get current user's cart
     */
    @Override
    public Cart getCart() {

        User user = getLoggedInUser();

        return cartRepository.findByUser(user)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Cart not found"));
    }

    /**
     * Decrease item quantity
     */
    @Override
    public Cart decreaseItem(Long menuItemId) {

        Cart cart = getCart();

        CartItem item = cart.getCartItems()
                .stream()
                .filter(i -> i.getMenuItem().getId().equals(menuItemId))
                .findFirst()
                .orElseThrow(() ->
                        new ResourceNotFoundException("Item not found in cart"));

        item.setQuantity(item.getQuantity() - 1);

        if (item.getQuantity() <= 0) {
            cart.getCartItems().remove(item);
            cartItemRepository.delete(item);
        } else {
            item.setPrice(item.getMenuItem().getPrice() * item.getQuantity());
            cartItemRepository.save(item);
        }

        double total = cart.getCartItems()
                .stream()
                .mapToDouble(CartItem::getPrice)
                .sum();

        cart.setTotalAmount(total);

        return cartRepository.save(cart);
    }

    /**
     * Remove item completely from cart
     */
    @Override
    public Cart removeItem(Long menuItemId) {

        Cart cart = getCart();

        CartItem item = cart.getCartItems()
                .stream()
                .filter(i -> i.getMenuItem().getId().equals(menuItemId))
                .findFirst()
                .orElseThrow(() ->
                        new ResourceNotFoundException("Item not found"));

        cart.getCartItems().remove(item);
        cartItemRepository.delete(item);

        double total = cart.getCartItems()
                .stream()
                .mapToDouble(CartItem::getPrice)
                .sum();

        cart.setTotalAmount(total);

        return cartRepository.save(cart);
    }

    /**
     * Clear cart
     */
    @Override
    public void clearCart() {

        Cart cart = getCart();

        cartItemRepository.deleteAll(cart.getCartItems());

        cart.getCartItems().clear();

        cart.setTotalAmount(0.0);

        cartRepository.save(cart);

        logger.info("Cart cleared successfully");
    }

    /**
     * Get logged-in user
     */
    private User getLoggedInUser() {

        Authentication auth =
                SecurityContextHolder.getContext().getAuthentication();

        String email = auth.getName();

        return userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found"));
    }
}