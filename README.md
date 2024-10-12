# Detecção Automática de Placas de carro

# Intruções para executar o código

É recomendado utilizar python=3.12 e um ambiente virtual. Seguem as instruções:

## Instruções para a instalação do mini-conda

É recomendado a instalação do mini-conda para a melhor instalação dos pacotes sem comprometer o python global. É possível também rodar sem a utilização de uma venv (ambiente virtual) ou até mesmo com uma venv python, mas é recomendado que se utilize o mini-conda pela facilidade da troca de versões do python.

### Instalação no Linux

Baixe o instalador via terminal com wget ou similar:
```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Navegue até a pasta onde o instalador foi baixado:

```sh
cd /caminho/para/o/arquivo
```

Execute o script:
```sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Ativar o Miniconda

Após a instalação, feche e reabra o terminal ou execute o seguinte comando para ativar o conda:
```
source ~/miniconda3/bin/activate
```

### Instalação no Windows


**Baixar o Instalador do Miniconda**

Acesse o site oficial: https://docs.conda.io/en/latest/miniconda.html.
Escolha a versão para Windows, de acordo com sua arquitetura (32 bits ou 64 bits).
Baixe o instalador recomendado (geralmente a versão de 64 bits).

![O link para o mini-conda é este acima]("./resources/windows.png")


**Executar o Instalador**

- Após o download, execute o arquivo .exe baixado.
- Selecione a opção "Just Me" para instalar o Miniconda apenas para o usuário atual.
- Aceite os termos da licença e escolha o local onde deseja instalar (ou deixe o caminho padrão).
- Importante: Durante a instalação, marque a caixa que diz "Add Miniconda3 to my PATH environment variable" (se você quiser acessar o conda pelo terminal diretamente). Cuidado, pois isso pode alterar outras versões do Python instaladas no sistema.
- Finalize a instalação.


## Criando o ambiente virtual e instando as dependências:

Na pasta do projeto, crie um ambiente virtual com o seguinte comando:

```sh
conda create -n viscomp -python=3.12
```
Após isso, ative o ambiente:

```sh
conda activate viscomp
```

Com isso podemos instalar as dependências.

```sh
pip install -r requirements.txt
```

## Executando o código:

Para executar o código, certifique-se que está na pasta do projeto e então execute o seguinte comando:

Agora, você pode rodar o script pelo terminal da seguinte forma:

Para rodar o script sem usar a GPU:

```bash
python main.py organic-data/video_teste_1.mp4
```

Para rodar o script usando a GPU:

```sh
python main.py organic-data/video_teste_1.mp4 --gpu
```

Caso se tente executar o script com gpu sem possuir gpu na sua máquina, o código não irá funcionar.