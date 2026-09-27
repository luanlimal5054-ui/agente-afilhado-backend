# Agente Afiliado Backend

Backend V1 do Agente Afiliado para integração com Mercado Livre.

## Render
Build Command:
`pip install -r requirements.txt`

Start Command:
`gunicorn -k uvicorn.workers.UvicornWorker app:app`

## Estado atual
A V1 sobe com dados zerados e endpoints básicos. O fluxo OAuth do Mercado Livre fica em modo seguro/pendente até as credenciais serem configuradas no Render. Não publica anúncios nem envia mensagens.
