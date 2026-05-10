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
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
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
    }

    @Test
    void addItemToCart_success_newItem() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(menuItemRepository.findById(10L)).thenReturn(Optional.of(menuItem));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.addItemToCart(10L, 2);

        assertNotNull(updatedCart);
        verify(cartItemRepository).save(any(CartItem.class));
        verify(cartRepository).save(cart);
    }

    @Test
    void addItemToCart_createNewCart() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.empty());
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);
        when(menuItemRepository.findById(10L)).thenReturn(Optional.of(menuItem));

        Cart updatedCart = cartService.addItemToCart(10L, 1);

        assertNotNull(updatedCart);
        verify(cartRepository, times(2)).save(any(Cart.class));
    }

    @Test
    void addItemToCart_existingItem() {
        mockSecurity();
        cart.getCartItems().add(cartItem);
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(menuItemRepository.findById(10L)).thenReturn(Optional.of(menuItem));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.addItemToCart(10L, 2);

        assertEquals(3, cartItem.getQuantity());
        assertEquals(300.0, cartItem.getPrice());
        verify(cartItemRepository).save(cartItem);
    }

    @Test
    void addItemToCart_differentRestaurant() {
        mockSecurity();
        cart.getCartItems().add(cartItem);

        Restaurant restaurant2 = new Restaurant();
        restaurant2.setId(2L);
        Category category2 = new Category();
        category2.setRestaurant(restaurant2);
        MenuItem menuItem2 = new MenuItem();
        menuItem2.setId(20L);
        menuItem2.setCategory(category2);

        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(menuItemRepository.findById(20L)).thenReturn(Optional.of(menuItem2));

        assertThrows(BadRequestException.class, () -> cartService.addItemToCart(20L, 1));
    }

    @Test
    void addItemToCart_invalidQuantity() {
        assertThrows(BadRequestException.class, () -> cartService.addItemToCart(10L, 0));
        assertThrows(BadRequestException.class, () -> cartService.addItemToCart(10L, null));
    }

    @Test
    void addItemToCart_menuItemNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(menuItemRepository.findById(10L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> cartService.addItemToCart(10L, 1));
    }

    @Test
    void getCart_success() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));

        Cart foundCart = cartService.getCart();

        assertNotNull(foundCart);
    }

    @Test
    void getCart_notFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> cartService.getCart());
    }

    @Test
    void decreaseItem_successDelete() {
        mockSecurity();
        cart.getCartItems().add(cartItem);
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.decreaseItem(10L);

        assertTrue(updatedCart.getCartItems().isEmpty());
        verify(cartItemRepository).delete(cartItem);
    }

    @Test
    void decreaseItem_successUpdateQuantity() {
        mockSecurity();
        cartItem.setQuantity(2);
        cartItem.setPrice(200.0);
        cart.getCartItems().add(cartItem);

        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.decreaseItem(10L);

        assertEquals(1, cartItem.getQuantity());
        verify(cartItemRepository).save(cartItem);
    }

    @Test
    void decreaseItem_itemNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));

        assertThrows(ResourceNotFoundException.class, () -> cartService.decreaseItem(10L));
    }

    @Test
    void removeItem_success() {
        mockSecurity();
        cart.getCartItems().add(cartItem);
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(cartRepository.save(any(Cart.class))).thenReturn(cart);

        Cart updatedCart = cartService.removeItem(10L);

        assertTrue(updatedCart.getCartItems().isEmpty());
        verify(cartItemRepository).delete(cartItem);
    }

    @Test
    void removeItem_itemNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));

        assertThrows(ResourceNotFoundException.class, () -> cartService.removeItem(10L));
    }

    @Test
    void clearCart_success() {
        mockSecurity();
        cart.getCartItems().add(cartItem);
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));

        cartService.clearCart();

        assertTrue(cart.getCartItems().isEmpty());
        assertEquals(0.0, cart.getTotalAmount());
        verify(cartItemRepository).deleteAll(anyList());
        verify(cartRepository).save(cart);
    }

    @Test
    void getLoggedInUser_userNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> cartService.getCart());
    }
}