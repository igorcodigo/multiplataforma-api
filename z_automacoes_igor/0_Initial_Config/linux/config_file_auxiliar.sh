source .venv/bin/activate

echo "Criando migrações..."
python3 manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Erro ao criar migrações"
    read -p "Pressione Enter para sair..."
    exit 1
fi

echo "Para realizar as migrações no banco de dados pressione Enter"
read -p ""
python3 manage.py migrate

echo "Criando super usuário"
python3 manage.py createsuperuser

cd Initial_Config
CURRENT_DIR=$(pwd)
echo $CURRENT_DIR
rm -rf "$CURRENT_DIR"*

read -p "Pressione Enter para sair..."