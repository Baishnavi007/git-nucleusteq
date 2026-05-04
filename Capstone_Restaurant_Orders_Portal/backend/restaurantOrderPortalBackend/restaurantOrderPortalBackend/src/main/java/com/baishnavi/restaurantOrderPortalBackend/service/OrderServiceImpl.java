package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.constants.AppConstants;
import com.baishnavi.restaurantOrderPortalBackend.entity.*;
import com.baishnavi.restaurantOrderPortalBackend.enums.OrderStatus;
import com.baishnavi.restaurantOrderPortalBackend.exception.BadRequestException;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.repository.*;

import jakarta.transaction.Transactional;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Implementation of OrderService
 */
@Service
@Transactional
public class OrderServiceImpl implements OrderService {

    private final CartRepository cartRepository;
    private final OrderRepository orderRepository;
    private final OrderItemRepository orderItemRepository;
    private final AddressRepository addressRepository;
    private final UserRepository userRepository;
    private final RestaurantRepository restaurantRepository;

    public OrderServiceImpl(CartRepository cartRepository,
                            OrderRepository orderRepository,
                            OrderItemRepository orderItemRepository,
                            AddressRepository addressRepository,
                            UserRepository userRepository,
                            RestaurantRepository restaurantRepository) {
        this.cartRepository = cartRepository;
        this.orderRepository = orderRepository;
        this.orderItemRepository = orderItemRepository;
        this.addressRepository = addressRepository;
        this.userRepository = userRepository;
        this.restaurantRepository = restaurantRepository;
    }

    /**
     * Place Order
     * @return order
     */
    @Override
    public Order placeOrder() {

        Authentication auth =
                SecurityContextHolder.getContext().getAuthentication();

        String email = auth.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found"));

        if (cart.getCartItems().isEmpty()) {
            throw new RuntimeException("Cart is empty");
        }

        Address address = addressRepository
                .findById(user.getSelectedAddressId())
                .orElseThrow(() -> new RuntimeException("Address not found"));

        if (user.getWalletBalance() < cart.getTotalAmount()) {
            throw new RuntimeException("Insufficient balance");
        }


        Restaurant restaurant = cart.getCartItems()
                .get(0)
                .getMenuItem()
                .getRestaurant();

        Order order = new Order();
        order.setUser(user);
        order.setAddress(address);
        order.setRestaurant(restaurant);
        order.setStatus(OrderStatus.PLACED);
        order.setCreatedAt(LocalDateTime.now());
        order.setTotalAmount(cart.getTotalAmount());

        order = orderRepository.save(order);

        List<OrderItem> orderItems = new ArrayList<>();

        for (CartItem cartItem : cart.getCartItems()) {
            OrderItem item = new OrderItem();
            item.setOrder(order);
            item.setMenuItem(cartItem.getMenuItem());
            item.setQuantity(cartItem.getQuantity());
            item.setPrice(cartItem.getPrice());

            orderItemRepository.save(item);
            orderItems.add(item);
        }

        order.setOrderItems(orderItems);

        user.setWalletBalance(user.getWalletBalance() - cart.getTotalAmount());
        userRepository.save(user);

        cart.getCartItems().clear();
        cart.setTotalAmount(0.0);
        cartRepository.save(cart);

        return order;
    }

    /**
     * Get the order history of logged-in user
     * @return order history
     */
    @Override
    public List<Order> getMyOrders() {

        Authentication auth =
                SecurityContextHolder.getContext().getAuthentication();

        String email = auth.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        return orderRepository.findByUser(user);
    }
    /**
     * Update order status
     *
     * @param orderId order ID
     * @param status new status
     * @return updated order
     */
    @Override
    public Order updateOrderStatus(Long orderId, String status) {

        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order not found"));

        OrderStatus newStatus;

        try {
            newStatus = OrderStatus.valueOf(status.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new BadRequestException("Invalid order status");
        }

        OrderStatus currentStatus = order.getStatus();

        if (!isValidTransition(currentStatus, newStatus)) {
            throw new BadRequestException(
                    "Invalid status transition from " + currentStatus + " to " + newStatus
            );
        }

        if (newStatus == OrderStatus.CANCELLED && currentStatus != OrderStatus.CANCELLED) {

            User user = order.getUser();

            Double before = user.getWalletBalance();

            user.setWalletBalance(before + order.getTotalAmount());

            System.out.println("Before: " + before);
            System.out.println("After: " + user.getWalletBalance());
        }

        order.setStatus(newStatus);

        return orderRepository.save(order);
    }
    private boolean isValidTransition(OrderStatus current, OrderStatus next) {

        return switch (current) {

            case PLACED ->
                    next == OrderStatus.PENDING ||
                            next == OrderStatus.CANCELLED;

            case PENDING ->
                    next == OrderStatus.DELIVERED ||
                            next == OrderStatus.CANCELLED;

            case DELIVERED ->
                    next == OrderStatus.COMPLETED;

            case COMPLETED, CANCELLED ->
                    false;

            default ->
                    false;
        };
    }
    /**
     * Cancel order within 30 seconds
     *
     * @param orderId order ID
     * @return updated order
     */
    @Override
    public Order cancelOrder(Long orderId) {

        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new RuntimeException("Order not found"));

        if (order.getStatus() == OrderStatus.CANCELLED) {
            throw new RuntimeException("Order already cancelled");
        }

        long secondsPassed = java.time.Duration.between(
                order.getCreatedAt(),
                java.time.LocalDateTime.now()
        ).getSeconds();

        if (secondsPassed > AppConstants.ORDER_CANCEL_TIME_SECONDS) {
            throw new RuntimeException("Cancellation time exceeded (30 seconds)");
        }
        User user = userRepository.findById(order.getUser().getId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        user.setWalletBalance(user.getWalletBalance() + order.getTotalAmount());

        order.setStatus(OrderStatus.CANCELLED);

        userRepository.save(user);
        return orderRepository.save(order);
    }
    /**
     * Get order status
     *
     * @param orderId order ID
     * @return order status
     */
    @Override
    public String getOrderStatus(Long orderId) {

        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new RuntimeException("Order not found"));

        return order.getStatus().name();
    }

    /**
     * Incoming Orders
     * @return orders
     */
    @Override
    public List<Order> getOrdersForOwner() {

        Authentication auth =
                SecurityContextHolder.getContext().getAuthentication();

        String email = auth.getName();

        User owner = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        List<Restaurant> restaurants =
                restaurantRepository.findByOwner(owner);

        List<Order> orders = new ArrayList<>();

        for (Restaurant r : restaurants) {
            orders.addAll(orderRepository.findByRestaurant(r));
        }

        return orders;
    }
}