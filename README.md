# Telegram Channel Videos Downloader

Download all videos from any Telegram channel automatically using the Telegram API.

## Funcionalidades

- Lista todos os seus canais e grupos do Telegram
- Detecta automaticamente se o canal possui videos
- Baixa todos os videos mantendo o nome original dos arquivos
- Suporta retomada: se parar no meio, basta rodar novamente que os ja baixados serao pulados
- Mostra progresso de download em tempo real

## Requisitos

- Python 3.8+
- Uma conta no Telegram

## Instalacao

1. Clone o repositorio:
```bash
git clone https://github.com/rodrigomerce/telegram-channel-videos-downloader.git
cd telegram-channel-videos-downloader
```

2. Instale a dependencia:
```bash
pip install telethon
```

3. Crie o arquivo de configuracao a partir do modelo:
```bash
cp config.example.py config.py
```

4. Edite o `config.py` com suas credenciais da API do Telegram:
```python
API_ID = 123456
API_HASH = "seu_api_hash_aqui"
```

> Nao sabe como obter essas credenciais? Veja o guia em [CONFIGURACAO.md](CONFIGURACAO.md).

## Uso

```bash
python download_telegram_videos.py
```

Na primeira execucao, sera solicitado seu numero de telefone e um codigo de verificacao enviado pelo Telegram. Depois disso, a sessao fica salva e nao sera necessario logar novamente.

O script ira:
1. Listar todos os seus canais e grupos
2. Voce escolhe o canal pelo numero
3. Verificar se o canal possui videos
4. Pedir confirmacao antes de iniciar
5. Baixar todos os videos na pasta `./videos/`

## Estrutura

```
├── config.example.py           # Modelo de configuracao (copie para config.py)
├── config.py                   # Suas credenciais (ignorado pelo git)
├── CONFIGURACAO.md             # Guia para obter API_ID e API_HASH
├── download_telegram_videos.py # Script principal
└── videos/                     # Pasta onde os videos sao salvos
```
