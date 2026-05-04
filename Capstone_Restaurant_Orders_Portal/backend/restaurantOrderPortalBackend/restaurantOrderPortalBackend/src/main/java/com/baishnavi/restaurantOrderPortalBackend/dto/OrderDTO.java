package com.baishnavi.restaurantOrderPortalBackend.dto;

import java.time.LocalDateTime;
import java.util.List;

/**
 * DTO for Order response
 */
public class OrderDTO {

    private Long id;
    private Double totalAmount;
    private String status;
    private LocalDateTime createdAt;
    private List<OrderItemDTO> items;
    private String customerName;
    private String address;
    private String restaurantName;
    public OrderDTO() {}

    public OrderDTO(Long id, Double totalAmount, String status,
                    LocalDateTime createdAt, List<OrderItemDTO> items, String customerName, String address, String restaurantName) {
        this.id = id;
        this.totalAmount = totalAmount;
        this.status = status;
        this.createdAt = createdAt;
        this.items = items;
        this.customerName=customerName;
        this.address=address;
        this.restaurantName=restaurantName;
    }

    public String getRestaurantName() {
        return restaurantName;
    }

    public void setRestaurantName(String restaurantName) {
        this.restaurantName = restaurantName;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(Double totalAmount) { this.totalAmount = totalAmount; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public List<OrderItemDTO> getItems() { return items; }
    public void setItems(List<OrderItemDTO> items) { this.items = items; }
}