import os
import re


def search_term_in_files(directory, term, ignore_dirs=None, ignore_files=None):
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    results = []
    # Compilar o padrão de termo para a busca
    term_pattern = re.compile(term, re.IGNORECASE)

    # Caminhar pelo diretório e subdiretórios
    for root, dirs, files in os.walk(directory):
        # Remover diretórios que devem ser ignorados da lista de diretórios a serem explorados
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            # Ignorar arquivos específicos
            if file in ignore_files:
                continue

            file_path = os.path.join(root, file)
            try:
                # Abrir e ler o conteúdo do arquivo
                with open(
                    file_path, 'r', encoding='utf-8', errors='ignore'
                ) as f:
                    content = f.read()
                    # Procurar pelo termo no conteúdo
                    if term_pattern.search(content):
                        results.append(file_path)
            except Exception as e:
                print(f'Erro ao ler o arquivo {file_path}: {e}')

    return results


# Exemplo de uso
directory = os.getcwd()  # Obter o diretório atual automaticamente
term = '1'  # Substitua pelo termo que deseja buscar

# Defina os diretórios e arquivos que serão ignorados
ignore_dirs = ['venv', '.venv', '__pycache__', '.git']
ignore_files = ['ignore_me.txt', 'ignore_this.log']

found_files = search_term_in_files(directory, term, ignore_dirs, ignore_files)

print(f'O termo "{term}" foi encontrado nos seguintes arquivos:')
for file in found_files:
    print(file)
print(
    f'--------------------------------------------------------------------------------- '
)
