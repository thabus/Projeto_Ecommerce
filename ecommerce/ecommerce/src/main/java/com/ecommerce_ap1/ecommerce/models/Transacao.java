package com.ecommerce_ap1.ecommerce.models;

import java.util.Date;

import com.azure.spring.data.cosmos.core.mapping.Container;

import jakarta.persistence.Id;
import lombok.Data;

@Data
@Container(containerName = "pedidos")
public class Transacao {

    @Id
    private String id;

    private String cartaoId;
    private Double valor;
    private Date dataTransacao;
    private String descricao;
}