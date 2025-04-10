package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.models.Endereco;
import com.ecommerce_ap1.ecommerce.models.Usuario;
import com.ecommerce_ap1.ecommerce.repositories.UsuarioRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UsuarioService {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Transactional
public Usuario criarUsuarioComCartoes(Usuario usuario) {
    if (usuario.getCartoes() == null || usuario.getCartoes().isEmpty()) {
        throw new IllegalArgumentException("Usuário deve ter pelo menos um cartão de crédito.");
    }

    // setar o usuário em cada cartão
    for (CartaoCredito cartao : usuario.getCartoes()) {
        cartao.setUsuario(usuario);
    }

    // setar o usuário em cada endereço
    if (usuario.getEnderecos() != null) {
        for (Endereco endereco : usuario.getEnderecos()) {
            endereco.setUsuario(usuario);
        }
    }

    return usuarioRepository.save(usuario);
}


    public List<Usuario> listarUsuarios() {
        return usuarioRepository.findAll();
    }

    public Optional<Usuario> buscarUsuarioPorId(Integer id) {
        return usuarioRepository.findById(id);
    }

    public Usuario atualizarUsuario(Integer id, Usuario dadosAtualizados) {
        Usuario usuario = usuarioRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Usuário não encontrado"));

        if (dadosAtualizados.getNome() != null) {
            usuario.setNome(dadosAtualizados.getNome());
        }

        if (dadosAtualizados.getEmail() != null) {
            usuario.setEmail(dadosAtualizados.getEmail());
        }

        if (dadosAtualizados.getCartoes() != null) {
            for (CartaoCredito cartao : dadosAtualizados.getCartoes()) {
                cartao.setUsuario(usuario);
            }
            usuario.setCartoes(dadosAtualizados.getCartoes());
        }

        if (dadosAtualizados.getEnderecos() != null) {
            for (Endereco endereco : dadosAtualizados.getEnderecos()) {
                endereco.setUsuario(usuario);
            }
            usuario.setEnderecos(dadosAtualizados.getEnderecos());
        }

        return usuarioRepository.save(usuario);
    }

}
