package com.baishnavi.restaurantOrderPortalBackend.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import java.util.List;
import java.util.Objects;

/**
 * Entity representing user's cart.
 * <p>
 * Each user has one cart that contains multiple cart items.
 */
@Entity
@Table(name = "carts")
public class Cart {

    /**
     * Primary key
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Total amount of all items in the cart
     */
    private Double totalAmount;

    /**
     * One cart belongs to one user
     */
    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;

    /**
     * List of items inside the cart
     */
    @OneToMany(mappedBy = "cart")
    private List<CartItem> cartItems;

    /**
     * No-args constructor (required by JPA)
     */
    public Cart() {}

    /**
     * All-args constructor
     */
    public Cart(Long id, Double totalAmount, User user, List<CartItem> cartItems) {
        this.id = id;
        this.totalAmount = totalAmount;
        this.user = user;
        this.cartItems = cartItems;
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

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public List<CartItem> getCartItems() {
        return cartItems;
    }

    public void setCartItems(List<CartItem> cartItems) {
        this.cartItems = cartItems;
    }

    // ================= OVERRIDDEN METHODS =================

    /**
     * toString method (excluding cartItems to avoid recursion)
     */
    @Override
    public String toString() {
        return "Cart{" +
                "id=" + id +
                ", totalAmount=" + totalAmount +
                '}';
    }

    /**
     * equals based on id
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Cart)) return false;
        Cart cart = (Cart) o;
        return id != null && id.equals(cart.id);
    }

    /**
     * hashCode based on id
     */
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}