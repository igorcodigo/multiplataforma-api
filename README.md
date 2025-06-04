# 🌐 PlataformaEduca - Microserviço da API

Este repositório contém o microserviço da API RESTful para a PlataformaEduca. Desenvolvido com Django e Django REST framework, este back-end é responsável por gerenciar a autenticação de usuários, a área de comentários e outras funcionalidades essenciais da plataforma, servindo como base para o front-end da PlataformaEduca.

## 🛠️ Tecnologias Principais

*   **Framework Back-end**: Django, Django REST framework
*   **Banco de Dados**: SQLite
*   **Segurança**: As senhas dos usuários são protegidas utilizando técnicas modernas de hash e criptografia.
*   **Contêinerização**: Docker, para garantir um ambiente de desenvolvimento e produção consistente e facilitar o deployment.
*   **CI/CD**: GitHub Actions, para automação dos processos de integração e entrega contínua.

## 🚀 Funcionalidades da API

Este microserviço fornece endpoints para:

*   **Autenticação e Gerenciamento de Usuários**:
    *   Registro de novos usuários.
    *   Login de usuários com autenticação segura.
    *   (Endpoints para gerenciamento de perfis de usuário, se aplicável)
*   **Área de Comentários (Chat)**:
    *   Criação de novos comentários.
    *   Visualização de comentários.
    *   Edição de comentários existentes (restrito ao autor).
    *   Exclusão de comentários (restrito ao autor).
*   **(Outras funcionalidades conforme a evolução da plataforma)**
