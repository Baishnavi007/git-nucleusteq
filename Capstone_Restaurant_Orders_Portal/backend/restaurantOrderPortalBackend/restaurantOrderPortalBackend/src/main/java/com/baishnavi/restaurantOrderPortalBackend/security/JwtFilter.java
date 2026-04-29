package com.baishnavi.restaurantOrderPortalBackend.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;

import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

/**
 * JWT Authentication Filter

 * It ensures that secured endpoints can only be accessed
 * by authenticated users with proper roles.
 *
 */
@Component
public class JwtFilter extends OncePerRequestFilter {

    private final JwtUtil jwtUtil;

    /**
     * Constructor-based dependency injection
     *
     * @param jwtUtil utility class for JWT operations
     */
    public JwtFilter(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    /**
     * Core filtering logic
     *
     * @param request     incoming HTTP request
     * @param response    outgoing HTTP response
     * @param filterChain filter chain
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        try {
            // Extract Authorization header
            String header = request.getHeader("Authorization");

            if (header != null && header.startsWith("Bearer ")) {

                // Extract token
                String token = header.substring(7);

                // Validate token
                if (jwtUtil.validateToken(token)) {

                    // Extract user details
                    String email = jwtUtil.extractEmail(token);
                    String role = jwtUtil.extractRole(token);

                    /**
                     * Normalize role:
                     * - If role is "USER" → convert to "ROLE_USER"
                     * - If already "ROLE_USER" → keep as it is
                     */
                    if (role != null && !role.startsWith("ROLE_")) {
                        role = "ROLE_" + role;
                    }


                    List<SimpleGrantedAuthority> authorities =
                            List.of(new SimpleGrantedAuthority(role));


                    UsernamePasswordAuthenticationToken auth =
                            new UsernamePasswordAuthenticationToken(email, null, authorities);


                    SecurityContextHolder.getContext().setAuthentication(auth);


                    System.out.println("Authenticated user: " + email);
                    System.out.println("Assigned role: " + role);
                }
            }

        } catch (Exception ex) {
            /**
             * IMPORTANT:
             * Do NOT break the request if token fails
             * Let Spring Security handle unauthorized cases
             */
            System.out.println("JWT Filter Error: " + ex.getMessage());
        }

        // Continue filter chain
        filterChain.doFilter(request, response);
    }
}