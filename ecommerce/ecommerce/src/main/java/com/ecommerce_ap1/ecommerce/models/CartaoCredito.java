package com.ecommerce_ap1.ecommerce.models;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity(name = "cartoes_credito")
public class CartaoCredito {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column
    private String numero;
    @Column
    private String validade;
    @Column
    private String cvv;
    @Column
    private Double limite;
    @Column
    private double saldoDisponivel;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;
}