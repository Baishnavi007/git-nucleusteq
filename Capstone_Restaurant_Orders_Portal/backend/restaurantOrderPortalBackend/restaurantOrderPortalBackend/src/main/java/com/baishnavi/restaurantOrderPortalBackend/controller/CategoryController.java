package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.CategoryRequestDTO;
import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import com.baishnavi.restaurantOrderPortalBackend.service.CategoryService;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for Category APIs
 */
@RestController
public class CategoryController {

    private final CategoryService categoryService;

    public CategoryController(CategoryService categoryService) {
        this.categoryService = categoryService;
    }

    /**
     * Add category performed by RESTAURANT_OWNER
     */
    @PostMapping("/owner/category")
    public Category addCategory(@Valid @RequestBody CategoryRequestDTO request) {

        return categoryService.addCategory(
                request.getRestaurantId(),
                request.getName()
        );
    }

    /**
     * OWNER: Update category
     */
    @PutMapping("/owner/category/{id}")
    public Category updateCategory(
            @PathVariable Long id,
            @Valid @RequestBody CategoryRequestDTO request) {

        return categoryService.updateCategory(id, request.getName());
    }

    /**
     * OWNER: Get categories of selected restaurant
     */
    @GetMapping("/owner/categories")
    public List<Category> getOwnerCategories(@RequestParam Long restaurantId) {
        return categoryService.getCategoriesByRestaurant(restaurantId);
    }

    /**
     * USER: Get categories of restaurant
     */
    @GetMapping("/users/categories")
    public List<Category> getCategories(@RequestParam Long restaurantId) {
        return categoryService.getCategoriesByRestaurant(restaurantId);
    }

    /**
     * OWNER: Soft delete category
     */
    @DeleteMapping("/owner/category/{id}")
    public String deleteCategory(@PathVariable Long id) {

        categoryService.deleteCategory(id);

        return "Category deleted successfully";
    }
}