package com.baishnavi.restaurantOrderPortalBackend.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.Objects;

/**
 * Entity representing user address
 */
@Entity
@Table(name = "addresses")
public class Address {

    /**
     * Primary key
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Street details
     */
    private String street;

    /**
     * City of address
     */
    private String city;

    /**
     * State of address
     */
    private String state;

    /**
     * Pincode
     */
    private String pincode;

    /**
     * Default address flag
     */
    private Boolean isDefault;

    /**
     * Many addresses belong to one user
     */
    @ManyToOne
    @JoinColumn(name = "user_id")
    @JsonIgnore
    private User user;

    /**
     * No-args constructor (required by JPA)
     */
    public Address() {}

    /**
     * All-args constructor
     */
    public Address(Long id, String street, String city, String state,
                   String pincode, Boolean isDefault, User user) {
        this.id = id;
        this.street = street;
        this.city = city;
        this.state = state;
        this.pincode = pincode;
        this.isDefault = isDefault;
        this.user = user;
    }

    // Getters & Setters

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getStreet() { return street; }
    public void setStreet(String street) { this.street = street; }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    public String getState() { return state; }
    public void setState(String state) { this.state = state; }

    public String getPincode() { return pincode; }
    public void setPincode(String pincode) { this.pincode = pincode; }

    public Boolean getIsDefault() { return isDefault; }
    public void setIsDefault(Boolean isDefault) { this.isDefault = isDefault; }

    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }

    /**
     * toString method (excluding user to avoid recursion)
     */
    @Override
    public String toString() {
        return "Address{" +
                "id=" + id +
                ", city='" + city + '\'' +
                ", state='" + state + '\'' +
                ", pincode='" + pincode + '\'' +
                ", isDefault=" + isDefault +
                '}';
    }

    /**
     * equals method based on id
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Address)) return false;
        Address address = (Address) o;
        return id != null && id.equals(address.id);
    }

    /**
     * hashCode method based on id
     */
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}