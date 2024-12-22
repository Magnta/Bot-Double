import requests
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# Token do seu bot
TELEGRAM_TOKEN = '7017786436:AAEdctaqKXWuMo0rsVoDHn9RwZun7cFDag4'
CHAT_ID = '-4641113050'  # ID do chat para enviar mensagens

bot = Bot(token=TELEGRAM_TOKEN)

# Função que chama a API para obter os resultados anteriores
async def obter_resultados():
    cookies = {
        '_gid': 'GA1.2.781127896.1714749072',
        'AMP_MKTG': 'JTdCJTdE',
        '_did': 'web_712234434B09A034',
        'kwai_uuid': '4f8f5347e9db8f1a30e3a0751d616c40',
        '_gcl_au': '1.1.1274132088.1714749077',
        '_fbp': 'fb.1.1714749077202.1498210684',
        'AMP': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI5NTBlMTNlMy05MDBiLTQwMTQtYWE2Yy0xZDY4MWEzOGVmNzYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE0NzQ5MDc0MzA0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNDc0OTA3NDM5MCUyQyUyMlxhc3RFdmVudElkJTIyJTNBMCU3RA==',
        '_ga_LR2H8FWXB7': 'GS1.1.1714757367.3.1.1714757372.0.0.0',
        '_ga': 'GA1.1.1834781342.1714749072',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5,it;q=0.4,es;q=0.3,ru;q=0.2',
        'device_id': '950e13e3-900b-4014-aa6c-1d681a38ef76',
        'referer': 'https://jonbet.com/pt/games/double',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get('https://jonbet.com/api/roulette_games/recent', cookies=cookies, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = [result['roll'] for result in data]
            return results
        else:
            print(f"Erro na API: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao chamar a API: {e}")
        return None

# Função para determinar a cor de acordo com o resultado
def determinar_cor(resultado):
    if resultado == 1 or resultado == 2:
        return '⚪'  # Branco
    elif resultado == 3 or resultado == 4:
        return '🟢'  # Verde
    elif resultado == 5 or resultado == 6:
        return '⚫'  # Preto
    return '❓'  # Cor desconhecida

# Função para prever a próxima cor
def prever_proxima_cor(results):
    cor_contagem = {'🟢': 0, '⚫': 0, '⚪': 0}
    for cor in results[:5]:
        if cor in cor_contagem:
            cor_contagem[cor] += 1
    return max(cor_contagem, key=cor_contagem.get)

# Função para enviar mensagem com botão pelo Telegram
async def enviar_mensagem(cor):
    try:
        texto = f"💎 APOSTA CONFIRMADA 💎\n💰 APOSTE NA COR {cor}\n🆘 Nosso sinais só funcionam nesta casa de apostas. Se cadastrar por outro link vai tomar red."
        
        # Configurando botão com link
        botao = InlineKeyboardButton("🔗 Acessar Casa de Apostas", url="https://encurtador.com.br/GUenE")
        teclado = InlineKeyboardMarkup([[botao]])
        
        await bot.send_message(chat_id=CHAT_ID, text=texto, reply_markup=teclado)
        print(f"Mensagem enviada com botão: {texto}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

# Função principal para monitorar os resultados
async def monitorar_resultados():
    resultado_anterior = None

    while True:
        try:
            results = await obter_resultados()
            if results:
                cores = [determinar_cor(resultado) for resultado in results]
                print(f"Últimos resultados: {cores}")

                proxima_cor = prever_proxima_cor(cores)
                print(f"Próxima cor prevista: {proxima_cor}")

                if proxima_cor != resultado_anterior:
                    resultado_anterior = proxima_cor
                    await enviar_mensagem(proxima_cor)

            await asyncio.sleep(5)  # Aguarda 5 segundos antes de verificar novamente
        except Exception as e:
            print(f"Erro durante a execução: {e}")

if __name__ == '__main__':
    asyncio.run(monitorar_resultados())
