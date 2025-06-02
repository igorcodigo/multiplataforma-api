## Coisas a adicionar:
<details>
   <summary style="color: gray; font-weight: bold;; font-size: 20px;"> Coisas a adicionar  </summary>

1. Aplicativo email que vai padronizar a integracao com o Resend e com o email da Hostinger.
Vai facilitar a integracao apenas precisando mudar as chaves e informar qual quer usar, pode inclusive colocar uma forma de usar um provedor pra cada tipo de coisa. Mas focar em .usar apenas um pra tudo primeiro
2. Inclusive ja criar as funcoes primordias, por exemplo, funcao de boas vindas quando o usuario eh cadastrado e funcao "esqueci a senha" para mudar a senha.(essas duas funcoes citadas vao ter integracao direta com o app accounts).
3. Fazer uma rotina de IA que quando eu criar os itens do banco de dados um modelo que usa chave estrangeira, por exemplo, aí ele vai tentar codar o modelo de que caso o modelo da chave estrangeira seja deletado aí o modelo filho ainda vai conseguir armazenar alguma informação para poder diferenciar saber a quem estava ligado
4. Docker entender mais e mudar de sqlite para outro banco de dados
5. Verificar se algum invasor ou atacante conseguir descobrir o endpoint de criação de usuário. Verificar se ele conseguirá ter acesso ao... endpoint de criar o usuário e poder criar o usuário com permissão de admin. Tentar evitar isso, caso seja possível. E criar proteções.
6. Criar um condicional que caso o acesso dos usuários seja feito exclusivamente para o aplicativo, inclusive a parte de redefinir a senha, então não incluir o botão e o link no e-mail de recuperar a senha.
8. Melhorar a parte do commit que verifica as diferenças entre as versões com inteligência artificial e faz o comentário.Utilizando os parâmetros do chat GPT-4 mini, como por exemplo temperatura e outras coisas.
</details>



# Como usar
## Passo 1 - Clonar este repositorio
- Use o seguinte comando para clonar todos os arquivos em uma pasta especifica. 
   ```sh
   git clone https://github.com/igorcodigo/Template-Django2.git .
   ```
- Caso deseje criar uma subpasta contendo os arquivos deste repo remova o ponto no final deste comando.

   ```sh
   git clone https://github.com/igorcodigo/Template-Django2.git 
   ```

## Passo 2 - Desconectar deste repositório remoto e conectar no repositório a sua escolha

<!-- ## Passo 2.1 - Caso deseje clonar todos os commits -->
<details>
  <summary style="color: gray; font-weight: bold;; font-size: 20px;"> 2.1 - Caso deseje clonar todos os commits  </summary>

- Execute esse conjunto de comando para verificar o repositório remoto atual, desconetar deste repositório remoto e para verificar se realmente se desconectou deste repositório.
   ```sh
   git remote -v
   git remote remove origin
   git remote -v
   ```
- Execute esse comando para se desconectar deste repositório remoto
   ```sh
   git remote remove origin
   ```
- Execute esse comando para verificar se realmente se desconectou deste repositório
   ```sh
   git remote -v
   ```
- Execute esse comando para se conectar ao repositório remoto desejado
   ```sh
   git remote add origin (link https de seu repositório remoto)
   ```
    
</details>  

<!-- ## Passo 2.2 - Recriar o git para nao puxar os commits anteriores (geralmente para usar o template em um projeto real) -->

<details>
  <summary style="color: gray; font-weight: bold;; font-size: 20px;"> 2.1 - Recriar o git para nao puxar os commits anteriores (geralmente para usar o template em um projeto real)  </summary>
  
   ```sh
   Remove-Item -Recurse -Force .git
   Write-Output "Acabou de passar do comando 'Remove-Item -Recurse -Force .git '" 
   git init
   git add .
   git commit -m "first commit"
   git branch -M main
   Write-Output "Configuracoes iniciais feitas, agora pode conectar ao repositorio remoto e git push " 
   git remote -v
   ```
- Execute esse comando para se conectar ao repositório remoto desejado
   ```sh
   git remote add origin (link https de seu repositório remoto)
   ```
- Execute esse comando para verificar se realmente se conectou a este repositório
   ```sh
   git remote -v
   ```

</details>

## Passo 3 - Fazer configuracoes iniciais 
<details>
   <summary style="color: gray; font-weight: bold;; font-size: 20px;"> (criar venv, instalar bibliotecas, fazer migracoes do banco de dados e criar super usuario)  </summary>

- Execute o arquivo "01_Main_config_file.ps1" que esta na pasta "Initial_Config"
   ```sh
   ....
   ```

</details>

## Passo 4 - Ligar o servidor

<details>
   <summary style="color: gray; font-weight: bold;; font-size: 20px;"> Execute o arquivo "Start_Venv_Django.bat"  </summary>

- Execute o arquivo "Start_Venv_Django.bat" que esta na pasta "z_automacoes_igor" para ligar o servidor e abrir o navegador
   ```sh
   ....
   ```

</details>

## Endpoints Disponíveis

### Endpoints de Administração

#### `/admin/`
- **Método**: GET, POST
- **Descrição**: Interface de administração do Django.
- **Acesso**: Apenas administradores autenticados.
- **Dados Enviados**: Credenciais de administrador (username e password) para login.
- **Resposta**: Interface web de administração do Django.

### Endpoints de Autenticação

#### `/contas/api/token/`
- **Método**: POST
- **Descrição**: Obtém um token JWT para autenticação.
- **Dados Enviados**:
  ```json
  {
    "username": "seu_usuario",
    "password": "sua_senha"
  }
  ```
- **Resposta**:
  ```json
  {
    "refresh": "token_refresh_jwt",
    "access": "token_access_jwt"
  }
  ```

#### `/contas/api/token/refresh/`
- **Método**: POST
- **Descrição**: Atualiza um token JWT expirado.
- **Dados Enviados**:
  ```json
  {
    "refresh": "token_refresh_jwt"
  }
  ```
- **Resposta**:
  ```json
  {
    "access": "novo_token_access_jwt"
  }
  ```

#### `/contas/login/`
- **Método**: GET, POST
- **Descrição**: Página de login para autenticação via interface web.
- **Dados Enviados (POST)**:
  ```
  username: seu_usuario
  password: sua_senha
  ```
- **Resposta (GET)**: Página HTML de login.
- **Resposta (POST bem-sucedido)**: Redirecionamento para a página inicial após autenticação.


Método de Criação: Na função create do serializer, é chamado o método create_user do gerenciador de usuários. Em implementações padrão (inclusive em customizações cuidadosas do modelo de usuário), o método create_user cria somente um usuário comum, sem os privilégios de superusuário. Para criar um superusuário, normalmente é necessário chamar explicitamente o método create_superuser, o que não ocorre neste endpoint.

Exposição do Endpoint: Embora o endpoint seja público (com permissão AllowAny), ele foi projetado para permitir apenas a criação de contas regulares. Mesmo se um invasor descobrisse o endpoint, ele só poderia criar um usuário comum.