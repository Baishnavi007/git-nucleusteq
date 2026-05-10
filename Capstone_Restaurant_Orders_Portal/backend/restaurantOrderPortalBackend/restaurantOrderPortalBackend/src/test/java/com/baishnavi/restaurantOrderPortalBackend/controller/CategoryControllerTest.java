package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.CategoryRequestDTO;
import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import com.baishnavi.restaurantOrderPortalBackend.service.CategoryService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(CategoryController.class)
@AutoConfigureMockMvc(addFilters = false)
class CategoryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private CategoryService categoryService;

    @MockitoBean
    private JwtUtil jwtUtil;

    @Autowired
    private ObjectMapper objectMapper;

    private Category category;

    @BeforeEach
    void setUp() {
        category = new Category();
        category.setId(1L);
        category.setName("Desserts");
    }

    @Test
    void addCategory() throws Exception {
        CategoryRequestDTO requestDTO = new CategoryRequestDTO(1L, "Desserts");
        when(categoryService.addCategory(anyLong(), anyString())).thenReturn(category);

        mockMvc.perform(post("/owner/category")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(requestDTO)))
                .andExpect(status().isOk());
    }

    @Test
    void getOwnerCategories() throws Exception {
        when(categoryService.getCategoriesByRestaurant(1L)).thenReturn(List.of(category));

        mockMvc.perform(get("/owner/categories")
                        .param("restaurantId", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void getCategories() throws Exception {
        when(categoryService.getCategoriesByRestaurant(1L)).thenReturn(List.of(category));

        mockMvc.perform(get("/users/categories")
                        .param("restaurantId", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void deleteCategory() throws Exception {
        doNothing().when(categoryService).deleteCategory(1L);

        mockMvc.perform(delete("/owner/category/1"))
                .andExpect(status().isOk())
                .andExpect(content().string("Category deleted successfully"));
    }
}