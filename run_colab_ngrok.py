import os
import time
import subprocess
from pyngrok import ngrok, conf

token = os.environ.get('NGROK_AUTHTOKEN', '')
if not token:
    raise ValueError('Please set NGROK_AUTHTOKEN environment variable before running.')

conf.get_default().auth_token = token

proc = subprocess.Popen(
    ['streamlit', 'run', 'app.py',
     '--server.port', '8501',
     '--server.address', 'localhost',
     '--server.headless', 'true'],
    stdout=open('/content/streamlit.log', 'w'),
    stderr=subprocess.STDOUT
)

print("Streamlit starting, waiting 10 seconds...")
time.sleep(10)

tunnel = ngrok.connect(8501)
print('=' * 50)
print('Public URL:', tunnel.public_url)
print('=' * 50)
