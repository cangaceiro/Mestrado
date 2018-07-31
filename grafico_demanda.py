import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

dados = pd.read_csv('dados/2018-07-24-16:53-demanda.csv')
plt.xlabel('Geração')
plt.ylabel('Demanda GB')
plt.xlim((0, dados['geracao'].max()))
plt.ylim((0, dados['demanda'].max() + 2))
plt.plot(dados['geracao'], dados['demanda'])
plt.show()
