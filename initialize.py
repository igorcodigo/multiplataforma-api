#initialize.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform
import shutil
import subprocess
import sys
import socket


def is_windows():
    """Verifica se o sistema operacional é Windows."""
    return platform.system().lower() == 'windows'


def run_docker_compose():
    """Executa o comando docker-compose com base no sistema operacional."""
    docker_compose_file = "docker/docker-compose.yml"
    
    print(f"Current working directory: {os.getcwd()}") # Debug
    print(f"Checking for docker-compose file at: {os.path.abspath(docker_compose_file)}") # Debug
    
    if not os.path.exists(docker_compose_file):
        print(f"Erro: Arquivo {docker_compose_file} não encontrado.")
        return False
    
    try:
        # Primeiro, parar e remover os containers existentes
        print("Parando e removendo containers existentes...")
        down_command = ["docker", "compose", "-f", docker_compose_file, "down"]
        
        if is_windows():
            subprocess.run(down_command, shell=True, check=True)
        else:
            subprocess.run(down_command, check=True)
            
        # Comando para executar docker-compose
        if platform.system().lower() == 'linux':
            print("Executando docker-compose no Linux com perfil de produção...")

            command = ["docker", "compose", "-f", docker_compose_file, "--profile", "production", "up", "--build", "-d"]
            
        else:
            # Para Windows e outros sistemas
            print("Executando docker-compose no Windows/Mac com perfil de desenvolvimento...")
            command = ["docker", "compose", "-f", docker_compose_file, "--profile", "development", "up", "--build", "-d"]
        
        # Em sistemas Windows, pode ser necessário usar um método diferente
        if is_windows():
            print("Executando docker-compose no Windows...")
            result = subprocess.run(command, shell=True, check=True)
        else:
            print("Executando docker-compose no Linux/Mac...")
            result = subprocess.run(command, check=True)
        
        if result.returncode == 0:
            print("Docker Compose executado com sucesso!")
            return True
        else:
            print(f"Erro ao executar Docker Compose. Código de saída: {result.returncode}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar Docker Compose: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

def create_env_from_example():
    # Locais possíveis para o arquivo .env.example
    possible_locations = [
        '.env.example',
        'docker/.env.example',
        'config/.env.example'
    ]
    
    print(f"Current working directory: {os.getcwd()}") # Debug
    print(f"Checking for .env.example in: {possible_locations}") # Debug
    
    # Procura o arquivo .env.example
    env_example_path = None
    for location in possible_locations:
        print(f"Checking path: {os.path.abspath(location)}") # Debug
        if os.path.exists(location):
            env_example_path = location
            break
    
    if env_example_path:
        # Verifica se .env já existe e notifica usuário
        if os.path.exists('.env'):
            print("Arquivo .env já existe. Sobrescrevendo...")
        else:
            print(f"Criando arquivo .env a partir de {env_example_path}...")
            
        shutil.copy2(env_example_path, '.env')
        
        print("Arquivo .env criado/atualizado com sucesso.")
        return True
    else:
        # Se não encontrou .env.example, não cria arquivo vazio
        print("Arquivo .env.example não encontrado. Nenhum arquivo .env foi criado.")
        return False

def main():
    """Função principal."""
    # Muda o diretório de trabalho para o diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Changed working directory to: {os.getcwd()}") # Debug
    
    print(f"Iniciando configuração no sistema: {platform.system()}")

    if is_windows():
        print("Sistema operacional: Windows")
    elif platform.system().lower() == 'linux':
        print("Sistema operacional: Linux")
    else:
        print(f"Sistema operacional: {platform.system()} (não Windows nem Linux)")
    
    # Cria o arquivo .env a partir do .env.example
    if not create_env_from_example():
        print("Falha ao criar o arquivo .env a partir do .env.example.")
        # Decide if this should be a fatal error
        # sys.exit(1) # Uncomment if this is critical for the script to continue
    
    # Executa o docker-compose
    if not run_docker_compose():
        print("Falha ao executar docker-compose.")
        sys.exit(1)
    
    print("Inicialização concluída com sucesso!")

if __name__ == "__main__":
    main() 