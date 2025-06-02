
sudo chmod -R 777 Initial_Config/

echo "Criando a venv..."

python3 -m venv .venv

source .venv/bin/activate

echo "Instalando as bibliotecas necessarias a partir do arquivo 'requirements.txt' "
pip install -r requirements.txt

./Initial_Config/linux/config_file_auxiliar.sh


echo "Pressione Enter para fechar a janela..."
read -r

kill $$