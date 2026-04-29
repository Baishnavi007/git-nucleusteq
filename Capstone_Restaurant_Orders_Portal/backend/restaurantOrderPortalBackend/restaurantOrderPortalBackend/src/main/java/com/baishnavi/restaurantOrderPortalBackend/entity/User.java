package com.baishnavi.restaurantOrderPortalBackend.entity;

import com.baishnavi.restaurantOrderPortalBackend.enums.Role;
import jakarta.persistence.*;
import jakarta.validation.constraints.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;

/**
 * Entity representing application users.
 *
 * <p>
 * This class maps to the "users" table in the database and stores
 * user-related information such as name, email, phone number,
 * role, wallet balance, and associated addresses.
 * </p>
 */
@Entity
@Table(name = "users")
public class User {

    /**
     * Primary key of the user
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * First name of the user
     */
    @NotBlank(message = "First name is mandatory")
    private String firstName;

    /**
     * Last name of the user
     */
    @NotBlank(message = "Last name is mandatory")
    private String lastName;

    /**
     * Phone number of the user
     */
    @NotBlank(message = "Phone number is mandatory")
    private String phoneNumber;

    /**
     * Unique email of the user (used for login)
     */
    @Column(unique = true, nullable = false)
    @Email(message = "Invalid email format")
    @NotBlank(message = "Email is mandatory")
    private String email;

    /**
     * Encrypted password of the user
     */
    @NotBlank(message = "Password is mandatory")
    private String password;

    /**
     * Role of the user (USER / RESTAURANT_OWNER)
     */
    @Enumerated(EnumType.STRING)
    @NotNull(message = "Role is mandatory")
    private Role role;

    /**
     * Wallet balance of the user
     */
    @NotNull
    private Double walletBalance;

    /**
     * Created timestamp of the user
     */
    @NotNull
    private LocalDateTime createdAt;

    /**
     * List of addresses associated with the user
     */
    @OneToMany(mappedBy = "user")
    private List<Address> addresses;

    /**
     * Currently selected address ID
     */
    private Long selectedAddressId;

    /**
     * Default constructor (required by JPA)
     */
    public User() {}

    /**
     * All arguments constructor
     */
    public User(Long id, String firstName, String lastName, String phoneNumber,
                String email, String password, Role role, Double walletBalance,
                LocalDateTime createdAt, List<Address> addresses, Long selectedAddressId) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.phoneNumber = phoneNumber;
        this.email = email;
        this.password = password;
        this.role = role;
        this.walletBalance = walletBalance;
        this.createdAt = createdAt;
        this.addresses = addresses;
        this.selectedAddressId = selectedAddressId;
    }

    // ================= GETTERS & SETTERS =================

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }

    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }

    public String getPhoneNumber() { return phoneNumber; }
    public void setPhoneNumber(String phoneNumber) { this.phoneNumber = phoneNumber; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public Role getRole() { return role; }
    public void setRole(Role role) { this.role = role; }

    public Double getWalletBalance() { return walletBalance; }
    public void setWalletBalance(Double walletBalance) { this.walletBalance = walletBalance; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public List<Address> getAddresses() { return addresses; }
    public void setAddresses(List<Address> addresses) { this.addresses = addresses; }

    public Long getSelectedAddressId() { return selectedAddressId; }
    public void setSelectedAddressId(Long selectedAddressId) { this.selectedAddressId = selectedAddressId; }

    // ================= OVERRIDDEN METHODS =================

    /**
     * String representation (excluding sensitive fields like password)
     */
    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", firstName='" + firstName + '\'' +
                ", email='" + email + '\'' +
                ", role=" + role +
                ", walletBalance=" + walletBalance +
                '}';
    }

    /**
     * Equality based on ID
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User)) return false;
        User user = (User) o;
        return id != null && id.equals(user.id);
    }

    /**
     * Hashcode based on ID
     */
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}