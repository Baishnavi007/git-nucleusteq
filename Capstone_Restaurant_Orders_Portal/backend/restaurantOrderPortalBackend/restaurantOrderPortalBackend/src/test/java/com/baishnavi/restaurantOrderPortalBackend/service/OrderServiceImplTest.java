package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.constants.AppConstants;
import com.baishnavi.restaurantOrderPortalBackend.entity.*;
import com.baishnavi.restaurantOrderPortalBackend.enums.OrderStatus;
import com.baishnavi.restaurantOrderPortalBackend.exception.BadRequestException;
import com.baishnavi.restaurantOrderPortalBackend.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceImplTest {

    @Mock
    private CartRepository cartRepository;

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private OrderItemRepository orderItemRepository;

    @Mock
    private AddressRepository addressRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private RestaurantRepository restaurantRepository;

    @Mock
    private SecurityContext securityContext;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private OrderServiceImpl orderService;

    private User user;
    private Cart cart;
    private Order order;
    private Address address;

    @BeforeEach
    void setUp() {
        SecurityContextHolder.setContext(securityContext);

        user = new User();
        user.setId(1L);
        user.setEmail("test@example.com");
        user.setWalletBalance(1000.0);
        user.setSelectedAddressId(10L);

        address = new Address();
        address.setId(10L);

        Restaurant restaurant = new Restaurant();
        restaurant.setId(100L);

        MenuItem menuItem = new MenuItem();
        menuItem.setId(1L);
        menuItem.setRestaurant(restaurant);

        CartItem cartItem = new CartItem();
        cartItem.setMenuItem(menuItem);
        cartItem.setQuantity(2);
        cartItem.setPrice(300.0);

        List<CartItem> cartItems = new ArrayList<>();
        cartItems.add(cartItem);

        cart = new Cart();
        cart.setId(1L);
        cart.setUser(user);
        cart.setTotalAmount(300.0);
        cart.setCartItems(cartItems);

        order = new Order();
        order.setId(1L);
        order.setUser(user);
        order.setTotalAmount(300.0);
        order.setStatus(OrderStatus.PLACED);
        order.setCreatedAt(LocalDateTime.now());
    }

    private void mockSecurity() {
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn("test@example.com");
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
    }

    @Test
    void placeOrder_success() {
        mockSecurity();
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArguments()[0]);

        Order placedOrder = orderService.placeOrder();

        assertNotNull(placedOrder);
        assertEquals(OrderStatus.PLACED, placedOrder.getStatus());
        assertEquals(700.0, user.getWalletBalance());
        assertTrue(cart.getCartItems().isEmpty());
        verify(orderRepository).save(any(Order.class));
        verify(orderItemRepository).save(any(OrderItem.class));
        verify(userRepository).save(user);
        verify(cartRepository).save(cart);
    }

    @Test
    void placeOrder_insufficientBalance() {
        user.setWalletBalance(100.0);
        mockSecurity();
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));

        assertThrows(RuntimeException.class, () -> orderService.placeOrder());
    }

    @Test
    void updateOrderStatus_success() {
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        Order updatedOrder = orderService.updateOrderStatus(1L, "PENDING");

        assertEquals(OrderStatus.PENDING, updatedOrder.getStatus());
        verify(orderRepository).save(order);
    }

    @Test
    void updateOrderStatus_invalidTransition() {
        order.setStatus(OrderStatus.DELIVERED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

        assertThrows(BadRequestException.class, () -> orderService.updateOrderStatus(1L, "PENDING"));
    }

    @Test
    void cancelOrder_success() {
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        Order cancelledOrder = orderService.cancelOrder(1L);

        assertEquals(OrderStatus.CANCELLED, cancelledOrder.getStatus());
        assertEquals(1300.0, user.getWalletBalance());
        verify(userRepository).save(user);
        verify(orderRepository).save(order);
    }

    @Test
    void cancelOrder_timeExceeded() {
        order.setCreatedAt(LocalDateTime.now().minusSeconds(AppConstants.ORDER_CANCEL_TIME_SECONDS + 10));
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

        assertThrows(RuntimeException.class, () -> orderService.cancelOrder(1L));
    }
}