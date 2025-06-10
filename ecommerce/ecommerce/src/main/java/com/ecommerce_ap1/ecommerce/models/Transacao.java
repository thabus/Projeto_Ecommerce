package com.ecommerce_ap1.ecommerce.models;

import java.util.Date;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.Data;

@Data
@Entity(name = "transacoes")
public class Transacao {

    @Id
    private String id;

    private String cartaoId;
    private Double valor;
    private Date dataTransacao;
    private String descricao;
}