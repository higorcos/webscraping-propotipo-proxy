from browsermobproxy import Server
from selenium import webdriver
import json
import os
import time

# Caminho para o executável do BrowserMob Proxy
path_to_bmproxy = "C:/Users/higor/Documents/WorckCenter/webscraping-propotipo-proxy/browsermob-proxy-2.1.4-bin/bin/browsermob-proxy"

# Iniciar o servidor do BrowserMob Proxy
server = Server(path_to_bmproxy)
server.start()

# Configuração do proxy para o navegador Selenium
proxy = server.create_proxy()
proxy.new_har("api_capture",
              options={
                  'captureHeaders': True,
                  'captureContent': True,
                  #'captureContentTypes': ['application/json']  # Captura apenas conteúdo JSON
             }
              )  # Captura cabeçalhos e conteúdo

# Configuração do WebDriver para usar o proxy
options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server={proxy.proxy}')

# Desabilitar a verificação de segurança para evitar erros de certificado (não recomendado para produção)
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)

# Navegação para o site específico
driver.get('https://app2.tcema.tc.br/PCA/visualizarestrutura.zul')

# Espera 30 segundos para interagir com o site
time.sleep(60)

# Captura o log HAR das requisições
har_data = proxy.har

# Verificar se o diretório existe, se não, criá-lo
output_directory = "output"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Salvar os dados em um arquivo JSON
output_file_path = os.path.join(output_directory, 'har_data.json')
with open(output_file_path, 'w') as har_file:
    json.dump(har_data, har_file, indent=4)

# Imprimir URLs das requisições e conteúdo das respostas
for entry in har_data['log']['entries']:
    request_url = entry['request']['url']
    response = entry['response']
    if 'text' in response['content']:
        response_content = response
    else:
        response_content = response['content'].get('comment', 'No content available')
        response_content = response
    print(f"Request URL: {request_url}")
    print(f"Response Content: {response_content}\n")

# Encerramento do navegador e do proxy
driver.quit()

# Parar o servidor do BrowserMob Proxy após o uso
server.stop()
