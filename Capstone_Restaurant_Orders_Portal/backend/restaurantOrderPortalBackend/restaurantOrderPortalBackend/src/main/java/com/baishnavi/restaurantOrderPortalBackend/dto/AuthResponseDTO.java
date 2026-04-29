package com.baishnavi.restaurantOrderPortalBackend.dto;

/**
 * DTO for login response
 */
public class AuthResponseDTO {

    private String token;
    private String role;
    private String email;

    public AuthResponseDTO() {}

    public AuthResponseDTO(String token, String role, String email) {
        this.token = token;
        this.role = role;
        this.email = email;
    }

    /**
     * Get JWT token
     */
    public String getToken() {
        return token;
    }

    /**
     * Set JWT token
     */
    public void setToken(String token) {
        this.token = token;
    }

    /**
     * Get role
     */
    public String getRole() {
        return role;
    }

    /**
     * Set role
     */
    public void setRole(String role) {
        this.role = role;
    }

    /**
     * Get email
     */
    public String getEmail() {
        return email;
    }

    /**
     * Set email
     */
    public void setEmail(String email) {
        this.email = email;
    }
}