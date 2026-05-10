package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.constants.AppConstants;
import com.baishnavi.restaurantOrderPortalBackend.entity.*;
import com.baishnavi.restaurantOrderPortalBackend.enums.OrderStatus;
import com.baishnavi.restaurantOrderPortalBackend.enums.RestaurantStatus;
import com.baishnavi.restaurantOrderPortalBackend.exception.BadRequestException;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
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
    private Restaurant restaurant;

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

        restaurant = new Restaurant();
        restaurant.setId(100L);
        restaurant.setStatus(RestaurantStatus.OPEN);

        MenuItem menuItem = new MenuItem();
        menuItem.setId(1L);
        menuItem.setRestaurant(restaurant);

        // Add 2 items to ensure loop coverage is fully hit
        CartItem cartItem1 = new CartItem();
        cartItem1.setMenuItem(menuItem);
        cartItem1.setQuantity(1);
        cartItem1.setPrice(150.0);

        CartItem cartItem2 = new CartItem();
        cartItem2.setMenuItem(menuItem);
        cartItem2.setQuantity(1);
        cartItem2.setPrice(150.0);

        List<CartItem> cartItems = new ArrayList<>();
        cartItems.add(cartItem1);
        cartItems.add(cartItem2);

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
    }

    // ==========================================
    // placeOrder() TESTS
    // ==========================================

    @Test
    void placeOrder_success() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));
        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArguments()[0]);

        Order placedOrder = orderService.placeOrder();

        assertNotNull(placedOrder);
        assertEquals(OrderStatus.PLACED, placedOrder.getStatus());
        assertEquals(700.0, user.getWalletBalance());
        assertTrue(cart.getCartItems().isEmpty());
        assertEquals(0.0, cart.getTotalAmount());

        // Ensure loop ran twice for the two items
        verify(orderItemRepository, times(2)).save(any(OrderItem.class));
        verify(orderRepository).save(any(Order.class));
        verify(userRepository).save(user);
        verify(cartRepository).save(cart);
    }

    @Test
    void placeOrder_userNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> orderService.placeOrder());
    }

    @Test
    void placeOrder_cartNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> orderService.placeOrder());
    }

    @Test
    void placeOrder_cartEmpty() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        cart.getCartItems().clear();
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        assertThrows(BadRequestException.class, () -> orderService.placeOrder());
    }

    @Test
    void placeOrder_addressNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(addressRepository.findById(10L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> orderService.placeOrder());
    }

    @Test
    void placeOrder_insufficientBalance() {
        mockSecurity();
        user.setWalletBalance(100.0);
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));
        assertThrows(BadRequestException.class, () -> orderService.placeOrder());
    }

    @Test
    void placeOrder_restaurantClosed() {
        mockSecurity();
        restaurant.setStatus(RestaurantStatus.CLOSED);
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(cartRepository.findByUser(user)).thenReturn(Optional.of(cart));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));
        assertThrows(BadRequestException.class, () -> orderService.placeOrder());
    }

    // ==========================================
    // getMyOrders() TESTS
    // ==========================================

    @Test
    void getMyOrders_success() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(orderRepository.findByUser(user)).thenReturn(List.of(order));

        List<Order> orders = orderService.getMyOrders();
        assertEquals(1, orders.size());
    }

    @Test
    void getMyOrders_userNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> orderService.getMyOrders());
    }

    // ==========================================
    // updateOrderStatus() & isValidTransition TESTS
    // ==========================================

    @Test
    void updateOrderStatus_PlacedToPending() {
        order.setStatus(OrderStatus.PLACED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        Order updatedOrder = orderService.updateOrderStatus(1L, "PENDING");
        assertEquals(OrderStatus.PENDING, updatedOrder.getStatus());
    }

    @Test
    void updateOrderStatus_PlacedToCancelled() {
        order.setStatus(OrderStatus.PLACED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        orderService.updateOrderStatus(1L, "CANCELLED");
        assertEquals(1300.0, user.getWalletBalance()); // Refund check
        assertEquals(OrderStatus.CANCELLED, order.getStatus());
    }

    @Test
    void updateOrderStatus_PendingToDelivered() {
        order.setStatus(OrderStatus.PENDING);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        Order updatedOrder = orderService.updateOrderStatus(1L, "DELIVERED");
        assertEquals(OrderStatus.DELIVERED, updatedOrder.getStatus());
    }

    @Test
    void updateOrderStatus_PendingToCancelled() {
        order.setStatus(OrderStatus.PENDING);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        orderService.updateOrderStatus(1L, "CANCELLED");
        assertEquals(OrderStatus.CANCELLED, order.getStatus());
    }

    @Test
    void updateOrderStatus_DeliveredToCompleted() {
        order.setStatus(OrderStatus.DELIVERED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        Order updatedOrder = orderService.updateOrderStatus(1L, "COMPLETED");
        assertEquals(OrderStatus.COMPLETED, updatedOrder.getStatus());
    }

    // Invalid Transitions - Hitting the 'false' returns in the switch statement

    @Test
    void updateOrderStatus_InvalidPlacedToDelivered() {
        order.setStatus(OrderStatus.PLACED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(BadRequestException.class, () -> orderService.updateOrderStatus(1L, "DELIVERED"));
    }

    @Test
    void updateOrderStatus_InvalidPendingToPlaced() {
        order.setStatus(OrderStatus.PENDING);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(BadRequestException.class, () -> orderService.updateOrderStatus(1L, "PLACED"));
    }

    @Test
    void updateOrderStatus_InvalidDeliveredToCancelled() {
        order.setStatus(OrderStatus.DELIVERED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(BadRequestException.class, () -> orderService.updateOrderStatus(1L, "CANCELLED"));
    }

    @Test
    void updateOrderStatus_InvalidFromCompleted() {
        order.setStatus(OrderStatus.COMPLETED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(BadRequestException.class, () -> orderService.updateOrderStatus(1L, "PENDING"));
    }

    @Test
    void updateOrderStatus_InvalidFromCancelled() {
        order.setStatus(OrderStatus.CANCELLED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(BadRequestException.class, () -> orderService.updateOrderStatus(1L, "PLACED"));
    }

    @Test
    void updateOrderStatus_orderNotFound() {
        when(orderRepository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> orderService.updateOrderStatus(1L, "PENDING"));
    }

    @Test
    void updateOrderStatus_invalidEnumString() {
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(BadRequestException.class, () -> orderService.updateOrderStatus(1L, "UNKNOWN_STATUS"));
    }

    // ==========================================
    // cancelOrder() TESTS
    // ==========================================

    @Test
    void cancelOrder_success() {
        order.setCreatedAt(LocalDateTime.now().minusSeconds(10)); // Well within 30s
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        Order cancelledOrder = orderService.cancelOrder(1L);

        assertEquals(OrderStatus.CANCELLED, cancelledOrder.getStatus());
        assertEquals(1300.0, user.getWalletBalance()); // Refund verified
        verify(userRepository).save(user);
        verify(orderRepository).save(order);
    }

    @Test
    void cancelOrder_orderNotFound() {
        when(orderRepository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> orderService.cancelOrder(1L));
    }

    @Test
    void cancelOrder_alreadyCancelled() {
        order.setStatus(OrderStatus.CANCELLED);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(RuntimeException.class, () -> orderService.cancelOrder(1L));
    }

    @Test
    void cancelOrder_timeExceeded() {
        order.setCreatedAt(LocalDateTime.now().minusSeconds(AppConstants.ORDER_CANCEL_TIME_SECONDS + 5));
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        assertThrows(RuntimeException.class, () -> orderService.cancelOrder(1L));
    }

    @Test
    void cancelOrder_userNotFound() {
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        when(userRepository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> orderService.cancelOrder(1L));
    }

    // ==========================================
    // getOrderStatus() TESTS
    // ==========================================

    @Test
    void getOrderStatus_success() {
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));
        String status = orderService.getOrderStatus(1L);
        assertEquals("PLACED", status);
    }

    @Test
    void getOrderStatus_orderNotFound() {
        when(orderRepository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> orderService.getOrderStatus(1L));
    }

    // ==========================================
    // getOrdersForOwner() TESTS
    // ==========================================

    @Test
    void getOrdersForOwner_success() {
        mockSecurity();
        Restaurant restaurant2 = new Restaurant();
        restaurant2.setId(101L);

        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        // Add two restaurants to ensure the loop is fully covered
        when(restaurantRepository.findByOwner(user)).thenReturn(List.of(restaurant, restaurant2));
        when(orderRepository.findByRestaurant(restaurant)).thenReturn(List.of(order));
        when(orderRepository.findByRestaurant(restaurant2)).thenReturn(new ArrayList<>());

        List<Order> ownerOrders = orderService.getOrdersForOwner();

        assertEquals(1, ownerOrders.size());
        verify(orderRepository, times(1)).findByRestaurant(restaurant);
        verify(orderRepository, times(1)).findByRestaurant(restaurant2);
    }

    @Test
    void getOrdersForOwner_userNotFound() {
        mockSecurity();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.empty());
        assertThrows(RuntimeException.class, () -> orderService.getOrdersForOwner());
    }
}