package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.service.MenuItemService;

import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for Menu Item APIs
 */
@RestController
public class MenuItemController {

    private final MenuItemService menuItemService;

    public MenuItemController(MenuItemService menuItemService) {
        this.menuItemService = menuItemService;
    }

    /**
     * OWNER: Add menu item
     */
    @PostMapping("/owner/menu/add")
    public MenuItem addMenuItem(@RequestParam Long categoryId,
                                @RequestParam String name,
                                @RequestParam String description,
                                @RequestParam Double price) {

        return menuItemService.addMenuItem(categoryId, name, description, price);
    }

    /**
     * OWNER: Toggle availability
     */
    @PostMapping("/owner/menu/availability")
    public MenuItem updateAvailability(@RequestParam Long itemId,
                                       @RequestParam Boolean isAvailable) {

        return menuItemService.updateAvailability(itemId, isAvailable);
    }

    /**
     * OWNER: Get all items
     */
    @GetMapping("/owner/menu")
    public List<MenuItem> getAllMenu(@RequestParam Long categoryId) {
        return menuItemService.getAllMenuItems(categoryId);
    }

    /**
     * USER: Only available items
     */
    @GetMapping("/users/menu")
    public List<MenuItem> getAvailableMenu(@RequestParam Long categoryId) {
        return menuItemService.getAvailableMenuItems(categoryId);
    }

    /**
     * OWNER: Update menu item
     */
    @PutMapping("/owner/menu/update")
    public MenuItem updateMenuItem(@RequestParam Long itemId,
                                   @RequestParam String name,
                                   @RequestParam String description,
                                   @RequestParam Double price) {

        return menuItemService.updateMenuItem(itemId, name, description, price);
    }

    /**
     * OWNER: Delete menu item
     */
    @DeleteMapping("/owner/menu/delete")
    public String deleteMenuItem(@RequestParam Long itemId) {

        menuItemService.deleteMenuItem(itemId);
        return "Menu item deleted successfully";
    }
}