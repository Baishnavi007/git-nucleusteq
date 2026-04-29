package com.baishnavi.restaurantOrderPortalBackend.entity;

import com.baishnavi.restaurantOrderPortalBackend.enums.OrderStatus;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Enumerated;
import jakarta.persistence.EnumType;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Table;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;

/**
 * Entity representing user orders
 */
@Entity
@Table(name = "orders")
public class Order {

    /**
     * Primary key
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Total order amount
     */
    private Double totalAmount;

    /**
     * Order status (PLACED, DELIVERED, etc.)
     */
    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    /**
     * Order creation time
     */
    private LocalDateTime createdAt;

    /**
     * User who placed the order
     */
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    /**
     * Address used for delivery
     */
    @ManyToOne
    @JoinColumn(name = "address_id")
    private Address address;

    /**
     * Items inside the order
     */
    @OneToMany(mappedBy = "order")
    private List<OrderItem> orderItems;

    /**
     * No-args constructor
     */
    public Order() {}

    /**
     * All-args constructor
     */
    public Order(Long id, Double totalAmount, OrderStatus status,
                 LocalDateTime createdAt, User user,
                 Address address, List<OrderItem> orderItems) {
        this.id = id;
        this.totalAmount = totalAmount;
        this.status = status;
        this.createdAt = createdAt;
        this.user = user;
        this.address = address;
        this.orderItems = orderItems;
    }

    // ================= GETTERS & SETTERS =================

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Double getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(Double totalAmount) {
        this.totalAmount = totalAmount;
    }

    public OrderStatus getStatus() {
        return status;
    }

    public void setStatus(OrderStatus status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public List<OrderItem> getOrderItems() {
        return orderItems;
    }

    public void setOrderItems(List<OrderItem> orderItems) {
        this.orderItems = orderItems;
    }

    // ================= OVERRIDDEN METHODS =================

    @Override
    public String toString() {
        return "Order{" +
                "id=" + id +
                ", totalAmount=" + totalAmount +
                ", status=" + status +
                ", createdAt=" + createdAt +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Order)) return false;
        Order order = (Order) o;
        return id != null && id.equals(order.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}