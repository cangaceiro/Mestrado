import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

sns.set()


dados = pd.read_csv(
    'dados/2018-07-25-17:08-desvio.csv'
)

fig = plt.figure(1, figsize=(9, 6))

ax = fig.add_subplot(111)

bp = ax.boxplot([dados['cultural'], dados['genetico'], dados['dijkstra']])

plt.title('load average')

plt.ylabel('standard desviation')

ax.set_xticklabels(['ocupation Cultural', 'Ocupation Genetic', 'Ocupation SPF'])

plt.show()

filename = 'plots/{}.png'.format(dt.datetime.now().strftime('%Y-%m-%d-%H:%M'))

fig.savefig(filename, dpi=fig.dpi)

