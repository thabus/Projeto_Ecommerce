package com.ecommerce_ap1.ecommerce.models;

import java.util.Date;
import java.util.List;

import com.azure.spring.data.cosmos.core.mapping.Container;

import jakarta.persistence.Id;
import lombok.Data;

@Data
@Container(containerName = "pedidos")
public class Pedido {

    @Id
    private String id;

    private String clienteId;
    private List<String> produtosIds;
    private Double valorTotal;
    private Date dataPedido;
    private String status;

}