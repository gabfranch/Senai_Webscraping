import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://masander.github.io/AlimenticiaLTDA-financeiro/?authuser=0')

dic_despesas = {
    'id_despesa': [],
    'data': [],
    'tipo': [],
    'setor': [],
    'valor': [],
    'fornecedor': []
}

dic_orcamento = {
    'setor': [],
    'mes': [],
    'ano': [],
    'valor_previsto': [],
    'valor_realizado': []
}

trs = driver.find_elements(By.TAG_NAME, 'tr')

for tr in trs:
    try:
        id_despesa = tr.find_element(By.CLASS_NAME, 'td_id_despesa').text.strip()
        data = tr.find_element(By.CLASS_NAME, 'td_data').text.strip()
        tipo = tr.find_element(By.CLASS_NAME, 'td_tipo').text.strip()
        setor = tr.find_element(By.CLASS_NAME, 'td_setor').text.strip()
        valor = tr.find_element(By.CLASS_NAME, 'td_valor').text.strip()
        fornecedor = tr.find_element(By.CLASS_NAME, 'td_fornecedor').text.strip()

        dic_despesas['id_despesa'].append(id_despesa)
        dic_despesas['data'].append(data)
        dic_despesas['tipo'].append(tipo)
        dic_despesas['setor'].append(setor)
        dic_despesas['valor'].append(valor)
        dic_despesas['fornecedor'].append(fornecedor)
    except:
        continue

print('Despesas coletadas')

botao = driver.find_element(By.XPATH, '//*[@id="SubPageContainer"]/div[1]/nav/button[2]')
botao.click()

for tr in trs:
    try:
        setor = tr.find_element(By.CLASS_NAME, 'td_setor').text.strip()
        mes = tr.find_element(By.CLASS_NAME, 'td_mes').text.strip()
        ano = tr.find_element(By.CLASS_NAME, 'td_ano').text.strip()
        valor_previsto = tr.find_element(By.CLASS_NAME, 'td_valor_previsto').text.strip()
        valor_realizado = tr.find_element(By.CLASS_NAME, 'td_valor_realizado').text.strip()

        dic_orcamento['setor'].append(setor)
        dic_orcamento['mes'].append(mes)
        dic_orcamento['ano'].append(ano)
        dic_orcamento['valor_previsto'].append(valor_previsto)
        dic_orcamento['valor_realizado'].append(valor_realizado)
    except:
        continue

print('Orcamentos coletados')

driver.quit()

df_despesas = pd.DataFrame(dic_despesas)
df_orcamento = pd.DataFrame(dic_orcamento)

with pd.ExcelWriter('alimenticia_senai.xlsx') as writer:
    df_despesas.to_excel(writer, sheet_name='despesas', index=False)
    df_orcamento.to_excel(writer, sheet_name='orcamento', index=False)







