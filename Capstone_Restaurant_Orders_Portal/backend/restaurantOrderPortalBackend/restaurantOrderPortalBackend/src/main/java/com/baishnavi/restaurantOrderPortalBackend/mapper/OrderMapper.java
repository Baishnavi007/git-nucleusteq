package com.baishnavi.restaurantOrderPortalBackend.mapper;

import com.baishnavi.restaurantOrderPortalBackend.dto.OrderDTO;
import com.baishnavi.restaurantOrderPortalBackend.dto.OrderItemDTO;
import com.baishnavi.restaurantOrderPortalBackend.entity.Order;
import com.baishnavi.restaurantOrderPortalBackend.entity.OrderItem;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Mapper for Order
 */
public class OrderMapper {

    public static OrderDTO toDTO(Order order) {

        List<OrderItemDTO> items = order.getOrderItems()
                .stream()
                .map(OrderMapper::toItemDTO)
                .collect(Collectors.toList());
        String customerName = order.getUser().getFirstName() + " " + order.getUser().getLastName();
        String address = order.getAddress().getStreet() + ", "
                + order.getAddress().getCity() + "," + order.getAddress().getPincode();

        String restaurantName = order.getRestaurant().getName();

        return new OrderDTO(
                order.getId(),
                order.getTotalAmount(),
                order.getStatus().name(),
                order.getCreatedAt(),
                items,
                customerName,
                address,
                restaurantName


        );
    }

    public static OrderItemDTO toItemDTO(OrderItem item) {
        return new OrderItemDTO(
                item.getMenuItem().getName(),
                item.getQuantity(),
                item.getPrice()
        );
    }
}