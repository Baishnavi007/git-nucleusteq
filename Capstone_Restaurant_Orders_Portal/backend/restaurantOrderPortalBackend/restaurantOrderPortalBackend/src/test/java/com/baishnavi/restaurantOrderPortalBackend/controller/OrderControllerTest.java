package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.entity.*;
import com.baishnavi.restaurantOrderPortalBackend.enums.OrderStatus;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import com.baishnavi.restaurantOrderPortalBackend.service.OrderService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(OrderController.class)
@AutoConfigureMockMvc(addFilters = false)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private OrderService orderService;

    @MockitoBean
    private JwtUtil jwtUtil;

    private Order order;

    @BeforeEach
    void setUp() {
        User user = new User();
        user.setFirstName("John");
        user.setLastName("Doe");

        Address address = new Address();
        address.setStreet("Main St");
        address.setCity("Pune");

        Restaurant restaurant = new Restaurant();
        restaurant.setName("Tasty Bites");

        order = new Order();
        order.setId(1L);
        order.setTotalAmount(500.0);
        order.setStatus(OrderStatus.PLACED);
        order.setCreatedAt(LocalDateTime.now());
        order.setUser(user);
        order.setAddress(address);
        order.setRestaurant(restaurant);
        order.setOrderItems(new ArrayList<>());
    }

    @Test
    void placeOrder() throws Exception {
        when(orderService.placeOrder()).thenReturn(order);

        mockMvc.perform(post("/orders/place"))
                .andExpect(status().isOk());
    }

    @Test
    void getMyOrders() throws Exception {
        when(orderService.getMyOrders()).thenReturn(List.of(order));

        mockMvc.perform(get("/orders/my"))
                .andExpect(status().isOk());
    }

    @Test
    void getOwnerOrders() throws Exception {
        when(orderService.getOrdersForOwner()).thenReturn(List.of(order));

        mockMvc.perform(get("/owner/orders"))
                .andExpect(status().isOk());
    }

    @Test
    void updateStatus() throws Exception {
        when(orderService.updateOrderStatus(anyLong(), anyString())).thenReturn(order);

        mockMvc.perform(post("/owner/orders/status")
                        .param("orderId", "1")
                        .param("status", "PENDING"))
                .andExpect(status().isOk());
    }

    @Test
    void cancelOrder() throws Exception {
        when(orderService.cancelOrder(1L)).thenReturn(order);

        mockMvc.perform(post("/users/orders/cancel")
                        .param("orderId", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void getOrderStatus() throws Exception {
        when(orderService.getOrderStatus(1L)).thenReturn("PLACED");

        mockMvc.perform(get("/users/orders/1/status"))
                .andExpect(status().isOk())
                .andExpect(content().string("PLACED"));
    }
}