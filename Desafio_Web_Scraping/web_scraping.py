# pip install undetected-chromedriver
# pip install pandas
# pip install openpyxl

import setuptools
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

# Scrool falso
def simular_scroll(driver):
    scroll_steps = random.randint(3, 6)  # Quantidade aleatória
    for _ in range(scroll_steps):
        altura = random.randint(300, 800)
        driver.execute_script(f"window.scrollBy(0, {altura});")
        time.sleep(random.uniform(0.5, 1.5))  # Pausas


options = uc.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


driver = uc.Chrome(options=options)


dados_imoveis = {
    'metragem': [],
    'quartos': [],
    'banheiros': [],
    'vagas': [],
    'valor': [],
    'iptu': [],
    'condominio': [],
    'nome_rua': []
}

quantidade_imoveis = 0
pagina = 1

while quantidade_imoveis < 100:
    url = f"https://www.vivareal.com.br/venda/?transacao=venda&pagina={pagina}"
    print(f"\n Acessando página {pagina}...")
    driver.get(url)

    # Simula um usuário 
    simular_scroll(driver)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="rp-property-cd"]'))
        )
    except:
        print("Sem imóveis carregados nesta página, parando.")
        break

    imoveis = driver.find_elements(By.CSS_SELECTOR, '[data-cy="rp-property-cd"]')

    if not imoveis:
        print("Nenhum imóvel encontrado, parando.")
        break

    for imovel in imoveis:
        if quantidade_imoveis >= 100:
            break

        # Captura dos dados com tratamento de erro
        try:
            metragem = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text
        except:
            metragem = None

        try:
            quartos = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text
        except:
            quartos = None

        try:
            banheiros = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bathroomQuantity-txt"]').text
        except:
            banheiros = None

        try:
            vagas = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]').text
        except:
            vagas = None

        try:
            preco_section = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]')
            preco_p = preco_section.find_elements(By.TAG_NAME, 'p')

            valor = preco_p[0].text if len(preco_p) > 0 else None

            condominio = None
            iptu = None
            if len(preco_p) > 1:
                texto_cond_iptu = preco_p[1].text
                partes = texto_cond_iptu.split('•')
                for parte in partes:
                    parte = parte.strip()
                    if 'Cond.' in parte:
                        condominio = parte.replace('Cond.', '').strip()
                    elif 'IPTU' in parte:
                        iptu = parte.replace('IPTU', '').strip()
        except:
            valor = None
            condominio = None
            iptu = None

        try:
            nome_rua = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-street-txt"]').text
        except:
            nome_rua = None

        
        dados_imoveis['metragem'].append(metragem)
        dados_imoveis['quartos'].append(quartos)
        dados_imoveis['banheiros'].append(banheiros)
        dados_imoveis['vagas'].append(vagas)
        dados_imoveis['valor'].append(valor)
        dados_imoveis['iptu'].append(iptu)
        dados_imoveis['condominio'].append(condominio)
        dados_imoveis['nome_rua'].append(nome_rua)

        quantidade_imoveis += 1
        print(f"Imóvel {quantidade_imoveis} capturado.")

    # Delay aleatório 
    delay = random.uniform(3, 7)
    print(f"Aguardando {delay:.2f} segundos antes de ir para a próxima página...")
    time.sleep(delay)

    pagina += 1  

driver.quit()

df = pd.DataFrame(dados_imoveis)
df.to_excel("imoveis_vivareal_scraping.xlsx", index=False)

print(f"\nRaspagem finalizada! {len(df)} imóveis salvos no arquivo 'imoveis_vivareal_scraping.xlsx'.")