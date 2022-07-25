from fastapi import FastAPI, WebSocket  # Создаем websocket в нашем приложении FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Документ HTML с JavaScript, в одной строке
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Заказ</title>
    </head>
    <body>
        <h1>Сообщение</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Отправить сообщение</button>
        </form>
        <ol id='messages'>
        </ol>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):  # Создаем websocket в нашем приложении FastAPI
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")  # В нашем websocket маршруте мы получаем сообщение await и также
                                              # отправляем его
