package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.constants.AppConstants;
import com.baishnavi.restaurantOrderPortalBackend.entity.*;
import com.baishnavi.restaurantOrderPortalBackend.enums.OrderStatus;
import com.baishnavi.restaurantOrderPortalBackend.repository.*;

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
public class OrderServiceImpl implements OrderService {

    private final CartRepository cartRepository;
    private final OrderRepository orderRepository;
    private final OrderItemRepository orderItemRepository;
    private final AddressRepository addressRepository;
    private final UserRepository userRepository;

    public OrderServiceImpl(CartRepository cartRepository,
                            OrderRepository orderRepository,
                            OrderItemRepository orderItemRepository,
                            AddressRepository addressRepository,
                            UserRepository userRepository) {
        this.cartRepository = cartRepository;
        this.orderRepository = orderRepository;
        this.orderItemRepository = orderItemRepository;
        this.addressRepository = addressRepository;
        this.userRepository = userRepository;
    }

    @Override
    public Order placeOrder() {

        //  logged-in user
        Authentication auth =
                SecurityContextHolder.getContext().getAuthentication();

        String email = auth.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        //  cart
        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found"));

        if (cart.getCartItems().isEmpty()) {
            throw new RuntimeException("Cart is empty");
        }

        // selected address
        Address address = addressRepository
                .findById(user.getSelectedAddressId())
                .orElseThrow(() -> new RuntimeException("Address not found"));

        //  wallet check
        if (user.getWalletBalance() < cart.getTotalAmount()) {
            throw new RuntimeException("Insufficient balance");
        }

        //  create order
        Order order = new Order();
        order.setUser(user);
        order.setAddress(address);
        order.setStatus(OrderStatus.PLACED);
        order.setCreatedAt(LocalDateTime.now());
        order.setTotalAmount(cart.getTotalAmount());

        order = orderRepository.save(order);

        //  create order items
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

        //  deduct money
        user.setWalletBalance(user.getWalletBalance() - cart.getTotalAmount());
        userRepository.save(user);

        //  clear cart
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

        //  logged-in user
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
                .orElseThrow(() -> new RuntimeException("Order not found"));

        order.setStatus(OrderStatus.valueOf(status));

        return orderRepository.save(order);
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

        // Checking  time difference
        long secondsPassed = java.time.Duration.between(
                order.getCreatedAt(),
                java.time.LocalDateTime.now()
        ).getSeconds();

        // order can only be cancelled under given time limit (here 30 seconds) after placing the order
        if (secondsPassed > AppConstants.ORDER_CANCEL_TIME_SECONDS) {
            throw new RuntimeException("Cancellation time exceeded (30 seconds)");
        }


        order.setStatus(OrderStatus.CANCELLED);

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
}