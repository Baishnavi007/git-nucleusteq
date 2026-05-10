package com.baishnavi.restaurantOrderPortalBackend.dto;

/**
 * DTO for Cart Item
 */
public class CartItemDTO {

    private Long menuItemId;
    private String itemName;
    private Integer quantity;
    private Double price;

    public CartItemDTO() {}

    public CartItemDTO(Long menuItemId,String itemName, Integer quantity, Double price) {
        this.itemName = itemName;
        this.quantity = quantity;
        this.price = price;
        this.menuItemId = menuItemId;
    }

    public Long getMenuItemId() {
        return menuItemId;
    }

    public void setMenuItemId(Long menuItemId) {
        this.menuItemId = menuItemId;
    }

    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public Double getPrice() { return price; }
    public void setPrice(Double price) { this.price = price; }
}