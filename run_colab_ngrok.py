import os
import time
import subprocess
from pyngrok import ngrok

token = os.environ.get('NGROK_AUTHTOKEN')
if not token:
    raise ValueError('Please set NGROK_AUTHTOKEN in environment variables before running.')

ngrok.set_auth_token(token)

subprocess.Popen([
    'streamlit', 'run', 'app.py',
    '--server.port', '8501',
    '--server.address', 'localhost',
    '--server.headless', 'true'
], stdout=open('/content/streamlit.log', 'w'), stderr=subprocess.STDOUT)

time.sleep(8)
public_url = ngrok.connect(8501)
print('Public URL:', public_url)
