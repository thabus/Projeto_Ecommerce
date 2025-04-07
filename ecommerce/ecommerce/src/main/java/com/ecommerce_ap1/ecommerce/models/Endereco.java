package com.ecommerce_ap1.ecommerce.models;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity(name = "enderecos")
public class Endereco {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column
    private String rua;
    @Column
    private String numero;
    @Column
    private String cidade;
    @Column
    private String estado;
    @Column
    private String cep;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;
}
