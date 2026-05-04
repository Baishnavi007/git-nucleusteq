package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import com.baishnavi.restaurantOrderPortalBackend.service.MenuItemService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(MenuItemController.class)
@AutoConfigureMockMvc(addFilters = false)
class MenuItemControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private MenuItemService menuItemService;

    @MockitoBean
    private JwtUtil jwtUtil;

    private MenuItem menuItem;

    @BeforeEach
    void setUp() {
        menuItem = new MenuItem();
        menuItem.setId(1L);
        menuItem.setName("Pizza");
        menuItem.setDescription("Cheese Pizza");
        menuItem.setPrice(200.0);
    }

    @Test
    void addMenuItem() throws Exception {
        when(menuItemService.addMenuItem(eq(1L), eq("Pizza"), eq("Cheese Pizza"), eq(200.0))).thenReturn(menuItem);

        mockMvc.perform(post("/owner/menu/add")
                        .param("categoryId", "1")
                        .param("name", "Pizza")
                        .param("description", "Cheese Pizza")
                        .param("price", "200.0"))
                .andExpect(status().isOk());
    }

    @Test
    void updateAvailability() throws Exception {
        when(menuItemService.updateAvailability(1L, true)).thenReturn(menuItem);

        mockMvc.perform(post("/owner/menu/availability")
                        .param("itemId", "1")
                        .param("isAvailable", "true"))
                .andExpect(status().isOk());
    }

    @Test
    void getAllMenu() throws Exception {
        when(menuItemService.getAllMenuItems(1L)).thenReturn(List.of(menuItem));

        mockMvc.perform(get("/owner/menu")
                        .param("categoryId", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void getAvailableMenu() throws Exception {
        when(menuItemService.getAvailableMenuItems(1L)).thenReturn(List.of(menuItem));

        mockMvc.perform(get("/users/menu")
                        .param("categoryId", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void updateMenuItem() throws Exception {
        when(menuItemService.updateMenuItem(eq(1L), eq("Pizza"), eq("Cheese Pizza"), eq(200.0))).thenReturn(menuItem);

        mockMvc.perform(put("/owner/menu/update")
                        .param("itemId", "1")
                        .param("name", "Pizza")
                        .param("description", "Cheese Pizza")
                        .param("price", "200.0"))
                .andExpect(status().isOk());
    }

    @Test
    void deleteItem() throws Exception {
        doNothing().when(menuItemService).deleteMenuItem(1L);

        mockMvc.perform(delete("/owner/menu/1"))
                .andExpect(status().isOk())
                .andExpect(content().string("Item deleted"));
    }
}