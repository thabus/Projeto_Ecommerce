package com.ecommerce_ap1.ecommerce.config;

import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
public class DatabaseConfig {
    @Bean
    public DataSource getDataSource() {
        return DataSourceBuilder.create()
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .url("jdbc:mysql://ibmec-cloud-ecommerce386296.mysql.database.azure.com/ecommerce")
                .username("arvore")
                .password("M1nhaarvore")
                .build();
    }
}