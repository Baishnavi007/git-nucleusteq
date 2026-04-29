package com.baishnavi.restaurantOrderPortalBackend.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;

/**

  * Utility class for handling JWT (JSON Web Token) operations.
 */
@Component
public class JwtUtil {

    private static final String SECRET = "mySuperSecretKeyForJwtGeneration12345";
    private final Key key = Keys.hmacShaKeyFor(SECRET.getBytes());

    private static final long EXPIRATION_TIME = 1000 * 60 * 60;

    /**
     * Generates a JWT token for the given email and role.
     *
     * @param email the user's email (used as subject)
     * @param role  the role of the user (e.g., USER, OWNER)
     * @return generated JWT token as a String
     */
    public String generateToken(String email, String role) {
        return Jwts.builder()
                .setSubject(email)
                .claim("role", role)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * Extracts all claims from the given JWT token.
     *
     * @param token the JWT token
     * @return Claims object containing all token data
     */

    public Claims extractClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    /**
     * Extracts the email (subject) from the JWT token.
     *
     * @param token the JWT token
     * @return email stored in the token
     */
    public String extractEmail(String token) {
        return extractClaims(token).getSubject();
    }

    /**
     * Extracts the role from the JWT token.
     *
     * @param token the JWT token
     * @return role stored in the token
     */
    public String extractRole(String token) {
        return extractClaims(token).get("role", String.class);
    }

    /**
     * Validates the given JWT token.
     * @param token the JWT token
     * @return true if token is valid, false otherwise
     */
    public boolean validateToken(String token) {
        try {
            extractClaims(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}