package com.baishnavi.restaurantOrderPortalBackend.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import java.util.Objects;

/**
 * Entity representing an item inside a user's cart.
 * <p>
 * Each CartItem links a Cart with a MenuItem and stores
 * quantity and price at the time of adding to cart.
 */
@Entity
@Table(name = "cart_items")
public class CartItem {

    /**
     * Primary key
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Quantity of the menu item
     */
    private Integer quantity;

    /**
     * Price for this item (can be quantity * item price)
     */
    private Double price;

    /**
     * Cart to which this item belongs
     */
    @ManyToOne
    @JoinColumn(name = "cart_id")
    private Cart cart;

    /**
     * Menu item associated with this cart item
     */
    @ManyToOne
    @JoinColumn(name = "menu_item_id")
    private MenuItem menuItem;

    /**
     * No-args constructor (required by JPA)
     */
    public CartItem() {}

    /**
     * All-args constructor
     */
    public CartItem(Long id, Integer quantity, Double price, Cart cart, MenuItem menuItem) {
        this.id = id;
        this.quantity = quantity;
        this.price = price;
        this.cart = cart;
        this.menuItem = menuItem;
    }

    // ================= GETTERS & SETTERS =================

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public Cart getCart() {
        return cart;
    }

    public void setCart(Cart cart) {
        this.cart = cart;
    }

    public MenuItem getMenuItem() {
        return menuItem;
    }

    public void setMenuItem(MenuItem menuItem) {
        this.menuItem = menuItem;
    }

    // ================= OVERRIDDEN METHODS =================

    /**
     * String representation (excluding relations to avoid recursion)
     */
    @Override
    public String toString() {
        return "CartItem{" +
                "id=" + id +
                ", quantity=" + quantity +
                ", price=" + price +
                '}';
    }

    /**
     * Equality based on id
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof CartItem)) return false;
        CartItem that = (CartItem) o;
        return id != null && id.equals(that.id);
    }

    /**
     * Hashcode based on id
     */
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}