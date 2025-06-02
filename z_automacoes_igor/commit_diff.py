import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Variável para definir uma branch obrigatória para push
BRANCH_OBRIGATORIA = 'main'  # Defina um valor aqui para forçar o uso de uma branch específica

# Detecta automaticamente o username do sistema e define a branch apropriada
def detectar_branch_por_usuario():
    home_path = os.path.expanduser("~")
    if "\\pedro" in home_path or "/pedro" in home_path:
        return "devpedro"
    elif "\\igor1" in home_path or "/igor1" in home_path:
        return "devigor"
    else:
        # Default ou fallback caso não seja nenhum dos usuários esperados
        return "dev"

# Variável global para especificar a branch de destino para o push
# Usa a branch obrigatória se definida, caso contrário detecta pelo usuário
BRANCH_DESTINO = BRANCH_OBRIGATORIA if BRANCH_OBRIGATORIA else detectar_branch_por_usuario()

# Diretório onde serão salvos os arquivos de diferenças
DIRETORIO_SAIDA = 'utils/itens-temporarios'

# Calcula o caminho completo do diretório de saída uma única vez
CAMINHO_SAIDA = os.path.join(Path(__file__).resolve().parent, DIRETORIO_SAIDA)
os.makedirs(CAMINHO_SAIDA, exist_ok=True)


def encontrar_repositorio_git():
    """
    Encontra o repositório Git mais próximo começando pelo diretório do script atual
    e subindo na hierarquia de diretórios.
    """
    # Obtém o caminho absoluto do diretório onde está o script atual
    caminho_script = Path(__file__).resolve().parent
    print(
        f'\nIniciando busca pelo repositório Git a partir de: {caminho_script}'
    )

    caminho_atual = caminho_script
    while True:
        print(f'Verificando diretório: {caminho_atual}')

        # Verifica se existe um diretório .git no caminho atual
        git_dir = caminho_atual / '.git'
        if git_dir.is_dir():
            print(f'Repositório Git encontrado em: {caminho_atual}')
            return str(caminho_atual)

        # Verifica se chegamos à raiz do sistema
        if caminho_atual == caminho_atual.parent:
            print('Atingiu a raiz do sistema sem encontrar um repositório Git')
            break

        # Move para o diretório pai
        caminho_atual = caminho_atual.parent

    raise Exception(
        'Repositório Git não encontrado. Certifique-se de estar dentro de um repositório válido.'
    )


def salvar_diferencas(arquivo_saida='diferencas.txt'):
    try:
        # Encontra o repositório Git mais próximo
        caminho_repositorio = encontrar_repositorio_git()
        print(f'Usando repositório Git em: {caminho_repositorio}')

        # Alterar para o diretório do repositório Git
        os.chdir(caminho_repositorio)
        print(f'Diretório atual alterado para: {os.getcwd()}')

        print(f'Diretório de saída: {CAMINHO_SAIDA}')

        def executar_comando_git(comando):
            return subprocess.run(
                comando, capture_output=True, text=True, encoding='utf-8', errors='replace'
            )

        # Tenta o primeiro comando
        resultado = executar_comando_git(['git', 'diff', '--find-renames'])

        # Se não houver saída (nada detectado), tenta com --no-renames
        if not resultado.stdout.strip():
            print("O 'git diff --find-renames' não encontrou diferenças, tentando sem renomeações")
            resultado = executar_comando_git(['git', 'diff', '--no-renames'])

        # Se ainda assim não tiver saída, verifica se há algo staged
        if not resultado.stdout.strip():
            print("Ainda não encontrou diferenças, tentando com --staged")
            resultado = executar_comando_git(['git', 'diff', '--staged'])

        # Último recurso: pega todas as diferenças do HEAD
        if not resultado.stdout.strip():
            print("Nenhuma diferença detectada, tentando diff completo com HEAD")
            resultado = executar_comando_git(['git', 'diff', 'HEAD'])

        if not resultado.stdout.strip():
            print("O 'git diff --find-renames' não encontrou diferenças")
            resultado = executar_comando_git(['git', 'diff', '--staged'])

        if resultado.returncode != 0:
            print('Erro ao executar git diff:', resultado.stderr)
            return

        # Garante que o caminho do arquivo de saída está no diretório especificado
        arquivo_saida = os.path.join(CAMINHO_SAIDA, arquivo_saida)

        # Salva as diferenças em um arquivo
        with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
            arquivo.write(resultado.stdout)

        print(f'As diferenças foram salvas no arquivo: {arquivo_saida}')
        return arquivo_saida

    except Exception as e:
        print(f'Erro: {e}')
        # Adiciona mais detalhes sobre o erro
        import traceback

        print('\nDetalhes do erro:')
        print(traceback.format_exc())
        return None


def gerar_resposta_IA(prompt):
    global custo_estimado
    response = client.chat.completions.create(
        model='o1-mini',
        max_completion_tokens=2000,
        messages=[{'role': 'assistant', 'content': prompt}],
    )
    resposta_limpa = response.choices[0].message.content.replace(
        '**', ''
    )  # Remove os asteriscos

    # Obtenha a utilização de tokens da resposta
    usage = (
        response.usage
    )  # Geralmente um dicionário com 'prompt_tokens', 'completion_tokens' e 'total_tokens'
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    print(f'Tokens do prompt: {prompt_tokens}')
    print(f'Tokens da resposta: {completion_tokens}')
    print(f'Total de tokens: {total_tokens}')

    # Calcular custo estimado (substitua o valor pelo custo real do seu modelo)
    custo_por_1000000_tokens = 1.10
    custo_estimado = (total_tokens / 1000000) * custo_por_1000000_tokens * 6
    print(f'Custo estimado: RS$ {custo_estimado:.4f}')

    return resposta_limpa


def gerar_resumo_ia(conteudo_diff):
    prompt = f"""
    Analise as diferenças do código abaixo entre o estado atual e o último commit. Explique as mudanças utilizando termos da programacao. Comece sempre com o resumo inicial. Seguindo esse template:

    Resumo inicial: 
    - Priorize as mudanças funcionais ou de comportamento do sistema. Faça uma explicação curta, concisa, mas específica, e numere os itens. 
    - Evite incluir pontos secundários como refatoração de código, mudancas de estilo, adição de comentários ou simples mudanças de formatação, a menos que impactem diretamente a funcionalidade ou a lógica do código.

    Detalhes: 
    - Expanda a explicação das mudanças, abordando de maneira técnica cada ponto numerado no resumo.
    - Inclua aspectos relevantes que não foram mencionados no resumo inicial, como melhorias de performance ou questões de estilo de codificação que impactam o funcionamento, se houver.

    Arquivos modificados e o resumo em ate 12 palavras da modificacao de cada arquivo:
    - Liste os arquivos modificados
    Liste os arquivos que foram modificados

    Essas sao as diferenças:
    {conteudo_diff}
    """
    comentario_ia = gerar_resposta_IA(prompt)

    # Salvar o comentário gerado pela IA em um arquivo
    caminho_comentario = os.path.join(CAMINHO_SAIDA, 'diferencas_coments.txt')

    with open(caminho_comentario, 'w', encoding='utf-8') as comentario_arquivo:
        comentario_arquivo.write(comentario_ia.replace('\n', ' ', 3))

    print(f"Comentário gerado pela IA foi salvo em '{caminho_comentario}'")
    return comentario_ia


def adicionar_mudancas_ao_stage_commit_e_push():
    try:
        # Garante que estamos no diretório do repositório
        os.chdir(encontrar_repositorio_git())

        print(f'Custo estimado: RS$ {custo_estimado:.4f}')
        # Pergunta ao usuário se deseja adicionar as mudanças ao stage e fazer o commit
        resposta = input(
            f"Deseja adicionar as mudanças ao stage e fazer o commit na branch {BRANCH_DESTINO}? Digite '1' para sim, '2' para mudanças padrão, '0' para cancelar: "
        )

        if resposta == '1':
            subprocess.run(['git', 'add', '.'], check=True)
            print('Mudanças adicionadas ao stage.')

            caminho_comentario = os.path.join(
                CAMINHO_SAIDA, 'diferencas_coments.txt'
            )
            with open(
                caminho_comentario, 'r', encoding='utf-8'
            ) as comentario_arquivo:
                commit_message = comentario_arquivo.read()

            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f'Commit realizado com a mensagem: {commit_message}')

            # Usa a variável global BRANCH_DESTINO para especificar a branch de destino
            subprocess.run(
                ['git', 'push', 'origin', BRANCH_DESTINO], check=True
            )
            print(
                f"Mudanças enviadas para a branch '{BRANCH_DESTINO}' no repositório remoto."
            )

        elif resposta == '2':
            subprocess.run(['git', 'add', '.'], check=True)
            print('Mudanças adicionadas ao stage.')

            commit_message = 'Mudanças padrões realizadas ou arquivos movidos'
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f'Commit realizado com a mensagem: {commit_message}')

            # Também adiciona o push para a opção 2, usando a variável global
            resposta_push = input(
                f"Deseja enviar as mudanças para a branch '{BRANCH_DESTINO}'? Digite '1' para sim, '0' para não: "
            )
            if resposta_push == '1':
                subprocess.run(
                    ['git', 'push', 'origin', BRANCH_DESTINO], check=True
                )
                print(
                    f"Mudanças enviadas para a branch '{BRANCH_DESTINO}' no repositório remoto."
                )

        elif resposta == '0':
            print('Commit não realizado. Processo cancelado.')

        else:
            print('Opção inválida. Commit não realizado.')

    except Exception as e:
        print(f'Erro ao adicionar mudanças e fazer o commit: {e}')


def main():
    custo_estimado = ''
    # Carregar as variáveis do arquivo .env
    load_dotenv()
    global client
    client = OpenAI(
        api_key=os.getenv('OPEN_AI_API_KEY'),
    )

    # Salvar as diferenças
    arquivo_saida = salvar_diferencas()
    if arquivo_saida:
        # Processar as diferenças e gerar o comentário
        with open(arquivo_saida, 'r', encoding='utf-8') as arquivo:
            conteudo_diff = arquivo.read()
            print(gerar_resumo_ia(conteudo_diff)[:100])

        # Adicionar mudanças ao stage e fazer o commit
        adicionar_mudancas_ao_stage_commit_e_push()


if __name__ == '__main__':
    main()
