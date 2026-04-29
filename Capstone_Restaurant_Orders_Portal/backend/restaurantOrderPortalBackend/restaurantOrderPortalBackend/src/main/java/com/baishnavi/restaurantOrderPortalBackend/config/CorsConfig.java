package com.baishnavi.restaurantOrderPortalBackend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;

import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

import java.util.List;

/**
 * Global CORS configuration
 *
 * <p>
 * Allows frontend (HTML/JS running on different origin)
 * to communicate with backend APIs.
 * </p>
 */
@Configuration
public class CorsConfig {

    /**
     * Defines global CORS policy
     *
     * @return CorsFilter bean
     */
    @Bean
    public CorsFilter corsFilter() {

        CorsConfiguration config = new CorsConfiguration();


        config.setAllowedOrigins(List.of("http://127.0.0.1:5500", "http://localhost:5500"));

        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));


        config.setAllowedHeaders(List.of("*"));


        config.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();


        source.registerCorsConfiguration("/**", config);

        return new CorsFilter(source);
    }
}