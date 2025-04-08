package com.ecommerce_ap1.ecommerce.utils;

import org.springframework.stereotype.Component;

@Component
public class BigDataPublisher {

    public void enviarDadosVenda(String dadosVenda) {
        // Simulação de envio de dados para Azure Event Hubs
        System.out.println("Enviando dados para Big Data: " + dadosVenda);
    }
}
