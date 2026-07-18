# 🤖 Bot Telegram

Bot desenvolvido em Python utilizando a API do Telegram para divulgar produtos por mensagens automáticas.

## Tecnologias

- Python
- python-telegram-bot
- python-dotenv
- requests
- beautifulsoup4
- selenium
- webdriver-manager

## Como executar o bot

1. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Defina a variável de ambiente do token do Telegram:
   ```bash
   set BOT_TOKEN=seu_token_aqui
   ```
4. Inicie o bot:
   ```bash
   python app.py
   ```

## Como executar o scraper da Amazon

O projeto também possui um script separado para buscar ofertas da Amazon e salvar produtos em um arquivo JSON que o bot lê depois.

1. Certifique-se de que as dependências foram instaladas.
2. Execute:
   ```bash
   python amazon_scraper.py
   ```
3. O script irá abrir a página de ofertas da Amazon, coletar produtos com preço identificado e salvar os dados em:
   ```text
   products.json
   ```

## O que o scraper salva no JSON

O arquivo products.json é usado pelo handler de produtos do bot. Cada item contém:

- name: nome do produto
- price: preço encontrado na oferta
- description: descrição fixa da oferta
- link: link limpo do produto

Exemplo:

```json
[
  {
    "name": "Notebook Gamer Lenovo",
    "price": "R$5.899,00",
    "description": "Oferta capturada da Amazon",
    "link": "https://www.amazon.com.br/Notebook-Lenovo-15irx9-I5-13450hx-Nvidia/dp/B0H4HYLQ71"
  }
]
```

Depois que o JSON é atualizado, o comando /produtos do bot lê esse arquivo e envia os produtos para o Telegram um por vez.

## Funcionalidades

- [x] Conexão com Telegram
- [x] Comando /start
- [x] Comando /produtos
- [ ] Menu de botões
- [ ] Cadastro de produtos
- [ ] Banco de dados
- [ ] Sistema de ofertas
- [ ] Links de afiliados

