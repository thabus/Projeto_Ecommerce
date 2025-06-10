package com.ecommerce_ap1.ecommerce.request;

import lombok.Data;
import java.util.List;

@Data
public class RealizarCompraRequest {
    private String clienteId;
    private List<String> produtosIds;
    private Integer cartaoId; 
}