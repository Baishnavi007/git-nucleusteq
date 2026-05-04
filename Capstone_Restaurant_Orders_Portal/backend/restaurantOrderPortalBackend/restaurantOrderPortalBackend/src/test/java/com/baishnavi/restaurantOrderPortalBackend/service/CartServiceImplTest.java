package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.*;
import com.baishnavi.restaurantOrderPortalBackend.exception.BadRequestException;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.repository.CartItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.CartRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.MenuItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CartServiceImplTest {

    @Mock
    private CartRepository cartRepository;

    @Mock
    private CartItemRepository cartItemRepository;

    @Mock
    private MenuItemRepository menuItemRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private SecurityContext securityContext;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private CartServiceImpl cartService;

    private User user;
    private Cart cart;
    private MenuItem menuItem;
    private CartItem cartItem;

    @BeforeEach
    void setUp() {
        SecurityContextHolder.setContext(securityContext);

        user = new User();
        user.setId(1L);
        user.setEmail("test@example.com");

        Restaurant restaurant = new Restaurant();
        restaurant.setId(1L);

        Category category = new Category();
        category.setRestaurant(restaurant);

        menuItem = new MenuItem();
        menuItem.setId(10L);
        menuItem.setPrice(100.0);
        menuItem.setCategory(category);

        cart = new Cart();
        cart.setId(1L);
        cart.setUser(user);
        cart.setTotalAmount(0.0);
        cart.setCartItems(new ArrayList<>());

        cartItem = new CartItem();
        cartItem.setId(1L);
        cartItem.setCart(cart);
        cartItem.setMenuItem(menuItem);
        cartItem.setQuantity(1);
        cartItem.setPrice(100.0);
    }

    private void mockSecurity() {
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn("test@example.com");
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
    }

    @Test
    void addItemToCart_success_newItem() {
        mockSecurity();
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(menuItemRepository.findById(10L)).thenReturn(Optional.of(menuItem));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.addItemToCart(10L, 2);

        assertNotNull(updatedCart);
        verify(cartItemRepository).save(any(CartItem.class));
        verify(cartRepository).save(cart);
    }

    @Test
    void addItemToCart_invalidQuantity() {
        assertThrows(BadRequestException.class, () -> cartService.addItemToCart(10L, 0));
    }

    @Test
    void getCart_success() {
        mockSecurity();
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));

        Cart foundCart = cartService.getCart();

        assertNotNull(foundCart);
    }

    @Test
    void decreaseItem_success() {
        mockSecurity();
        cart.getCartItems().add(cartItem);
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.decreaseItem(10L);

        assertTrue(updatedCart.getCartItems().isEmpty());
        verify(cartItemRepository).delete(cartItem);
    }

    @Test
    void removeItem_success() {
        mockSecurity();
        cart.getCartItems().add(cartItem);
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.removeItem(10L);

        assertTrue(updatedCart.getCartItems().isEmpty());
        verify(cartItemRepository).delete(cartItem);
    }

    @Test
    void clearCart_success() {
        mockSecurity();
        cart.getCartItems().add(cartItem);
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));

        cartService.clearCart();

        assertTrue(cart.getCartItems().isEmpty());
        assertEquals(0.0, cart.getTotalAmount());
        verify(cartItemRepository).deleteAll(anyList());
        verify(cartRepository).save(cart);
    }
}