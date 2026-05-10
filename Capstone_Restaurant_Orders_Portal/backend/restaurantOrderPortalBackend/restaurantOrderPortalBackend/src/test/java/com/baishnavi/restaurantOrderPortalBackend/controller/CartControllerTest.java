package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.entity.Cart;
import com.baishnavi.restaurantOrderPortalBackend.entity.CartItem;
import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import com.baishnavi.restaurantOrderPortalBackend.service.CartService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(CartController.class)
@AutoConfigureMockMvc(addFilters = false)
class CartControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private CartService cartService;

    @MockitoBean
    private JwtUtil jwtUtil;

    private Cart cart;

    @BeforeEach
    void setUp() {
        cart = new Cart();
        cart.setId(1L);
        cart.setTotalAmount(150.0);

        MenuItem menuItem = new MenuItem();
        menuItem.setName("Burger");

        CartItem cartItem = new CartItem();
        cartItem.setQuantity(1);
        cartItem.setPrice(150.0);
        cartItem.setMenuItem(menuItem);

        cart.setCartItems(List.of(cartItem));
    }

    @Test
    void addToCart() throws Exception {
        when(cartService.addItemToCart(eq(1L), eq(1))).thenReturn(cart);

        mockMvc.perform(post("/cart/add")
                        .param("menuItemId", "1")
                        .param("quantity", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void getCart() throws Exception {
        when(cartService.getCart()).thenReturn(cart);

        mockMvc.perform(get("/cart"))
                .andExpect(status().isOk());
    }

    @Test
    void decrease() throws Exception {
        when(cartService.decreaseItem(anyLong())).thenReturn(cart);

        mockMvc.perform(post("/cart/decrease")
                        .param("menuItemId", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void remove() throws Exception {
        when(cartService.removeItem(anyLong())).thenReturn(cart);

        mockMvc.perform(delete("/cart/remove")
                        .param("menuItemId", "1"))
                .andExpect(status().isOk());
    }

    @Test
    void clearCart() throws Exception {
        doNothing().when(cartService).clearCart();

        mockMvc.perform(delete("/cart/clear"))
                .andExpect(status().isOk())
                .andExpect(content().string("Cart cleared successfully "));
    }
}