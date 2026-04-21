package com.baishnavi.restaurantOrderPortalBackend.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;
    private String lastName;
// as e-mail should be unique and not null for each customer
    @Column(unique = true, nullable = false)
    private String email;

    private String password;
    private String phoneNumber;
    //stores enum in db
    @Enumerated(EnumType.STRING)
    private Role role;

    private Double walletBalance = 1000.0;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // One user can have many addresses
    @OneToMany(mappedBy = "user")
    private List<Address> addresses; // Foreign key
    //default constructor: used by hibernate to make objects
    public User() {}
}