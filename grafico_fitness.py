import pandas as pd
import matplotlib.pyplot as plt

dados = pd.read_csv('dados/2018-07-21-12:20-fitness.csv')

plt.plot(list(range(len(dados))), dados['Fitness Geneti'],'g:')
plt.plot(list(range(len(dados))), dados['Fitness Cultural'], 'r-')
plt.plot(list(range(len(dados))), dados['Fitness SPF'], 'b--')
plt.xlabel("Generations")
plt.ylabel("Objetive Function Value")
plt.legend()
plt.show()
