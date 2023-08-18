import cv2
import os
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
from skimage.transform import resize
import matplotlib.offsetbox as offsetbox

estacoes = ["ESTACAO_VILA_MOEMA", "ESTACAO_CAPIVARI_DE_BAIXO", "ESTACAO_SAO_BERNARDO"]
for estacao in estacoes:

    df = pd.read_csv('/caminho/'+estacao+'.csv', names=[
                    'Time',
                    'Velocidade do Vento (m/s)',
                    'Direção do Vento (°)',
                    'Temperatura a 2m (°C)',
                    'Umidade Relativa (%RH)',
                    'Pressão ao Nível do Mar (hPa)',
                    'SO2 (µg/m³)',
                    '1'])

    has_hour = df['Time'].str.contains(':')
    null_indices = np.where(~has_hour)[0]
    df = df.reset_index()
    df.loc[null_indices, 'Time'] = df.loc[null_indices, 'Time'] + " 00:00:00"
    df['Time'] = df['Time'].apply(lambda x: pd.to_datetime(str(x)[:16].replace('/', '-'), format='%Y-%m-%d %H:%M')) # Converter a coluna 'Time' para o formato de data e hora adequado
    df = df.sort_values(by='Time') # Ordenar o DataFrame pela coluna 'Time'
    df = df.sort_values(by='Time').reset_index(drop=True)
    df['Time'] = df['Time'].dt.strftime('%H:%M %d/%m/%Y')
    dia_um = df['Time'][0]
    dia_mes = dia_um.split(' ')[1]

    folder_path = '/caminho/'+ estacao

    # Lista de nomes dos arquivos de imagem
    image_files = ['2Temp.png', '3Umid.png', '4Pres.png', '5SO2 .png', 'Direção do Vento (°).png']

    # Altura do espaço em branco para o título
    title_height = 300

    # Abrir as imagens
    images = [Image.open(os.path.join(folder_path, filename)) for filename in image_files]

    # Obter as dimensões da primeira imagem
    width, height = images[2].size

    # Calcular a altura total da imagem composta (incluindo espaço em branco e imagens)
    composite_height = title_height + height * len(images)

    # Criar uma nova imagem composta com o tamanho adequado para todas as imagens e o espaço em branco
    composite_image = Image.new('RGB', (width, composite_height), color='white')

    # Colar cada imagem na posição correta na imagem composta (centralizada horizontalmente)
    for i, image in enumerate(images):
        # Calcular as coordenadas de colagem centralizadas
        paste_x = (width - image.width) // 2  # Centralizar horizontalmente
        paste_y = title_height + i * height

        composite_image.paste(image, (paste_x, paste_y))
    composite_image.show()
    # Salvar a imagem composta como um arquivo PNG
    composite_image.save('/caminho/'+ estacao+'/composite.png')

    # Carregar a imagem
    image = Image.open('/caminho/'+ estacao+'/composite.png')

    # Definir a dimensão da figura
    fig, ax = plt.subplots(figsize=(10, 16))

    # Plotar a imagem
    ax.imshow(image)

    # Obter as dimensões da primeira imagem
    width, height = image.size

    # Definir os textos dos títulos
    if estacao == "ESTACAO_VILA_MOEMA":
        title_text = 'Estação Vila Moema'
    elif estacao == "ESTACAO_CAPIVARI_DE_BAIXO":
        title_text = 'Estação Capivari'
    elif estacao == "ESTACAO_SAO_BERNARDO":
        title_text = 'Estação São Bernado'
    header_right_text = 'Previsão WRF/CHEM'
    header_left_text = 'Rodada:' + dia_mes

    # Adicionar os títulos
    ax.text(0.4 * width, 0.022 * height, title_text, color='black', fontsize=16)

    # Adicionar o quadrado em volta do texto do título
    rect = Rectangle((0.08 * width, 0.0055 * height), 0.9 * width, 0.02 * height,
                     fill=True, facecolor='white', edgecolor='black', alpha=0.5)
    ax.add_patch(rect)

    # Adicionar os cabeçalhos
    ax.text(0.08 * width, 0.0008 * height, header_right_text, color='black', fontsize=14)
    ax.text(0.78 * width, 0.0005 * height, header_left_text, color='black', fontsize=14)

    img = mpimg.imread('/caminho/LOGO.png')

    img_width = 73.14
    img_height = 55.4

    img_resized = resize(img, (img_height, img_width), anti_aliasing=True)

    fig_width, fig_height = fig.get_size_inches() * fig.dpi

    x = fig_width - img_width - 80
    y = fig_height - img_height - 40

    offset_img = offsetbox.OffsetImage(img_resized, zoom=1)
    image_box = offsetbox.AnnotationBbox(offset_img, (fig_width - x, fig_height - y), frameon=False)
    ax.add_artist(image_box)

    # Remover os eixos da imagem
    ax.axis('off')

    # Ajustar a posição da imagem para ocupar a figura inteira
    ax.set_position([0, 0, 1, 1])

    # Ajustar os limites dos eixos para coincidir com as dimensões da imagem
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)

    # Salvar a imagem com os títulos
    plt.savefig('/caminho/'+ estacao+'/meteograma_'+estacao+'.png', bbox_inches='tight', pad_inches=0)
plt.close()
# print('aaaaaaaaaaaaaaaaaa')
import os
import matplotlib.pyplot as plt

# Criar uma figura para a imagem composta
fig = plt.figure(figsize=(8, 6))

# Loop para cada estação
import numpy as np
from PIL import Image

# Tamanho do espaço em branco para o título (defina o valor desejado em pixels)
# Tamanho do espaço em branco para o título (defina o valor desejado em pixels)
title_height = 300

# Criar uma figura para o meteograma das imagens SO2
fig = plt.figure(figsize=(8, 6))

# Variável para rastrear se já foi adicionada a imagem em branco
added_blank_image = False

estacoes = ["ESTACAO_VILA_MOEMA", "ESTACAO_CAPIVARI_DE_BAIXO", "ESTACAO_SAO_BERNARDO"]

# Loop para cada estação
for i, estacao in enumerate(estacoes):
    folder_path = os.path.join('/caminho/', estacao)

    # Nome do arquivo da imagem 5SO2
    image_file = '6SO2 .png'

    # Caminho completo do arquivo da imagem 5SO2
    image_path = os.path.join(folder_path, image_file)

    # Carregar a imagem de SO2
    img = Image.open(image_path)

    # Criar uma nova figura para cada imagem de SO2
    fig = plt.figure(figsize=(8, 6))

    # Verificar se é a primeira iteração (ou seja, i é igual a 0)
    if i == 0:
        # Criar uma imagem em branco com o mesmo width que as imagens de SO2 e altura definida pelo title_height
        blank_image = Image.new('RGB', (img.width, title_height), color='white')

        # Adicionar a imagem em branco na primeira iteração
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(blank_image)
        ax.axis('off')

    # Adicionar um subplot para cada imagem de SO2 a partir da segunda iteração
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(img)
    ax.axis('off')

    # Ajustar o espaçamento entre subplots
    plt.tight_layout()

    # Mostrar a figura
    plt.show()


# Ajustar o espaçamento entre subplots
plt.tight_layout()

# Salvar a imagem composta
fig.savefig('/caminho/compositeSO2.png', dpi=300, bbox_inches='tight')


image = Image.open('/caminho/compositeSO2.png')

# Definir a dimensão da figura
fig, ax = plt.subplots(figsize=(10, 16))

# Plotar a imagem
ax.imshow(image)

# Obter as dimensões da primeira imagem
width, height = image.size

header_right_text = 'Previsão WRF/CHEM'
header_left_text = 'Rodada:' + dia_mes
title_text = 'Concentração de SO2'


# Adicionar os títulos
ax.text(0.4 * width, 0.04 * height, title_text, color='black', fontsize=14)

# Adicionar o quadrado em volta do texto do título
rect = Rectangle((0.11 * width, 0.01 * height), 0.83 * width, 0.035 * height,
                fill=True, facecolor='white', edgecolor='black', alpha=0.5)
ax.add_patch(rect)

# Adicionar os cabeçalhos
ax.text(0.11 * width, 0.00008 * height, header_right_text, color='black', fontsize=10)
ax.text(0.80 * width, 0.0005 * height, header_left_text, color='black', fontsize=10)

img = mpimg.imread('/caminho/LOGO.png')

img_width = 60
img_height = 45.4

img_resized = resize(img, (img_height, img_width), anti_aliasing=True)

fig_width, fig_height = fig.get_size_inches() * fig.dpi

x = fig_width - img_width - 30
y = fig_height - img_height

offset_img = offsetbox.OffsetImage(img_resized, zoom=1)
image_box = offsetbox.AnnotationBbox(offset_img, (fig_width - x, fig_height - y), frameon=False)
ax.add_artist(image_box)

# Remover os eixos da imagem
ax.axis('off')

# Ajustar a posição da imagem para ocupar a figura inteira
ax.set_position([0, 0, 1, 1])

# Ajustar os limites dos eixos para coincidir com as dimensões da imagem
ax.set_xlim(0, width)
ax.set_ylim(height, 0)

# Salvar a imagem com os títulos
plt.savefig('/caminho/'+ estacao+'/meteogramaSO2_'+estacao+'.png', bbox_inches='tight', pad_inches=0)

# Ajustar o espaçamento entre subplots
plt.tight_layout()
