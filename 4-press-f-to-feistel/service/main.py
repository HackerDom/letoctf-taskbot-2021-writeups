import os
from logging.config import dictConfig

from flask import Flask, request

from feistel import Feistel

FLAG = os.environ["FLAG"].encode()
KEY = bytes.fromhex(os.environ["KEY"])


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)

cipher = Feistel(KEY)

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    if not data:
        app.logger.error(f'{request.remote_addr} /api/encrypt, Wrong data: {request.data}')
        return {'error': 'I need JSON'}
    
    try:
        pt = bytes.fromhex(data.get('pt'))
    except Exception as ex:
        app.logger.error(f'{request.remote_addr} /api/encrypt, Can\'t get pt: ({ex})')
        return {'error': 'I need "pt" param in hex'}

    if len(pt) > 128:
        app.logger.error(f'{request.remote_addr} /api/encrypt, "pt" is too long: {len(pt)}')
        return {'error': '"pt" is too long!'}

    ct = cipher.encrypt(pt)
    app.logger.info(f'{request.remote_addr} /api/encrypt, Nice pt: {pt.hex()}, ct: {ct.hex()}')

    return {'ct': ct.hex()}

@app.route('/api/get_flag')
def get_flag():
    app.logger.info(f'{request.remote_addr} /api/get_flag')
    return {'encrypted_flag': cipher.encrypt(FLAG).hex()}