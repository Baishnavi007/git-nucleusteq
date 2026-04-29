package com.baishnavi.restaurantOrderPortalBackend.dto;

/**
 * DTO for Order Item
 */
public class OrderItemDTO {

    private String itemName;
    private Integer quantity;
    private Double price;

    public OrderItemDTO() {}

    public OrderItemDTO(String itemName, Integer quantity, Double price) {
        this.itemName = itemName;
        this.quantity = quantity;
        this.price = price;
    }

    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public Double getPrice() { return price; }
    public void setPrice(Double price) { this.price = price; }
}