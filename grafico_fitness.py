import pandas as pd
import matplotlib.pyplot as plt

dados = pd.read_csv('dados/2018-07-16-17:23-fitness.csv')

plt.plot(list(range(len(dados))), dados['Fitness Genético'], 'r-')
plt.plot(list(range(len(dados))), dados['Fitness Cultural'], 'g:')
plt.plot(list(range(len(dados))), dados['Fitness SPF'], 'b--')

plt.show()
