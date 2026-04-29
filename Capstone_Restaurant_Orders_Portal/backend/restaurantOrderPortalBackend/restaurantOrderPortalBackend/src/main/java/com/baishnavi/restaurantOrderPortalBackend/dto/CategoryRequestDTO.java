package com.baishnavi.restaurantOrderPortalBackend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

/**
 * DTO for creating category
 */
public class CategoryRequestDTO {

    @NotNull(message = "Restaurant ID is required")
    private Long restaurantId;

    @NotBlank(message = "Category name is required")
    private String name;

    public CategoryRequestDTO() {}

    public CategoryRequestDTO(Long restaurantId, String name) {
        this.restaurantId = restaurantId;
        this.name = name;
    }

    public Long getRestaurantId() { return restaurantId; }
    public void setRestaurantId(Long restaurantId) { this.restaurantId = restaurantId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}