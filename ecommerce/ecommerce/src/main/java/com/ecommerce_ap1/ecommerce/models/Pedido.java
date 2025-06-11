package com.ecommerce_ap1.ecommerce.models;

import java.util.Date;
import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.Data;

@Data
@Entity(name = "pedidos")
public class Pedido {

    @Id
    private String id;

    private String usuarioId;
    private String usuarioNome;
    private List<String> produtosIds;
    private List<String> produtos;
    private Double valorTotal;
    private Date dataPedido;
    private String status;

}