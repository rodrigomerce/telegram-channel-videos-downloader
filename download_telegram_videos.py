import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat

try:
    from config import API_ID, API_HASH
except ImportError:
    print("Arquivo config.py nao encontrado!")
    print("Copie o config.example.py para config.py e preencha suas credenciais.")
    print("Veja CONFIGURACAO.md para instrucoes detalhadas.")
    exit(1)

DOWNLOAD_DIR = "./videos"
SCAN_LIMIT = 50  # mensagens verificadas para detectar vídeos


def is_video(message):
    """Verifica se a mensagem contém um vídeo."""
    if message.video:
        return True
    if message.document and message.document.mime_type:
        return message.document.mime_type.startswith("video/")
    return False


def get_filename(message):
    """Extrai o nome original do arquivo ou gera um padrão."""
    if message.document:
        for attr in message.document.attributes:
            if hasattr(attr, "file_name") and attr.file_name:
                name = attr.file_name
                for char in '<>:"/\\|?*':
                    name = name.replace(char, "_")
                return name
    return f"video_{message.id}.mp4"


async def listar_canais(client):
    """Lista todos os canais e grupos do usuário e retorna o escolhido."""
    canais = []

    print("\nBuscando seus canais e grupos...\n")

    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, (Channel, Chat)):
            canais.append({
                "id": entity.id,
                "nome": dialog.name,
                "username": getattr(entity, "username", None),
                "tipo": "Canal" if getattr(entity, "broadcast", False) else "Grupo",
            })

    if not canais:
        print("Nenhum canal ou grupo encontrado.")
        return None

    print(f"{'#':<5} {'Tipo':<8} {'Nome'}")
    print("-" * 60)
    for i, c in enumerate(canais, 1):
        sufixo = f"  (@{c['username']})" if c["username"] else ""
        print(f"{i:<5} {c['tipo']:<8} {c['nome']}{sufixo}")

    print(f"\nTotal: {len(canais)} encontrados.")

    while True:
        escolha = input("\nDigite o numero do canal desejado (0 para sair): ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(canais):
            return canais[int(escolha) - 1]
        print("Opcao invalida. Tente novamente.")


async def verificar_videos(client, channel_id):
    """Verifica as primeiras mensagens do canal para detectar vídeos."""
    print(f"\nAnalisando as ultimas {SCAN_LIMIT} mensagens do canal...")

    video_count = 0
    msg_count = 0

    async for message in client.iter_messages(channel_id, limit=SCAN_LIMIT):
        msg_count += 1
        if is_video(message):
            video_count += 1

    return video_count, msg_count


async def baixar_videos(client, channel_id, channel_nome):
    """Baixa todos os vídeos do canal."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    print(f"\nBaixando videos de: {channel_nome}")
    print(f"Pasta de destino: {os.path.abspath(DOWNLOAD_DIR)}\n")

    total = 0
    downloaded = 0
    skipped = 0

    async for message in client.iter_messages(channel_id):
        if is_video(message):
            total += 1
            filename = get_filename(message)
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            if os.path.exists(filepath):
                print(f"  [{total}] Ja existe, pulando: {filename}")
                skipped += 1
                continue

            print(f"  [{total}] Baixando: {filename}...")

            await client.download_media(
                message,
                file=filepath,
                progress_callback=lambda current, total_bytes:
                    print(f"\r    Progresso: {current / total_bytes * 100:.1f}%", end="", flush=True),
            )
            print()
            downloaded += 1

    print(f"\nConcluido! {downloaded} baixados, {skipped} pulados, {total} videos encontrados.")


async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.start()
    print("Conectado ao Telegram!")

    canal = await listar_canais(client)
    if not canal:
        print("Saindo...")
        await client.disconnect()
        return

    print(f"\nVoce escolheu: {canal['nome']}")

    # Monta o ID no formato que o Telethon espera para canais
    channel_id = int(f"-100{canal['id']}")

    # Verifica se o canal tem vídeos antes de iniciar o download
    video_count, msg_count = await verificar_videos(client, channel_id)

    if video_count == 0:
        print(f"\nNenhum video encontrado nas ultimas {msg_count} mensagens.")
        print("Este canal nao parece conter videos.")
        await client.disconnect()
        return

    print(f"Encontrados {video_count} videos nas ultimas {msg_count} mensagens analisadas.")

    confirma = input("\nDeseja iniciar o download de TODOS os videos? (s/n): ").strip().lower()
    if confirma != "s":
        print("Download cancelado.")
        await client.disconnect()
        return

    await baixar_videos(client, channel_id, canal["nome"])
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
