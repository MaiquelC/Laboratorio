# Função que converte dados em micrograma para partícula por milhão.
def ugm3_to_ppm(carbone):
    carbone_ppb = 1.88 * carbone
    carbone_ppm = 1000 * carbone_ppb
    return carbone_ppm

# Função para filtrar os dados do dataframe
def filtragem():
    for i in range(1, len(df.columns)-1):
        data = df.columns[i+1]
        df[data] = np.where(df[data] < 0, np.nan, df[data])
    alerta = 0
    for data in df.columns:
       if data == 'Temperatura do Ar (°C)' or data == 'PM10 (µg/m³)' or data == 'PM2.5 (µg/m³)' or data == 'O3 (µg/m³)' or data == 'NO2 1h (µg/m³)' or data == 'NO2 (µg/m³)' or data == 'NO2 (µg/m³)' or data == 'NO (µg/m³)' or data == 'CO (µg/m³)':
          for i in range(1, len(df)-1):
             valor_atual = df.loc[i, data]
             valor_anterior = df.loc[i-1, data]
             valor_posterior = df.loc[i+1, data]

             if (valor_atual > (3 * valor_anterior)) and (valor_atual > (3 * valor_posterior) and not np.isnan(valor_anterior) and not np.isnan(valor_posterior)):

                 df.loc[i, data] = np.nan
                 if data == 'CO (µg/m³)':
                          alerta = 1
    # se houver erro
    if alerta == 1:
       for data in df.columns:
          if data == 'Temperatura do Ar (°C)':
             for i in range(1, len(df)-1):
                valor_atual = df.loc[i, data]
                valor_anterior = df.loc[i-1, data]
                if valor_atual > 5 + valor_anterior or valor_atual < (valor_anterior - 5):
                   df.loc[i, data] = df.loc[i, '2'] # pega a temperatura do aqt
          if data == 'Pressão do Ar (hPa)':
             for i in range(1, len(df)-1):
                valor_atual = df.loc[i, data]
                valor_anterior = df.loc[i-1, data]
                if valor_atual > 5 + valor_anterior or valor_atual < (valor_anterior - 5):
                   df.loc[i, data] = np.nan
          if data == 'O3 (µg/m³)' or data == 'CO (µg/m³)' or data == 'NO2 (µg/m³)' or data == 'NO (µg/m³)':
             for i in range(1, len(df)-1):
                valor_atual = df.loc[i, data]
                valor_anterior = df.loc[i-1, data]
                valor_posterior = df.loc[i+1, data]
             if valor_atual > (valor_anterior * 3) or valor_atual > (valor_posterior * 3):
                df.loc[i, data] = np.nan
                i = i + 1
    return  

# Função que cria o gráfico específico para cada umas das colunas pelo tempo
def plot_graph(time, data, tipo, cte):

    if cte == 1 or cte == 2 or cte == 3:
      return

    # Definindo a cor do gráfico que será plotado
    valor_normalizado = contador / 25
    cores = ['red', 'red','green', 'blue', 'green', 'blue', 'green', 'orange', 'yellow', 'blue', 'teal', 'green', 'red', 'yellow', 'orange']
    cmap = mcolors.LinearSegmentedColormap.from_list('CustomMap', cores)
    cor = cmap(valor_normalizado)

    # Criação do gráfico em barras para a chuva.
    if data == 'Intensidade de Chuva (mm/h)':
       primeiro_valor = df[time].iloc[0]
       ultimo_valor = df[time].iloc[-1]
       fig, ax = plt.subplots(figsize=(7, 6))
       if tipo == 1:
          ax.bar(df[time], df[data], color=cor)
          x_positions = []
          x_labels = []

          # Iterar sobre os valores da coluna 'Time'
          for i, time in enumerate(df['Time']):
              # Verificar se a hora é igual a '00' (formato HH:MM)
              if time.split()[0].endswith('00:00'):
                  # Adicionar a posição no eixo x à lista de posições para desenhar as linhas verticais
                  x_positions.append(i)
                  # Adicionar o rótulo do mês na lista de rótulos personalizados
                  segunda_parte = time.split()[1]
                  partes2 = segunda_parte.split('/')  # Divide a segunda parte usando o caractere de barra
                  x_labels.append('/'.join(partes2[:2]))  # Adicione o mês à lista de rótulos personalizados

          # Adicionar as linhas verticais no gráfico
          for pos in x_positions:
              ax.axvline(pos, color='gray', linestyle='dashed', linewidth=0.5)

          # Definir as posições e rótulos dos meses no eixo x
          ax.set_xticks(x_positions)
          ax.set_xticklabels(x_labels, rotation=90)

    # Criação gráfico específico para a direção do vento.
    elif data == 'Direção do Vento (°)':
        #arrumar isso aqui
        df['Direção do Vento (°)'] = df['Direção do Vento (°)'].astype(float)
        velocidade = df['Velocidade do Vento (m/s)'] 
        y = [np.nan] + [0] * (len(df) - 1)  # altura constante com valor NaN no início
        x = df['Time']  # valores de x
        direcao = df['Direção do Vento (°)']  # graus

        # Criação do gráfico
        fig, ax = plt.subplots()
        ax.plot(x, df['Velocidade do Vento (m/s)'], linewidth = 1, color=cor)  # y constante com valor NaN no início

        # Loop pelos valores de x e direção.
        for i, (xi, di, vei) in enumerate(zip(x, direcao, velocidade)):
            # Cálculo das componentes u e v da direção do vento
            ui = vei * np.sin(np.radians(di))
            vi = vei * np.cos(np.radians(di))
            ax.quiver(xi, media_velocidade, ui, vi, angles='uv', scale_units='xy', scale=2, width = 0.001, alpha = 0.8)

        # Configurações do gráfico.
        locator = MaxNLocator(nbins=30)
        ax.xaxis.set_major_locator(locator)
        primeiro_valor = df[time].iloc[0]
        ultimo_valor = df[time].iloc[-1]
        x_positions = []
        x_labels = []

        for i, time in enumerate(df['Time']):
              if time.split()[0].endswith('00:00'):
                  x_positions.append(i)
                  segunda_parte = time.split()[1]
                  partes2 = segunda_parte.split('/')  
                  x_labels.append('/'.join(partes2[:2]))

        for pos in x_positions:
              ax.axvline(pos, color='gray', linestyle='dashed', linewidth=0.5)

        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=90)
        ax.set_xlim(primeiro_valor, ultimo_valor)
        ax.set_ylim(0, media_velocidade + 7)
        ax.grid(True, linestyle='dotted', linewidth=0.5, color='gray')
        plt.xticks(rotation=270) 
        fig = plt.gcf()  
        fig.set_size_inches(16, 4)
        ax.set_title(data)
        fig.suptitle("Estação Rio Grande - Secretaria do Meio Ambiente", fontsize=12)
        plt.savefig("/caminho/" + data + ".png", dpi=1000, bbox_inches='tight')
        return

    # Criação do gráfico "normal", que se aplicam aos demais casos.
    else:
       if data == 'NO2 1h (µg/m³)':
          fig, ax = plt.subplots(figsize=(7, 6))
          primeiro_valor = df[time].iloc[0]
          ultimo_valor = df[time].iloc[-1]

          ax.bar(df["Time"], df[data], color=cor)
          x_positions = []
          x_labels = []

          for i, time in enumerate(df['Time']):
              if time.split()[0].endswith('00:00'):
                  x_positions.append(i)
                  segunda_parte = time.split()[1]
                  partes2 = segunda_parte.split('/') 
                  x_labels.append('/'.join(partes2[:2]))

          for pos in x_positions:
              ax.axvline(pos, color='gray', linestyle='dashed', linewidth=0.5)

          ax.set_xticks(x_positions)
          ax.set_xticklabels(x_labels, rotation=90)

       elif tipo == 1:
          fig, ax = plt.subplots(figsize=(7, 6))
          primeiro_valor = df[time].iloc[0]
          ultimo_valor = df[time].iloc[-1]
          ax.plot(df["Time"], df[data], color=cor)
          x_positions = []
          x_labels = []

          for i, time in enumerate(df['Time']):
              if time.split()[0].endswith('00:00'):
                  x_positions.append(i)
                  segunda_parte = time.split()[1]
                  partes2 = segunda_parte.split('/')  
                  x_labels.append('/'.join(partes2[:2])) 

          for pos in x_positions:
              ax.axvline(pos, color='gray', linestyle='dashed', linewidth=0.5)

          ax.grid(True, linestyle='dotted', linewidth=0.5, color='gray')
          ax.set_xticks(x_positions)
          ax.set_xticklabels(x_labels, rotation=90)


       elif tipo == 2:
          ddia = df2['Time'].iloc[0]
          mes = 6
          ano = int(ddia.split('/')[2][:4])

          _, num_dias = calendar.monthrange(ano, mes)
          primeiro_dia_semana, _ = calendar.monthrange(ano, mes)
          num_semanas = math.ceil((num_dias + primeiro_dia_semana) / 7)
          calendario = pd.DataFrame(index=range(1, num_semanas + 1), columns=range(7))

          primeiro_indice = df2[data].idxmin()
          dados = df2[data]
          contador_dias = 0
          for i in range(num_semanas):
                for j in range(7):
                    if i == 0 and j < primeiro_dia_semana:
                        calendario.iloc[i, j] = np.nan
                    else:
                        if contador_dias < num_dias*24:
                              calendario.iloc[i, j] = float(dados[contador_dias])
                              contador_dias += 24

          dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
          calendario = calendario.astype(float) 
          fig, ax = plt.subplots(figsize=(7, 6))

          # Definir cores e plotar o heatmap
          if data == 'Chuva Acumulada (mm)':
            cmap = sns.cubehelix_palette(start=0.5, rot=-0.5, as_cmap=True) # Definindo a paleta de cores
            sns.heatmap(calendario, cmap=cmap, linewidths=0.5, annot=True, fmt=".2f", cbar=False) # Plotando o heatmap
          elif data == 'PM2.5 24h (µg/m³)':
            cmap = sns.cubehelix_palette(start=2, rot=-0.9, as_cmap=True)
            sns.heatmap(calendario, cmap=cmap, linewidths=0.5, annot=True, fmt=".2f", cbar=False)
          elif data == 'PM10 24h (µg/m³)':
              cmap = sns.color_palette("icefire", as_cmap=True) 
              sns.heatmap(calendario, cmap=cmap, linewidths=0.5, annot=True, fmt=".2f", cbar=False) 

          # Adicionar linhas entres os dias no calendário
          for i in range(0, num_semanas + 1):
              if i == num_semanas:
                  ax.hlines(i, xmin=0, xmax=7, colors='black', linewidth=2)  # Linhas horizontais mais grossas
              else:
                  ax.hlines(i, xmin=0, xmax=7, colors='black', linewidth=0.5)  # Linhas horizontais
          for j in range(0, 8):
              if j == 7:
                  ax.vlines(j, ymin=0, ymax=num_semanas+0.5, colors='black', linewidth=2)  # Linhas verticais mais grossas , pois elas não aparecem normalmente
              else:
                  ax.vlines(j, ymin=0, ymax=num_semanas+0.5, colors='black', linewidth=0.5)  # Linhas verticais

          # Adicionar o número do dia no canto superior direito de cada bloco de dados
          for i in range(num_semanas):
              for j in range(7):
                  dia = i * 7 + j + 1 - primeiro_dia_semana
                  if dia >= 1 and dia <= num_dias:
                      ax.text(j + 0.9, i + 0.1, str(dia), color='black', ha='center', va='center', fontsize=8)

          # Adicionar a barra de cores
          cax = fig.add_axes([0.95, 0.15, 0.04, 0.7])  # Posição e tamanho da barra de cores
          cb = plt.colorbar(ax.collections[0], cax=cax)  # Adicionar a barra de cores ao gráfico

          # Configurar os rótulos da barra de cores
          cb.set_label(data) 
          if data == 'Chuva Acumulada (mm)':
              cb.mappable.set_clim(vmin=0, vmax=50)# Adicionar linhas representando valores na barra de cores
          elif data == 'PM2.5 24h (µg/m³)':
                      valores_linhas = [valor_p1, valor_p2, valor_p3, valor_nf]  # Valores para adicionar linhas
                      text = ['P1', 'P2', 'P3', 'PF']
                      cb.mappable.set_clim(vmin=0, vmax=65)# Adicionar linhas representando valores na barra de cores
                      for valor, texto in zip(valores_linhas, text):
                            cb.ax.axhline(valor, color='white', linestyle='--', linewidth=0.8)
                            cb.ax.text(0.5, valor + 2, str(valor), color='white', ha='center', va='center')
                            cb.ax.text(-0.5, valor, texto, color='black', ha='center', va='center')
          elif data == 'PM10 24h (µg/m³)':
                      valores_linhas = [valor_p1, valor_p2, valor_p3, valor_nf]
                      text = ['P1', 'P2', 'P3', 'PF']
                      cb.mappable.set_clim(vmin=0, vmax=130)
                      for valor, texto in zip(valores_linhas, text):
                            cb.ax.axhline(valor, color='white', linestyle='--', linewidth=0.8)
                            cb.ax.text(0.5, valor + 3, str(valor), color='white', ha='center', va='center')
                            cb.ax.text(-0.5, valor, texto, color='black', ha='center', va='center')

          meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

          ax.set_xticklabels(dias_semana)
          ax.yaxis.set_ticks_position('none')
          ax.set_yticklabels(["".format(i) for i in range(1, num_semanas + 1)])
          ax.set_title(f'{meses[mes]} {ano}'+" - "+data)   # Atualizar o título com o mês correto
          fig.suptitle("Estação Rio Grande - Secretaria do Meio Ambiente", fontsize=12)
          nomeador = str(contador+3)
          data = data[:4]
          plt.savefig("/caminho/" + nomeador + data + ".png", dpi=1000, bbox_inches='tight')
          plt.show()
          return

       elif tipo == 3:
          fig, ax = plt.subplots(figsize=(7, 6))
          primeiro_valor = df3[time].iloc[0]
          ultimo_valor = df3[time].iloc[-1]
          ax.bar(df3["Time"], df3[data], color=cor)
          x_positions = []
          x_labels = []

          for i, time in enumerate(df3['Time']):
              if time.split()[0].endswith('00:00'):
                  x_positions.append(i)
                  segunda_parte = time.split()[1]
                  partes2 = segunda_parte.split('/') 
                  x_labels.append('/'.join(partes2[:2]))

          for pos in x_positions:
              ax.axvline(pos, color='gray', linestyle='dashed', linewidth=0.5)

          ax.set_xticks(x_positions)
          ax.set_xticklabels(x_labels, rotation=90)

    ax.set_ylabel(data)
    ax.set_title(data, pad=10)
    fig.suptitle("Estação Rio Grande - Secretaria do Meio Ambiente", fontsize=12, y=0.91, va='baseline', ha='center') 
    plt.subplots_adjust(top=0.85)

    # Definindo valores máximos e mínimos para os valores do eixo y.
    if data == "Umidade Relativa (%RH)":
        ax.set_ylim(20, 100)

    # Determinando o valor máximo da lista data, o qual será utilizado em seguida.
    if tipo == 1:
        valor_maximo = df[data].max()
    elif tipo == 2:
        valor_maximo = df2[data].max()
    elif tipo == 3:
        valor_maximo = df3[data].max()

    # Desenhar a linha horizontal constante em y, para os valores dos Padrões de Qualidade do Ar Intermediários (PI).
    if valor_p1 != 0 and valor_p1 <= 10*valor_maximo: #Se o valor do PI-1 for 10x maior que o maior valor da lista data, não serão mostrados.
        plt.axhline(y=valor_p1, color='r', linewidth=0.8, linestyle='dashed')
        plt.annotate('P1'.format(valor_p1), xy=(0.05, valor_p1 + 0.5))
        if data != 'CO 8h (ppm)':
          plt.axhline(y=valor_p2, color='y', linewidth=0.8, linestyle='dashed')
          plt.annotate('P2'.format(valor_p2), xy=(0.05, valor_p2 + 0.5))
          plt.axhline(y=valor_p3, color='b', linewidth=0.8, linestyle='dashed')
          plt.annotate('P3'.format(valor_p3), xy=(0.05, valor_p3 + 0.5))
          plt.axhline(y=valor_nf, color='g', linewidth=0.8, linestyle='dashed')
          plt.annotate('NF'.format(valor_nf), xy=(0.05, valor_nf + 0.5))
        
    # Defini
    if data == 'Velocidade do Vento (m/s)' or data == 'PM10 (µg/m³)' or data == 'PM2.5 (µg/m³)' or data == 'O3 (µg/m³)' or data == 'NO2 1h (µg/m³)' or data == 'NO2 (µg/m³)' or data == 'NO2 (µg/m³)' or data == 'NO (µg/m³)' or data == 'CO (µg/m³)':
        ax.set_ylim(0)

    plt.xticks(rotation=270) # Gira os valores visuais do eixo x em 90 graus

    # Salvar imagem do gráfico na pasta específica.
    data = data[:4]
    nomeador = str(contador)
    plt.savefig("/caminho/" + nomeador + data + ".png", dpi=1000, bbox_inches='tight')


# }

# Criando o dataframe que vem da tabela com os dados vindo diretos do vaisala de 1h em 1h.
df = pd.read_csv('/caminho/nome_arquivo.csv', skiprows=5, names=[
                                                   'Time',
                                                   '1',
                                                   '2',
                                                   'Temperatura do Ar (°C)',
                                                   '3',
                                                   'Umidade Relativa (%RH)',
                                                   'Pressão do Ar (hPa)',
                                                   '4',
                                                   'Velocidade do Vento (m/s)',
                                                   'Velocidade do Vento Máxima (m/s)',
                                                   'Direção do Vento (°)',
                                                   'Intensidade de Chuva (mm/h)',
                                                   'Chuva Acumulada (mm)',
                                                   'CO (µg/m³)',
                                                   'CO 8h (ppm)',
                                                   '6',
                                                   'NO (µg/m³)',
                                                   'NO2 (µg/m³)',
                                                   'NO2 1h (µg/m³)',
                                                   '7',
                                                   'O3 (µg/m³)',
                                                   'O3 8h (µg/m³)',
                                                   '8',
                                                   '9',
                                                   '10',
                                                   '11',
                                                   'PM2.5 (µg/m³)',
                                                   'PM2.5 24h (µg/m³)',
                                                   '12',
                                                   'PM10 (µg/m³)',
                                                   'PM10 24h (µg/m³)',
                                                   '13'])


# Filtragem dos dados
sim = 1
if sim == 1:
  filtragem()


df['Time'] = pd.to_datetime(df['Time'].str[:16].str.replace('/', '-'), format='%Y-%m-%d %H:%M')
df = df.sort_values(by='Time').reset_index(drop=True)

# Verificar se existem valores de horários faltando e acrescentar esses valores
diff = df['Time'].diff()
linhas_faltantes = df[diff > pd.Timedelta(hours=1)]
new_rows = []
for i, row in linhas_faltantes.iterrows():
    time_diff = row['Time'] - df.loc[i - 1, 'Time']
    num_intervals = int(time_diff.total_seconds() / 3600) - 1

    print("Linha atual:", row)
    print("Diferença de tempo:", time_diff)
    print("Número de intervalos:", num_intervals)

    for j in range(1, num_intervals + 1):
        new_time = df.loc[i - 1, 'Time'] + pd.Timedelta(hours=j)
        new_row = {'Time': new_time}
        new_rows.append(new_row)
        print("Nova linha adicionada:", new_row)

if len(new_rows) > 0:
    new_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df = new_df.sort_values(by='Time').reset_index(drop=True)
else:
    df = df.reset_index(drop=True)

# Converter a coluna 'Time' de volta para o formato desejado
df['Time'] = df['Time'].dt.strftime('%H:%M %d/%m/%Y')

# Pedindo data incial e final para o usário, além de quantos valores ele deseja no fim.
valor_inicial = '00:00 01/06/2023' #input("Digite a data inicial do gráfico (no formato H:M d/m/Y): ")
valor_final = '23:00 30/06/2023' #input("Digite a data final do gráfico (no formato H:M d/m/Y): ")

# Reecriando o dataframe, agora apenas com as linhas final e inicial da coluna Time estabelecidos pelo usuário.
linha_inicial = int((df['Time'] == valor_inicial).idxmax()) 
linha_final = int((df['Time'] == valor_final).idxmax()) + 1
df = df.iloc[linha_inicial:linha_final, :]
df = df.reset_index(drop=True)

# Definindo algumas variavéis que serão utilizadas em sequência.
num_linhas = len(df['Time']) # número total de linhas da coluna time
modulo_dia = num_linhas % 24 # quantos dias o período informado possui
modulo_oitohoras = num_linhas % 8 # quantos períodos de 8 horas o período informado possui
contador = 0 # contador que será usado para nomear os arquivos
cte_ar_ingeraveis = 0
media_velocidade = df['Velocidade do Vento (m/s)'].mean()
print(df)

# Aqui serão calculadas as médias de 24 horas e 8 horas, pois os dados do Vaisala não faz a médiade com conjuntos de períodos inteiros, ele faz com base nas últimas 24/8 horas anteriores daquela hora.
if modulo_dia == 0 or modulo_oitohoras == 0: # Repare que é um OR
    if modulo_dia == 0:
        # primeiro vamos criar a coluna com as médias diárias do Material Particulado (PM), pq o limite estabelecido pelo Ministério do Meio Ambiente utiliza a média
        num_dias = num_linhas // 24
        # se o número de dias for maior que 3, a chuva acumulada e a intesidade de chuva passam a ser a média das 24h e não mais de 1h
        for i in range(num_dias):
            linha_inicial = i * 24
            linha_final = (i + 1) * 24

            coluna_PM25 = df.columns.get_loc('PM2.5 (µg/m³)')
            coluna_PM25_24h = df.columns.get_loc('PM2.5 24h (µg/m³)')
            media_horaria = df.iloc[linha_inicial:linha_final, coluna_PM25].mean()
            df.iloc[linha_inicial:linha_final, coluna_PM25_24h] = media_horaria

            coluna_PM10 = df.columns.get_loc('PM10 (µg/m³)')
            coluna_PM10_24h = df.columns.get_loc('PM10 24h (µg/m³)')
            media_horaria = df.iloc[linha_inicial:linha_final, coluna_PM10].mean()
            df.iloc[linha_inicial:linha_final, coluna_PM10_24h] = media_horaria

        aviso_chuva_acumulada = 0
        if num_dias > 3:
            aviso_chuva_acumulada = 1
            for i in range(num_dias):
                linha_inicial = i * 24
                linha_final = (i + 1) * 24

                coluna_intensity = df.columns.get_loc('Intensidade de Chuva (mm/h)')
                coluna_accumulation = df.columns.get_loc('Chuva Acumulada (mm)')
                soma_horaria = df.iloc[linha_inicial:linha_final, coluna_intensity].sum()
                df.iloc[linha_inicial:linha_final, coluna_accumulation] = soma_horaria

        indices = list(range(0, len(df), 24))
        df2 = df.iloc[indices]
    else:
        cte_ar_ingeraveis = 1
        df2 = df
        print(modulo_dia)
        print("A quantidade de horas não é múltipla de 24, ou seja, não podemos gerar gráficos de PM2.5 e PM10 para comparar com as constantes")

    if modulo_oitohoras == 0:
        num_dias = int(num_linhas // 24)
        num_oitohoras = num_linhas // 8
        for i in range(num_oitohoras):
            linha_inicial = i * 8
            linha_final = (i + 1) * 8

            coluna_O3 = df.columns.get_loc('O3 (µg/m³)')
            coluna_O3_8h = df.columns.get_loc('O3 8h (µg/m³)')
            media_horaria = df.iloc[linha_inicial:linha_final, coluna_O3].mean()
            df.iloc[linha_inicial:linha_final, coluna_O3_8h] = media_horaria

            coluna_CO = df.columns.get_loc('CO (µg/m³)')
            coluna_CO_8h = df.columns.get_loc('CO 8h (ppm)')
            media_horaria = df.iloc[linha_inicial:linha_final, coluna_CO].mean()
            df.iloc[linha_inicial:linha_final, coluna_CO_8h] = media_horaria

        indices = list(range(0, len(df), 8))
        df3 = df.iloc[indices]
        df3.loc[:, 'CO 8h (ppm)'] = df3.apply(lambda row: ugm3_to_ppm(row['CO 8h (ppm)']), axis=1)
    else:
        cte_ar_ingeraveis = 2
        df3 = df
        print(modulo_oitohoras)
        print("A quantidade de horas não é múltipla de 24 e nem de 8, ou seja, não podemos gerar gráficos de PM2.5, PM10, O3 e CO para comparar com as constantes limites")
else:
    cte_ar_ingeraveis = 3
    df2 = df
    df3 = df
    print(modulo_dia)
    print("Para gerar os gráficos de qualidade do ar acumulados é necessário que o valor total de horas seja um multiplo inteiro de 8 ou 24")


# Definindo os valores dos Padrões de Qualidade do Ar Intermediários e Finais de cada poluente, definidos pela Resoluçãõ n° 491-19/11/2018
parametros = {
    'CO 8h (ppm)': (0, 0, 0, 9),
    'NO2 1h (µg/m³)': (260, 240, 220, 200),
    'O3 8h (µg/m³)': (140, 130, 120, 110),
    'PM2.5 24h (µg/m³)': (60, 50, 37, 25),
    'PM10 24h (µg/m³)': (120, 100, 75, 50),
}
                                              
# Loop que irá chamar a função para criar os gráficos de cada uma das colunas pela coluna do tempo
for i in range(1, len(df.columns)-1):
    data = df.columns[i+1]
    valor_maximo = 0
    contador = contador + 1
    # Colunas presentes nessa lista, nomeadas por números, não serão utilizadas, por isso as "descartamos"
    if data not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:
        valor_p1, valor_p2, valor_p3, valor_nf = parametros.get(data, (0, 0, 0, 0))
        if data in ['CO 8h (ppm)', 'O3 8h (µg/m³)']:
            plot_graph('Time', data, 3, cte_ar_ingeraveis)
        elif data in ['Chuva Acumulada (mm)', 'PM10 24h (µg/m³)', 'PM2.5 24h (µg/m³)']:
            ddia = df2['Time'].iloc[0]
            mes = ddia.split('/')[1]
            ano = ddia.split('/')[2][:4]
            plot_graph('Time', data, 2, cte_ar_ingeraveis)
        else:
            plot_graph('Time', data, 1, cte_ar_ingeraveis)

# }
