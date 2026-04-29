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

    public OrderDTO() {}

    public OrderDTO(Long id, Double totalAmount, String status,
                    LocalDateTime createdAt, List<OrderItemDTO> items) {
        this.id = id;
        this.totalAmount = totalAmount;
        this.status = status;
        this.createdAt = createdAt;
        this.items = items;
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