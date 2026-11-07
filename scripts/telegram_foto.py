"""Define a foto do canal do Telegram com brand/logo-grupo-640.jpg (roda uma vez, manualmente, no GitHub Actions).
O robô precisa estar como administrador com a permissão 'Alterar informações do canal'."""
import os, json, uuid, urllib.request
token, chat = os.environ["TELEGRAM_BOT_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
b = uuid.uuid4().hex
dados = open("brand/logo-grupo-640.jpg", "rb").read()
corpo = (f'--{b}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat}\r\n'
         f'--{b}\r\nContent-Disposition: form-data; name="photo"; filename="logo.jpg"\r\nContent-Type: image/jpeg\r\n\r\n').encode() + dados + f"\r\n--{b}--\r\n".encode()
req = urllib.request.Request(f"https://api.telegram.org/bot{token}/setChatPhoto", data=corpo,
                             headers={"Content-Type": f"multipart/form-data; boundary={b}"})
try:
    print(json.load(urllib.request.urlopen(req, timeout=60)))
except urllib.error.HTTPError as e:
    print(e.code, e.read().decode()); raise SystemExit(1)
