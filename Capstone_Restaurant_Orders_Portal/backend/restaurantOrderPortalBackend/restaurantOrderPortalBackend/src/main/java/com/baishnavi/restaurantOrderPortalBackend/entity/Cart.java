package com.baishnavi.restaurantOrderPortalBackend.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "carts")
public class Cart {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Double totalAmount;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;

    public Cart() {}
}