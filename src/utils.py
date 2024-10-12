import cv2
import easyocr
import numpy as np
from src.inference import inference
from collections import deque, Counter
from difflib import SequenceMatcher
from roboflow import Roboflow

def get_config(config: dict) -> tuple:
    rf= Roboflow(api_key=config["API_KEY"])
    project = rf.workspace(config["WORKSPACE"]).project(config["PROJECT"])
    version = project.version(int(config["VERSION"]))
    return project, version

def get_dataset(version):
    dataset = version.dataset()
    return dataset

# Função para cortar a placa usando as coordenadas da bounding box
def cortar_placa(frame, bounding_box):
    x_min, y_min, x_max, y_max = map(int, bounding_box)
    return frame[y_min:y_max, x_min:x_max]


def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarização usando método de Otsu
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Remover ruído usando GaussianBlur
    blurred = cv2.GaussianBlur(binary, (3, 3), 0)

    # Redimensionar a imagem para melhor OCR
    width = 800  # Defina a largura desejada
    height = int(blurred.shape[0] * (width / blurred.shape[1]))
    resized = cv2.resize(blurred, (width, height))

    # Aplicar dilatação e erosão
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(resized, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    # Ajuste de contraste
    contrast_enhanced = cv2.convertScaleAbs(eroded, alpha=1, beta=0)

    return contrast_enhanced

# Função para realizar OCR na imagem da placa
def detectar_caracteres(img, leitor):
    #img_preprocessada = preprocess_image(img)
    img_preprocessada = img

    # Definir a lista de caracteres permitidos (apenas letras maiúsculas e números)
    allowlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    # Fazer OCR na imagem
    resultado = leitor.readtext(np.array(img_preprocessada), allowlist=allowlist)

    # Extrair o texto detectado
    texto_detectado = " ".join([res[1] for res in resultado])

    # Verificar se a placa tem 7 caracteres
    if len(texto_detectado) == 7:
        return texto_detectado
    else:
        return None

# Função para calcular similaridade entre duas strings
def calcular_similaridade(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

# Função para contar caracteres e usar sistema de votação por caractere
def atualizar_votacao_caracteres(placa_atual, nova_placa, votos_caracteres):
    for i, caractere in enumerate(nova_placa):
        if i < len(placa_atual):
            # Adicionar o caractere ao contador de votos na posição i
            votos_caracteres[i].update([caractere])

# Função para formar a placa mais provável com base nos votos de cada caractere
def formar_placa_por_votacao(votos_caracteres):
    return "".join([votos.most_common(1)[0][0] for votos in votos_caracteres])

# Função para detectar se uma nova placa deve ser considerada
def detectar_nova_placa(placa_atual, nova_placa):
    # Contar quantos caracteres são diferentes entre as placas
    diferencas = sum([1 for a, b in zip(placa_atual, nova_placa) if a != b])
    return diferencas >= 5  # Se 5 ou mais caracteres forem diferentes, é uma nova placa

# Função para processar vídeo frame a frame e salvar o resultado
def processar_video(video_path, gpu=True):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        return

    # Inicializar o leitor do EasyOCR fora do loop
    leitor = easyocr.Reader(['pt', 'en'], gpu=gpu)

    placa_atual = None  # Placa atual inferida
    votos_caracteres = []  # Lista de contadores de votos por posição de caractere

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Chamar o modelo de inferência para obter as coordenadas da placa
        result = inference(frame)
        if len(result.boxes) > 0:  # Verificar se há alguma placa detectada
            bbox = result.boxes.xyxy[0].tolist()  # Obter a primeira caixa delimitadora

            # Cortar a placa com base nas coordenadas da inferência
            placa_img = cortar_placa(frame, bbox)

            # Detectar caracteres da placa
            texto_detectado = detectar_caracteres(placa_img, leitor)
            if texto_detectado is not None:
                if placa_atual is None:
                    # Primeira placa detectada
                    placa_atual = texto_detectado
                    votos_caracteres = [Counter() for _ in range(len(placa_atual))]
                    print(f"Nova placa detectada: {placa_atual}")
                else:
                    if detectar_nova_placa(placa_atual, texto_detectado):
                        # Considerar uma nova placa
                        placa_atual = texto_detectado
                        votos_caracteres = [Counter() for _ in range(len(placa_atual))]
                        print(f"Nova placa detectada: {placa_atual}")
                    else:
                        # Atualizar os votos de cada caractere
                        atualizar_votacao_caracteres(placa_atual, texto_detectado, votos_caracteres)
                        # Formar a nova placa inferida com base nos votos
                        placa_inferida = formar_placa_por_votacao(votos_caracteres)
                        if placa_inferida != placa_atual:
                            placa_atual = placa_inferida
                            print(f"Placa inferida: {placa_atual}")

            # Desenhar o bounding box e o texto detectado no frame
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
            
            # faça um fundo branco para o texto na parte superior esquerda e coloque o texto da placa

            top_left_x = 10  # Margem da borda esquerda
            top_left_y = 40 
            # Desenha o retângulo no canto superior da tela
            cv2.rectangle(frame, (top_left_x, top_left_y - 30), (top_left_x + 200, top_left_y), (255, 255, 255), -1)

            # Coloca o texto no retângulo desenhado
            cv2.putText(frame, placa_atual, (top_left_x + 5, top_left_y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
            # faça um fundo branco para o texto
            

        # Escrever o frame processado no arquivo de vídeo de saída
        # out.write(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar o vídeo e o objeto VideoWriter
    cap.release()
    #print(f"Processamento concluído. Vídeo salvo em: {output_path}")
