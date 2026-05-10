package com.baishnavi.restaurantOrderPortalBackend.dto;

/**
 * DTO for user response
 */
public class UserDTO {

    private Long id;
    private String firstName;
    private String email;
    private String role;
    private Double walletBalance;

    public UserDTO() {}

    public UserDTO(Long id, String firstName, String email,
                   String role, Double walletBalance) {
        this.id = id;
        this.firstName = firstName;
        this.email = email;
        this.role = role;
        this.walletBalance = walletBalance;
    }

    /**
     * Getters & Setters

     */
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }

    public Double getWalletBalance() { return walletBalance; }
    public void setWalletBalance(Double walletBalance) { this.walletBalance = walletBalance; }
}