package com.baishnavi.todo.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

// Data Transfer Object for Todo
  public class TodoDTO {
    // DTO contains only client-facing fields.
// id and createdAt are excluded as they are system-generated and should not be controlled by the client.


    // Title must not be null and should have minimum 3 characters
    @NotNull(message = "Title cannot be null")
    @Size(min = 3, message = "Title must be at least 3 characters")
    private String title;

    private String description;

    // Status (PENDING / COMPLETED)
    private String status;

    // Default constructor
    public TodoDTO() {
    }

    // Getters and Setters

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }


    public void setDescription(String description) {
        this.description = description;
    }

    public String getStatus() {
        return status;
    }


    public void setStatus(String status) {
        this.status = status;
    }
}