package com.baishnavi.restaurantOrderPortalBackend.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Table;

import java.util.Objects;

/**
 * Entity representing items in an order
 */
@Entity
@Table(name = "order_items")
public class OrderItem {

    /**
     * Primary key
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Quantity of item
     */
    private Integer quantity;

    /**
     * Price at the time of order
     */
    private Double price;

    /**
     * Order to which this item belongs
     */
    @ManyToOne
    @JoinColumn(name = "order_id")
    private Order order;

    /**
     * Menu item reference
     */
    @ManyToOne
    @JoinColumn(name = "menu_item_id")
    private MenuItem menuItem;

    /**
     * No-args constructor
     */
    public OrderItem() {}

    /**
     * All-args constructor
     */
    public OrderItem(Long id, Integer quantity, Double price,
                     Order order, MenuItem menuItem) {
        this.id = id;
        this.quantity = quantity;
        this.price = price;
        this.order = order;
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

    public Order getOrder() {
        return order;
    }

    public void setOrder(Order order) {
        this.order = order;
    }

    public MenuItem getMenuItem() {
        return menuItem;
    }

    public void setMenuItem(MenuItem menuItem) {
        this.menuItem = menuItem;
    }

    // ================= OVERRIDDEN METHODS =================

    @Override
    public String toString() {
        return "OrderItem{" +
                "id=" + id +
                ", quantity=" + quantity +
                ", price=" + price +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderItem)) return false;
        OrderItem that = (OrderItem) o;
        return id != null && id.equals(that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}