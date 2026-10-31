import requests
import json

try:
    r = requests.get('http://127.0.0.1:8000/v1/models')
    print('vLLM /v1/models response code:', r.status_code)
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print('vLLM error:', e)

try:
    r2 = requests.get('http://127.0.0.1:8888/health')
    print('HexStrike 8888 response code:', r2.status_code)
    print(r2.text[:200])
except Exception as e:
    print('Hexstrike error:', e)
