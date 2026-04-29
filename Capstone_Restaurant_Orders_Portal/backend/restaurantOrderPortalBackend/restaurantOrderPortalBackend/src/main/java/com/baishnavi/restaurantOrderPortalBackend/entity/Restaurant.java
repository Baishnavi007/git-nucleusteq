package com.baishnavi.restaurantOrderPortalBackend.entity;

import com.baishnavi.restaurantOrderPortalBackend.enums.RestaurantStatus;
import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import java.util.List;
import java.util.Objects;

/**
 * Entity representing a restaurant in the system.
 *
 * <p>
 * A restaurant is owned by a user (RESTAURANT_OWNER)
 * and contains multiple categories and menu items.
 * </p>
 */
@Entity
@Table(name = "restaurants")
public class Restaurant {

    /**
     * Primary key
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Restaurant name
     */
    private String name;

    /**
     * City where restaurant is located
     */
    private String city;

    /**
     * Optional description
     */
    private String description;

    /**
     * Current status of restaurant (OPEN, CLOSED, TEMP_CLOSED)
     */
    @Enumerated(EnumType.STRING)
    private RestaurantStatus status;

    /**
     * Owner of restaurant
     */
    @ManyToOne
    @JoinColumn(name = "owner_id")
    private User owner;

    /**
     * Categories under this restaurant
     */
    @OneToMany(mappedBy = "restaurant")
    @JsonIgnore
    private List<Category> categories;

    /**
     * No-args constructor (required by JPA)
     */
    public Restaurant() {}

    /**
     * All-args constructor
     *
     * @param id restaurant ID
     * @param name restaurant name
     * @param city restaurant city
     * @param description description
     * @param status restaurant status
     * @param owner owner of restaurant
     * @param categories categories under restaurant
     */
    public Restaurant(Long id, String name, String city,
                      String description, RestaurantStatus status,
                      User owner, List<Category> categories) {
        this.id = id;
        this.name = name;
        this.city = city;
        this.description = description;
        this.status = status;
        this.owner = owner;
        this.categories = categories;
    }

    //GETTERS & SETTERS

    /**
     * Get restaurant ID
     */
    public Long getId() {
        return id;
    }

    /**
     * Set restaurant ID
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * Get restaurant name
     */
    public String getName() {
        return name;
    }

    /**
     * Set restaurant name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Get city
     */
    public String getCity() {
        return city;
    }

    /**
     * Set city
     */
    public void setCity(String city) {
        this.city = city;
    }

    /**
     * Get description
     */
    public String getDescription() {
        return description;
    }

    /**
     * Set description
     */
    public void setDescription(String description) {
        this.description = description;
    }

    /**
     * Get restaurant status
     */
    public RestaurantStatus getStatus() {
        return status;
    }

    /**
     * Set restaurant status
     */
    public void setStatus(RestaurantStatus status) {
        this.status = status;
    }

    /**
     * Get owner
     */
    public User getOwner() {
        return owner;
    }

    /**
     * Set owner
     */
    public void setOwner(User owner) {
        this.owner = owner;
    }

    /**
     * Get categories
     */
    public List<Category> getCategories() {
        return categories;
    }

    /**
     * Set categories
     */
    public void setCategories(List<Category> categories) {
        this.categories = categories;
    }

    // ================= OVERRIDDEN METHODS =================

    /**
     * String representation
     */
    @Override
    public String toString() {
        return "Restaurant{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", city='" + city + '\'' +
                ", status=" + status +
                '}';
    }

    /**
     * Equality based on ID
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Restaurant)) return false;
        Restaurant that = (Restaurant) o;
        return id != null && id.equals(that.id);
    }

    /**
     * Hashcode based on ID
     */
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}