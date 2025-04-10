package com.ecommerce_ap1.ecommerce.models;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
@Container(containerName = "produtos")
public class Produto {

    @Id
    private String id;

    @PartitionKey
    private String produtoCategoria;

    private String nome;
    private String descricao;
    private Double preco;
    private Integer estoque;

}