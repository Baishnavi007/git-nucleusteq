package com.baishnavi.restaurantOrderPortalBackend.dto;

import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import java.util.List;

/**
 * DTO for category with its menu items
 */
public class CategoryMenuDTO {

    private Long categoryId;
    private String categoryName;
    private List<MenuItem> items;

    public CategoryMenuDTO() {}

    public CategoryMenuDTO(Long categoryId, String categoryName, List<MenuItem> items) {
        this.categoryId = categoryId;
        this.categoryName = categoryName;
        this.items = items;
    }

    public Long getCategoryId() { return categoryId; }
    public void setCategoryId(Long categoryId) { this.categoryId = categoryId; }

    public String getCategoryName() { return categoryName; }
    public void setCategoryName(String categoryName) { this.categoryName = categoryName; }

    public List<MenuItem> getItems() { return items; }
    public void setItems(List<MenuItem> items) { this.items = items; }
}