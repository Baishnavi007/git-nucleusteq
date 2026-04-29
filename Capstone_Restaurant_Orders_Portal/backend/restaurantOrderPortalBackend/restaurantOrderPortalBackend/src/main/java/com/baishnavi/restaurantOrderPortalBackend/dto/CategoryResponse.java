package com.baishnavi.restaurantOrderPortalBackend.dto;

import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import java.util.List;

/**
 * DTO for category with its available menu items
 */
public class CategoryResponse {

    private String categoryName;
    private List<MenuItem> items;

    public CategoryResponse() {}

    public CategoryResponse(String categoryName, List<MenuItem> items) {
        this.categoryName = categoryName;
        this.items = items;
    }

    public String getCategoryName() {
        return categoryName;
    }

    public List<MenuItem> getItems() {
        return items;
    }
}