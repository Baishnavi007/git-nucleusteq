package com.baishnavi.restaurantOrderPortalBackend.dto;

import java.util.List;

/**
 * DTO for Cart response
 */
public class CartDTO {

    private Double totalAmount;
    private List<CartItemDTO> items;

    public CartDTO() {}

    public CartDTO(Double totalAmount, List<CartItemDTO> items) {
        this.totalAmount = totalAmount;
        this.items = items;
    }

    public Double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(Double totalAmount) { this.totalAmount = totalAmount; }

    public List<CartItemDTO> getItems() { return items; }
    public void setItems(List<CartItemDTO> items) { this.items = items; }
}