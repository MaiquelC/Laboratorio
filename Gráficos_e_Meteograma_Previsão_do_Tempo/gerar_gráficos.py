import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg
from matplotlib import patches
import calendar
import math
import locale
from pylab import arange
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import AutoLocator
from datetime import datetime

def obter_mes_extenso(data):
    meses_abreviados = [
        'JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN',
        'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'
    ]
    dia, mes, _ = data.split('/')
    mes_numero = int(mes)
    mes_abreviado = meses_abreviados[mes_numero - 1]
    return f"{dia} {mes_abreviado}"

def plot_graph(time, data, tipo, cte, estacao):

    if cte == 1 or cte == 2 or cte == 3:
      return

    # Definindo a cor do gráfico que será plotado
    valor_normalizado = contador / 49
    cores = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'purple', 'orange', 'teal', 'pink']
    cmap = mcolors.LinearSegmentedColormap.from_list('CustomMap', cores)
    cor = cmap(valor_normalizado)

    # Criação do gráfico em barras para a chuva
    if data == 'Intensidade)':
       primeiro_valor = df[time].iloc[0]
       ultimo_valor = df[time].iloc[-1]
       fig, ax = plt.subplots(figsize=(8,2))
       if tipo == 1:
          ax.bar(df[time], df[data])

    # Criação gráfico específico para a direção do vento
    elif data == 'Direção do Vento (°)':
        df['Direção do Vento (°)'] = df['Direção do Vento (°)'].astype(float)
        velocidade = df['Velocidade do Vento (m/s)']
        y = [np.nan] + [0] * (len(df) - 1)  # altura constante com valor NaN no início
        # criando listas que serão usadas em seguida
        x_labels = []
        x_positions = []
        x_labels_extenso = []
        # plotando no gráfico apenas tempos em 00h de cada dia e substituindo esse valor pelo nome por extenso do dia
        for i, time in enumerate(df['Time']):
              # Verifique se a hora é igual a '00' (formato HH:MM)
              if time.split(" ")[0].endswith('00:00'):
                  # Adicione o valor ao formato desejado na lista de rótulos personalizados
                  print(time.split(" ")[1])
                  x_labels.append((i, obter_mes_extenso(time.split(" ")[1])))
              else:
                  # Adicione a posição no eixo x à lista de posições para desenhar as linhas verticais
                  x_positions.append(i)
        x = df['Time']  # valores de x
        direcao = df['Direção do Vento (°)']  # graus

        # Criação do gráfico
        fig, ax = plt.subplots()
        ax.plot(x, df['Velocidade do Vento (m/s)'], linewidth = 1)

        # Criando e plotando as felchas da direção do vento
        for i, (xi, di, vei) in enumerate(zip(x, direcao, velocidade)):
            ui = vei * np.sin(np.radians(di)) # Cálculo das componentes u e v da direção do vento (seguindo que Norte em 90°)
            vi = vei * np.cos(np.radians(di))
            ax.quiver(xi, media_velocidade, ui, vi, angles='uv', scale_units='xy', scale=2, width = 0.0019, headwidth=7, alpha = 0.8)

        # Configurações do gráfico.
        locator = MaxNLocator(nbins=30)
        ax.xaxis.set_major_locator(locator)
        ax.set_ylabel('Velocidade do Vento (m/s)')
        primeiro_valor = df['Time'].iloc[0]
        ultimo_valor = df['Time'].iloc[-1]
        ax.set_xlim(primeiro_valor, ultimo_valor)

        # Plotar as linhas verticais no gráfico para as demais horas que não são 00h
        for pos in x_positions:
            plt.axvline(x=pos, color='gray', linestyle=':', linewidth=0.5)

        # Obter os índices de cada valor de 00h e os novos valores, nomes do dia por extenso
        x_indices, x_values = zip(*x_labels)

        # Configurar os rótulos do eixo x usando os índices e valores salvos
        plt.xticks(x_indices, x_values)
        ax.set_ylim(0, media_velocidade + media_velocidade*2)
        ax.grid(True, linestyle='dotted', linewidth=0.5, color='gray')
        #plt.xticks(rotation=270)
        fig = plt.gcf()
        fig.set_size_inches(8,2) # Define o tamanho da figura em polegadas
        ax.set_title('Direção do Vento (°)')
        plt.savefig("/content/drive/MyDrive/CTJL/wrfout_previsao_teste/Graficos/"+estacao+"/" +data+".png", dpi=1000, bbox_inches='tight')
        plt.show()
        return

    # Criação do gráfico "normal", que se aplicam aos demais casos.
    else:
       if tipo == 1:

            # Crie uma lista vazia para armazenar os rótulos personalizados
            x_labels = []
            x_positions = []

            # Itere sobre os valores da coluna 'Time'
            for i, time in enumerate(df['Time']):
                # Verifique se a hora é igual a '00' (formato HH:MM)
                if time.split()[0].endswith('00:00'):
                    # Adicione o valor ao formato desejado na lista de rótulos personalizados
                    x_labels.append((i, obter_mes_extenso(time.split()[1])))
                else:
                    # Adicione a posição no eixo x à lista de posições para desenhar as linhas verticais
                    x_positions.append(i)

            if data == "Intensidade de Chuva (mm/h)":
                fig, ax1 = plt.subplots(figsize=(8, 2))
                # Plotar o gráfico de barras (Intensidade de Chuva)
                ax1.bar(df['Time'], df[data], color=cor, label='Intensidade de Chuva')
                ax1.set_ylabel('Intensidade de Chuva (mm/h)', color=cor)
                ax1.tick_params(axis='y', labelcolor=cor)

                # Criar um segundo eixo y compartilhando o mesmo eixo x
                ax2 = ax1.twinx()

                # Plotar o gráfico de linhas (Chuva Acumulada)
                ax2.plot(df['Time'], df['Chuva Acumulada (mm)'], color='blue', label='Chuva Acumulada')
                ax2.set_ylabel('Chuva Acumulada (mm)', color='blue')
                ax2.tick_params(axis='y', labelcolor='blue')

                # Mostrar as legendas
                ax1.legend(loc='upper left', fontsize='small')
                ax2.legend(loc='upper right', fontsize='small')

                primeiro_valor = df['Time'].iloc[0]
                ultimo_valor = df['Time'].iloc[-1]
                ax1.grid(True, linestyle='dashed', linewidth=0.5, color='gray')
                for pos in x_positions:
                    plt.axvline(x=pos, color='gray', linestyle=':', linewidth=0.5)

                # Definir os rótulos personalizados no eixo x
                x_indices, x_values = zip(*x_labels)
                plt.xticks(x_indices, x_values, rotation=90)

                # Definir o rótulo do eixo y principal
                ax1.set_ylabel(data)
                ax1.set_title('Precipitação', pad=10)
                return
            else:
                fig, ax = plt.subplots(figsize=(8, 2))
                ax.plot(df["Time"], df[data], color=cor)
            primeiro_valor = df["Time"].iloc[0]
            ultimo_valor = df["Time"].iloc[-1]
            ax.grid(True, linestyle='dashed', linewidth=0.5, color='gray')

    # Ajustar o espaçamento entre os subplots
    plt.subplots_adjust(top=0.85)

    # Definindo valores máximos e mínimos para os valores do eixo y.
    if data == "Umidade Relativa (%RH)":
        ax.set_ylim(20, 100)
    elif data == "Pressão do Ar (hPa)":
        ax.set_ylim(990, 1030)

    if data == 'SO2 (ppm)' or data == 'Velocidade do Vento (m/s)' or data == 'PM10 (µg/m³)' or data == 'PM2.5 (µg/m³)' or data == 'O3 (µg/m³)' or data == 'NO2 1h (µg/m³)' or data == 'NO2 (µg/m³)' or data == 'NO2 (µg/m³)' or data == 'NO (µg/m³)' or data == 'CO (µg/m³)':
        ax.set_ylim(0)
    ax.set_xlim(primeiro_valor, ultimo_valor)
    # Plotar as linhas verticais
    for pos in x_positions:
        plt.axvline(x=pos, color='gray', linestyle=':', linewidth=0.5)

    ax.set_title(data, pad=10)
    ax.set_ylabel(data)
    x_indices, x_values = zip(*x_labels)

    # Configurar os rótulos do eixo x usando os índices e valores salvos
    plt.xticks(x_indices, x_values)
    ax.yaxis.set_major_locator(MaxNLocator(5))

    # Salvar imagem do gráfico na pasta específica.
    data = data[:4]
    nomeador = str(contador)
    plt.savefig("/content/drive/MyDrive/CTJL/wrfout_previsao_teste/Graficos/"+estacao+"/" + nomeador + data + ".png", dpi=1000, bbox_inches='tight')

estacoes = ["ESTACAO_VILA_MOEMA", "ESTACAO_CAPIVARI_DE_BAIXO", "ESTACAO_SAO_BERNARDO"]
for estacao in estacoes:
        df = pd.read_csv('/content/drive/MyDrive/CTJL/wrfout_previsao_teste/'+estacao+'.csv', names=[
                    'Time',
                    'Velocidade do Vento (m/s)',
                    'Direção do Vento (°)',
                    'Temperatura a 2m (°C)',
                    'Umidade Relativa (%RH)',
                    'Pressão ao Nível do Mar (hPa)',
                    'SO2 (µg/m³)',
                    'Chuva Acumulada (mm)'])

        has_hour = df['Time'].str.contains(':')
        null_indices = np.where(~has_hour)[0]
        df = df.reset_index()
        df.loc[null_indices, 'Time'] = df.loc[null_indices, 'Time'] + " 00:00:00"
        df['Time'] = df['Time'].apply(lambda x: pd.to_datetime(str(x)[:16].replace('/', '-'), format='%Y-%m-%d %H:%M')) # Converter a coluna 'Time' para o formato de data e hora adequado
        df = df.sort_values(by='Time') # Ordenar o DataFrame pela coluna 'Time'
        df = df.sort_values(by='Time').reset_index(drop=True)
        df['Time'] = df['Time'].dt.strftime('%H:%M %d/%m/%Y')
        df['Pressão ao Nível do Mar (hPa)'] = df['Pressão ao Nível do Mar (hPa)'].drop_duplicates().iloc[1:]
        df['Intensidade de Chuva (mm/h)'] = df['Chuva Acumulada (mm)'].diff().fillna(value=0)
        for column in df.columns[3:-1]:
            df[column] = df[column].fillna(method='ffill')

        dia_um = df['Time'][0]
        dia_um_split = dia_um.split(' ')[1].split('/')
        dia_mes = '/'.join(dia_um_split[:2])

        valor_inicial = '00:00 30/06/2023' #input("Digite a data inicial do gráfico (no formato H:M d/m/Y): ")
        valor_final = '00:00 03/07/2023' #input("Digite a data final do gráfico (no formato H:M d/m/Y): ")

        # Reecriando o dataframe, agora apenas com as linhas final e inicial da coluna Time estabelecidos pelo usuário.
        linha_inicial = int((df['Time'] == valor_inicial).idxmax()) # encontra o número da linha que contém o mesmo valor que o usuário quer
        linha_final = int((df['Time'] == valor_final).idxmax()) + 1
        df = df.iloc[linha_inicial:linha_final, :]

        num_linhas = len(df['Time']) # número total de linhas da coluna time
        contador = 0 # contador que será usado para nomear os arquivos
        cte_ar_ingeraveis = 0
        media_velocidade = df['Velocidade do Vento (m/s)'].mean()
        num_nbins = 24

        # Loop que irá chamar a função para criar os gráficos de cada uma das colunas pela coluna do tempo.
        for i in range(1, len(df.columns)-1):
            data = df.columns[i+1]
            valor_maximo = 0
            contador = contador + 1

            valor_p1, valor_p2, valor_p3, valor_nf = parametros.get(data, (0, 0, 0, 0))
            if data in ['CO 8h (ppm)', 'O3 8h (µg/m³)']:
                plot_graph('Time', data, 3, cte_ar_ingeraveis, estacao)
            elif data in ['PM10 24h (µg/m³)', 'PM2.5 24h (µg/m³)']:
                mes = ddia.split('/')[1]
                ano = ddia.split('/')[2][:4]
                plot_graph('Time', data, 2, cte_ar_ingeraveis, estacao)
            else:
                plot_graph('Time', data, 1, cte_ar_ingeraveis, estacao)
