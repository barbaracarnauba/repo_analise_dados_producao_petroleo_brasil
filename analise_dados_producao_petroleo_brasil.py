"""
Análise de Dados de Produção de Petróleo com Python
@author: Bárbara Cynthia Carnaúba dos Santos
contato: https://www.linkedin.com/in/barbaracarnauba/

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sea
from IPython import get_ipython

# Fonte dos dados carregados: Agência Nacional do Petróleo
# http://www.anp.gov.br/conteudo-do-menu-superior/31-dados-abertos/5538-producao-de-petroleo-e-gas-natural-nacional

# Para conferir os insights: http://www.anp.gov.br/dados-estatisticos
# : Produção nacional de petróleo e LGN (metros cúbicos))

get_ipython().magic('reset -sf') #Limpa workspace
plt.close('all') #fecha todos os gráficos

# Listando métodos e atributos das bibliotecas: Pandas, Numpy e Matplotlib.Pyplot
print(list(dir(pd)))
print(list(dir(np)))
print(list(dir(plt)))

# Lendo o arquivo csv e salvando-o em DataFrame

dfProd15_1S=pd.read_csv('producao-terra-2015-1sem.csv')
dfProd15_2S=pd.read_csv('producao-terra-2015-2sem.csv')
dfProd15 = pd.concat([dfProd15_1S,dfProd15_2S],ignore_index=True)

# Removendo duplicatas:

dfProd15.drop_duplicates()

# Análise exploratória dos Dados do DataFrame dfProd15

#Listando os nomes de todas as colunas
print(dfProd15.columns.to_list())

# Vamos trabalhar primeiraments apenas com os dados de produção de óleo
dfProd15=dfProd15[['Ano','Mês/Ano','Estado','Bacia','Campo','Poço','Ambiente',\
                   'Instalação', 'Produção de Óleo (m³)']]

#Listando tipos de dados de cada coluna: Object é uma string ou dado misto, 
# float64 é um número real

dfProd15.dtypes

#Procurando número de elementos faltantes no arquivo, elementos do tipo NaN

dfProd15.isna().sum() 

#Excluindo linhas com elementos faltantes

dfProd15.dropna(inplace=True)

# A representação decimal está com ",". Mudaremos para ".":
    
dfProd15['Produção de Óleo (m³)']=dfProd15['Produção de Óleo (m³)'].str.replace(',','.')


# A Coluna "Produção de Óleo (m³)" deveria ter dados do tipo float64, mas possui
# dados do tipo objet, logo, temos que transformá-los em float64
    
dfProd15['Produção de Óleo (m³)']=dfProd15['Produção de Óleo (m³)'].astype('float64')

# Listando Bacias e Campos presentes no DataSet

unique_bacias=pd.unique(dfProd15['Bacia']) 
unique_campos=pd.unique(dfProd15['Campo']) 

# Filtrando dados uma coluna

alagoas_prod2015=dfProd15[(dfProd15.Bacia == "Alagoas")] # & (dfProd15.Campo == "ANAMBÉ")
reconcavo_prod2015=dfProd15[(dfProd15.Bacia == "Recôncavo")] 
sergipe_prod2015=dfProd15[(dfProd15.Bacia == "Sergipe")] 
tucano_prod2015=dfProd15[(dfProd15.Bacia == "Tucano Sul")] 
barreirinha_prod2015=dfProd15[(dfProd15.Bacia == "Barreirinhas")] 

# Filtrando dados múltiplas colunas: Bacia, Campo e Mês/Ano

sergipe_carmopolis_dez=dfProd15[(dfProd15.Bacia == "Sergipe") & (dfProd15.Campo == \
                            "CARMÓPOLIS")  & (dfProd15['Mês/Ano']== \
                            "12/2015")]
                                              
# Localizando maiores e menores produtores
                                
dfProd15=dfProd15.replace(0.0,np.nan) #Trocando elementos nulos por NaN
dfProd15.dropna(inplace=True) # Retirando NaN do DataFrame

max_oil_linha=dfProd15.loc[dfProd15['Produção de Óleo (m³)'].idxmax()]
print(max_oil_linha)
dfProd15['Produção de Óleo (m³)'].max()
min_oil_linha=dfProd15.loc[dfProd15['Produção de Óleo (m³)'].idxmin()]
print(min_oil_linha)
dfProd15['Produção de Óleo (m³)'].min()


###----------------AGRUPANDO VARIÁVEIS E PLOTANDO RESULTADOS---------------###

df_cut=dfProd15[['Estado', 'Bacia', 'Campo','Produção de Óleo (m³)']]

soma_prod_estados=df_cut.groupby(['Estado'],as_index=False).sum()
print(soma_prod_estados)

soma_prod_campos=df_cut.groupby(['Campo','Estado'],as_index=False).sum()
soma_prod_campos_ordemCrescente=soma_prod_campos.sort_values(by=['Produção de Óleo (m³)'], ignore_index=True)
print(soma_prod_campos)
print(soma_prod_campos_ordemCrescente)

campos_10maioresProd=soma_prod_campos_ordemCrescente[212::]

campos_10menoresProd = soma_prod_campos_ordemCrescente[0:10]

# Gráficos de Barra com Seaborn e Matplotlib

plt.rcParams.update({'font.size': 14})

plt.figure(1)
ax=sea.barplot('Estado','Produção de Óleo (m³)', data=soma_prod_estados,palette="rocket",ci=None)\
    .set(title='Produção total de óleo por estado - 2015')
degrees = 45
plt.xticks(rotation=degrees)
plt.tight_layout()

plt.figure(2)
ax=sea.barplot('Campo','Produção de Óleo (m³)', data=campos_10maioresProd,palette="dark",ci=None)\
    .set(title='Os 10 maiores campos produtores - 2015')
degrees = 90
plt.xticks(rotation=degrees)
plt.tight_layout()

plt.figure(3)
ax=sea.barplot('Campo','Produção de Óleo (m³)', data=campos_10menoresProd,palette="deep",ci=None)\
    .set(title='Os 10 menores campos produtores - 2015')
degrees = 90
plt.xticks(rotation=degrees)
plt.tight_layout()

# Gráfico de Pizza com Pandas

soma_prod_estados['Produção de Óleo (m³)'].sum()
soma_prod_campos['Produção de Óleo (m³)'].sum()
soma_prod_estados['Produção de Óleo (m³)'].describe()

soma_prod_bacias2=df_cut.groupby(['Bacia']).sum()

plot = soma_prod_bacias2.plot.pie(y='Produção de Óleo (m³)',figsize=(7, 7), 
fontsize=12, title='Produção de petróleo por bacia',autopct='%.1f%%' )


soma_prod_estados['Produção de Óleo (m³)'].sum()
soma_prod_estados.Estado == 'Rio Grande do Norte'
soma_prod_estados[(soma_prod_estados.Estado == "Alagoas")]

# Gráficos de Linha com o Pyplot-Matplotlib

se_carmopolis=dfProd15[(dfProd15.Estado == "Sergipe") & (dfProd15.Campo == \
                            "CARMÓPOLIS") ]
rn_canto=dfProd15[(dfProd15.Estado == "Rio Grande do Norte") & (dfProd15.Campo == \
                            "CANTO DO AMARO") ]
am_leste=dfProd15[(dfProd15.Estado == "Amazonas") & (dfProd15.Campo == \
                            "LESTE DO URUCU") ]

soma_se_carmopolis=se_carmopolis.groupby(['Mês/Ano'],as_index=False).sum()
soma_rn_canto=rn_canto.groupby(['Mês/Ano'],as_index=False).sum()
soma_am_leste=am_leste.groupby(['Mês/Ano'],as_index=False).sum()

plt.rcParams.update({'font.size': 18})

plt.figure(5)
plt.plot(soma_rn_canto['Mês/Ano'],soma_rn_canto['Produção de Óleo (m³)'] \
         ,'r', label='Canto do Amaro (RN)')
plt.plot(soma_se_carmopolis['Mês/Ano'],soma_se_carmopolis['Produção de Óleo (m³)'] \
         ,'b', label='Carmópolis (SE)')
plt.plot(soma_am_leste['Mês/Ano'],soma_am_leste['Produção de Óleo (m³)'] \
         ,'g', label='Leste do Urucu (AM)')
plt.xlabel('Mês/Ano');plt.ylabel('Produção de Óleo (m³)');plt.legend(frameon=False)
degrees = 45; plt.xticks(rotation=degrees); plt.tight_layout(); plt.show()











