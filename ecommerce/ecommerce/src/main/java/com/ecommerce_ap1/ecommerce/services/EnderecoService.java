package com.ecommerce_ap1.ecommerce.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ecommerce_ap1.ecommerce.models.Endereco;
import com.ecommerce_ap1.ecommerce.repositories.EnderecoRepository;

@Service
public class EnderecoService {

    @Autowired
    private EnderecoRepository enderecoRepository;

    public Endereco salvar(Endereco endereco) {
        return enderecoRepository.save(endereco);
    }

    public List<Endereco> listarPorUsuario(Integer usuarioId) {
        return enderecoRepository.findByUsuarioId(usuarioId);
    }

    public Endereco buscarPorId(Integer id) {
        return enderecoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Endereço não encontrado"));
    }

    public Endereco atualizarEndereco(Integer id, Endereco novoEndereco) {
        Endereco endereco = buscarPorId(id);
        endereco.setRua(novoEndereco.getRua());
        endereco.setCidade(novoEndereco.getCidade());
        endereco.setEstado(novoEndereco.getEstado());
        endereco.setCep(novoEndereco.getCep());
        return enderecoRepository.save(endereco);
    }
}
