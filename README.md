# Como obter API_ID e API_HASH do Telegram

Para usar este script, voce precisa de credenciais da API do Telegram. Siga os passos abaixo:

## Passo a passo

1. Acesse [https://my.telegram.org](https://my.telegram.org)

2. Faca login com seu **numero de telefone** (mesmo formato do Telegram, ex: +5511999999999)

3. Voce recebera um **codigo de confirmacao** no proprio Telegram (no chat "Telegram")

4. Apos o login, clique em **"API development tools"**

5. Preencha o formulario para criar um app:
   - **App title**: qualquer nome (ex: "Meu Downloader")
   - **Short name**: qualquer nome curto (ex: "meuapp")
   - **Platform**: pode deixar "Desktop"
   - **Description**: pode deixar vazio

6. Clique em **"Create application"**

7. Voce vera o **App api_id** (um numero) e o **App api_hash** (uma string hexadecimal)

## Configurando

Abra o arquivo `config.py` e substitua os valores:

```python
API_ID = 123456                          # Seu api_id (numero)
API_HASH = "abcdef1234567890abcdef1234"  # Seu api_hash (string)
```

## Observacoes

- Essas credenciais sao **pessoais** e vinculadas a sua conta. Nao compartilhe com ninguem.
- Voce so precisa criar o app **uma vez**. As credenciais nao expiram.
- O Telegram permite no maximo **criar um app por conta**.
