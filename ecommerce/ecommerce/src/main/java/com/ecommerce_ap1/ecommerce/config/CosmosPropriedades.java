package com.ecommerce_ap1.ecommerce.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "azure.cosmos")
public class CosmosPropriedades {
    private String uri;
    private String key;
    private String database;
    private boolean queryMetricsEnabled;
    private boolean responseDiagnosticsEnabled;
}