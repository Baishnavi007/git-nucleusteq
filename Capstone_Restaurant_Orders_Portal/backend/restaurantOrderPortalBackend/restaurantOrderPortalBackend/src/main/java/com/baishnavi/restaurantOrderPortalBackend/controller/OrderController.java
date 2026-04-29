package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.OrderDTO;
import com.baishnavi.restaurantOrderPortalBackend.mapper.OrderMapper;
import com.baishnavi.restaurantOrderPortalBackend.service.OrderService;

import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for Order APIs
 *

 */
@RestController
public class OrderController {

    private final OrderService orderService;

    /**
     * Constructor injection
     *
     * @param orderService service layer dependency
     */
    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    /**
     * Place a new order
     *
     * @return OrderDTO (clean response)
     */
    @PostMapping("/orders/place")
    public OrderDTO placeOrder() {
        return OrderMapper.toDTO(orderService.placeOrder());
    }

    /**
     * Get all orders of logged-in user
     *
     * @return list of OrderDTO
     */
    @GetMapping("/orders/my")
    public List<OrderDTO> getMyOrders() {
        return orderService.getMyOrders()
                .stream()
                .map(OrderMapper::toDTO)
                .toList();
    }

    /**
     * Update order status (Owner use only)
     *
     * @param orderId order ID
     * @param status new status
     * @return updated OrderDTO
     */
    @PostMapping("/owner/orders/status")
    public OrderDTO updateStatus(@RequestParam Long orderId,
                                 @RequestParam String status) {
        return OrderMapper.toDTO(
                orderService.updateOrderStatus(orderId, status)
        );
    }

    /**
     * Cancel order (User)
     *
     * @param orderId order ID
     * @return updated OrderDTO
     */
    @PostMapping("/users/orders/cancel")
    public OrderDTO cancelOrder(@RequestParam Long orderId) {
        return OrderMapper.toDTO(
                orderService.cancelOrder(orderId)
        );
    }

    /**
     * Get order status (User)
     *
     * @param orderId order ID
     * @return status string
     */
    @GetMapping("/users/orders/{orderId}/status")
    public String getOrderStatus(@PathVariable Long orderId) {
        return orderService.getOrderStatus(orderId);
    }
}