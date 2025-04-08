package com.ecommerce_ap1.ecommerce.models;

import com.azure.spring.data.cosmos.core.mapping.Container;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.util.UUID;

@Data
@Container(containerName = "produtos")
public class Produto {

    @Id
    private String id;

    private String nome;
    private String descricao;
    private Double preco;
    private Integer estoque;

    public Produto() {
        this.id = UUID.randomUUID().toString();
    }
}