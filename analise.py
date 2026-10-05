import json
import os
import time
from datetime import datetime
from random import random
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns

matplotlib.use('Agg')

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'
ARQUIVO_CSV = './taxa-cdi.csv'
REPETICOES = 10


def extrair_taxa_cdi():
    """Capta a taxa CDI mais recente da API do BCB."""
    try:
        response = requests.get(url=URL, timeout=30)
        response.raise_for_status()
    except requests.HTTPError:
        print('Dado não encontrado, parando a execução.')
        raise
    except Exception:
        print('Erro, parando a execução.')
        raise
    return float(json.loads(response.text)[-1]['valor'])


def salvar_registro(taxa_base):
    """Acrescenta uma linha (data, hora, taxa) ao arquivo CSV."""
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')
    cdi = taxa_base + (random() - 0.5)

    if not os.path.exists(ARQUIVO_CSV):
        with open(file=ARQUIVO_CSV, mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    with open(file=ARQUIVO_CSV, mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')


def gerar_grafico(nome_grafico):
    """Lê o CSV e salva o gráfico da taxa por hora em <nome_grafico>.png."""
    df = pd.read_csv(ARQUIVO_CSV)
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    grafico.tick_params(axis='x', labelrotation=90)
    plt.tight_layout()
    plt.savefig(f'{nome_grafico}.png')


def main():
    if len(argv) < 2:
        raise SystemExit('Uso: python analise.py <nome-do-grafico>')

    taxa_base = extrair_taxa_cdi()
    for _ in range(REPETICOES):
        salvar_registro(taxa_base)
        time.sleep(1)

    gerar_grafico(argv[1])
    print('Sucesso')


if __name__ == '__main__':
    main()
