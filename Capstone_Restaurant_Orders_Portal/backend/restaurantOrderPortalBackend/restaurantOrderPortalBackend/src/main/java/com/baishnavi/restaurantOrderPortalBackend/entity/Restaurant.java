package com.baishnavi.restaurantOrderPortalBackend.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "restaurants")
public class Restaurant {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String description;

    private String status;

    @ManyToOne
    @JoinColumn(name = "owner_id")
    private User owner;

    public Restaurant() {}
}