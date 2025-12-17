import requests
r = requests.get('http://localhost:8000/api/clientes/')
print(f'Status GET: {r.status_code}')
if r.status_code == 200:
    print(f'Total clientes: {len(r.json())}')
else:
    print(f'Error: {r.text[:200]}')
