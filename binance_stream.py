import websocket
import json
import requests
import sys
import logging
import platform

if platform.system() == 'Linux':
    sys.path.append('/root/algotrading_infra/')
else:
    sys.path.append('/Users/sanket/algotrading/infra')

from src.orderbook import Order, Orderbook, Halfbook
from src.types import Exchange, Side, Lifespan

ws_url = 'wss://fstream.binance.com/ws/'
base_url = 'https://fapi.binance.com'
COIN = 'ETHUSDT'

# open stream and buffer events
# get max limit depth snapshot through rest api
# drop any event where u < lastupdateid
# firs processed event should have U <= lastupdateid and u >= lastupdateid
# while listening to stream, each new event's `pu` should be equiv to last 'u'
#   otherwise get depth snapshot again
# data in each event is absolute quantity @ price level
# if quantity = 0, remove price level

def get_snapshot(symbol: str, limit : int):
    ep = '/fapi/v1/depth'
    endpoint = base_url + ep
    params = {
        "symbol": symbol,
        "limit":limit
    }
    response = requests.get(endpoint, params=params)
    print(response.status_code)
    return response.json()

def get_exchangeInfo():
    ep = '/fapi/v1/exchangeInfo'
    endpoint = base_url + ep
    response = requests.get(endpoint)
    # print(response)
    return response


def build_book(symbol: str):
    book_data = get_snapshot(symbol=symbol, limit=500)


# def main():
#     logging.basicConfig(filename='binance_stream', level=logging.ERROR)


# if __name__ == '__main__':
#     main()



# get_snapshot(symbol= 'BTCUSDT', limit=500)
# print((get_exchangeInfo().json()))


# print(get_snapshot(symbol='ETHUSDT', limit=500))



# print('defs')
# def on_open(ws):
#     print("opened binance stream")

#     auth_data = {
#         'method': 'SUBSCRIBE',
#         'params': ['ethusdt@depth'],
#         'id':1
#     }
#     ws.send(json.dumps(auth_data))
#     print('sent sub')

# def on_message(ws, message):
#     message = json.loads(message)
#     print(message)

# def on_close(ws):
#     print("closed connection")





# ws = websocket.WebSocketApp(url=ws_url, 
#                             on_open=on_open, 
#                             on_message=on_message,
#                             on_close=on_close)     
# print('made ws')
# ws.run_forever()



import asyncio
import websockets
import json
from datetime import datetime

## BINANCE VERSION
async def connect_to_stream():
    # uri = "wss://fstream.binance.com/ws"  # Replace with the WebSocket stream URL
    uri = 'wss://fstream.binance.com/ws'   
    
    async with websockets.connect(uri) as websocket:
        n = 0
        symbol = 'ethusdt'
        level = 20
        speed = 0
        # stream = "{}@depth{}@{}ms".format(symbol.lower(), level, speed)
        s2 = "ethusdt@depth@100ms"
        stream = [s2]
        # json_msg = json.dumps({"method": "SUBSCRIBE", "params": stream, "id": id})

        subscription_message = {
            "method": "SUBSCRIBE",
            "params": stream,
            'id':1 # Replace with the actual stream name
            # Add any additional fields specific to your subscription message
        }
        
        await websocket.send(json.dumps(subscription_message))
        
        # Create a task to send the unsubscription message after 5 seconds
        # unsubscription_task = asyncio.ensure_future(send_unsubscription(websocket))
        while True:
            message = await websocket.recv()
            n += 1
            print(f'Recieved message ({n}): {message}')
        # Process the received message as per  your requirements
#             if unsubscription_task.done():
#                 break   
# # Run the connection functionee
#                 # Wait for the unsubscription task to complete before closing the connection
            # await send_unsubscription()
        
        # Optionally, you can perform any cle
        # anup or additional tasks here
            # await websocket.close()



async def send_unsubscription(websocket):
    await asyncio.sleep(10)  # Delay before sending the unsubscription message

    symbol = 'ethusdt'
    level = 20
    speed = 0
    stream = "{}@depth{}@{}ms".format(symbol.lower(), level, speed)

    s2 = "ethusdt@depth@100ms"
    stream = [stream]
    unsubscription_message = {
        "method": "UNSUBSCRIBE",
        "stream_name": stream  # Replace with the actual stream name
        # Add any additional fields specific to your unsubscription message
    }

        # json_msg2 = json.dumps({"method": "UNSUBSCRIBE", "params": stream2, "id": id})

    await websocket.send(json.dumps(unsubscription_message))

asyncio.get_event_loop().run_until_complete(connect_to_stream())
