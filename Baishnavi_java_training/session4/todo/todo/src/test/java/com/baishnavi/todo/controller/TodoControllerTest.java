package com.baishnavi.todo.controller;

import com.baishnavi.todo.dto.TodoDTO;
import com.baishnavi.todo.service.TodoService;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;

import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

// This class tests Controller layer using MockMvc
@WebMvcTest(TodoController.class)
public class TodoControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TodoService service;

    @Autowired
    private ObjectMapper objectMapper;

    // ------------------- TEST 1 -------------------
    // CREATE TODO
    @Test
    void testCreateTodo() throws Exception {

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Study");
        dto.setStatus("PENDING");

        Mockito.when(service.createTodo(Mockito.any()))
                .thenReturn(dto);

        mockMvc.perform(post("/todos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Study"));
    }

    // ------------------- TEST 2 -------------------
    // GET ALL TODOS
    @Test
    void testGetAllTodos() throws Exception {

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Task1");

        Mockito.when(service.getAllTodos())
                .thenReturn(List.of(dto));

        mockMvc.perform(get("/todos"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.size()").value(1));
    }

    // ------------------- TEST 3 -------------------
    // GET TODO BY ID
    @Test
    void testGetTodoById() throws Exception {

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Task1");

        Mockito.when(service.getTodoById(1L))
                .thenReturn(dto);

        mockMvc.perform(get("/todos/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Task1"));
    }

    // ------------------- TEST 4 -------------------
    // UPDATE TODO
    @Test
    void testUpdateTodo() throws Exception {

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Updated Task");

        Mockito.when(service.updateTodo(Mockito.eq(1L), Mockito.any()))
                .thenReturn(dto);

        mockMvc.perform(put("/todos/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Updated Task"));
    }

    // ------------------- TEST 5 -------------------
    // DELETE TODO
    @Test
    void testDeleteTodo() throws Exception {

        Mockito.doNothing().when(service).deleteTodo(1L);

        mockMvc.perform(delete("/todos/1"))
                .andExpect(status().isOk());
    }
}