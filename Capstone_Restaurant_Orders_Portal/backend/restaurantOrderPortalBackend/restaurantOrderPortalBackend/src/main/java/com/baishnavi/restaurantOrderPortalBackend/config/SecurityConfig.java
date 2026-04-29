package com.baishnavi.restaurantOrderPortalBackend.config;

import com.baishnavi.restaurantOrderPortalBackend.security.JwtFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Security configuration for the application.
 *
 * <p>
 * This class configures:
 * <ul>
 *     <li>JWT-based authentication (stateless)</li>
 *     <li>Role-based authorization (USER / RESTAURANT_OWNER)</li>
 *     <li>CORS handling for frontend-backend communication</li>
 *     <li>Disables CSRF (since we use JWT)</li>
 *     <li>Allows preflight (OPTIONS) requests for CORS</li>
 * </ul>
 * </p>
 */
@Configuration
public class SecurityConfig {

    private final JwtFilter jwtFilter;

    /**
     * Constructor injection of JWT filter
     *
     * @param jwtFilter custom JWT authentication filter
     */
    public SecurityConfig(JwtFilter jwtFilter) {
        this.jwtFilter = jwtFilter;
    }

    /**
     * Defines the security filter chain.
     *
     * @param http HttpSecurity object
     * @return configured SecurityFilterChain
     * @throws Exception in case of configuration errors
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        http
                // Disable CSRF (JWT based apps don't need it)
                .csrf(csrf -> csrf.disable())

                // Enable CORS using global configuration
                .cors(Customizer.withDefaults())

                // Stateless session (no session stored)
                .sessionManagement(session ->
                        session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                )

                // Authorization rules
                .authorizeHttpRequests(auth -> auth

                        // Allow preflight requests (VERY IMPORTANT for CORS)
                        .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()

                        // Public APIs (login/register)
                        .requestMatchers("/auth/**").permitAll()

                        // User APIs (wallet, restaurants, etc.)
                        .requestMatchers("/users/**").hasRole("USER")

                        // Restaurant Owner APIs
                        .requestMatchers("/owner/**").hasRole("RESTAURANT_OWNER")

                        // All other requests require authentication
                        .anyRequest().authenticated()
                )

                // Add JWT filter before Spring Security filter
                .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    /**
     * Password encoder bean for hashing passwords.
     *
     * @return BCryptPasswordEncoder instance
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}