package com.ecommerce_ap1.ecommerce.models;

import jakarta.persistence.*;
import lombok.Data;
import com.fasterxml.jackson.annotation.JsonBackReference;

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
    private Integer cvv;
    @Column
    private Double limite;
    @Column
    private double saldoDisponivel;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    @JsonBackReference
    private Usuario usuario;
}