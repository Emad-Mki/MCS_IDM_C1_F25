"""
تشغيل Streamlit Dashboard على Google Colab عبر ngrok
Run Streamlit Dashboard on Google Colab via ngrok

طريقة الاستخدام في Colab:
1. !pip install pyngrok streamlit scikit-learn pandas numpy matplotlib seaborn plotly
2. !wget <رابط ملف run_colab_ngrok.py>
3. !python run_colab_ngrok.py
"""
import os
import time
import subprocess
import sys

# التحقق من تثبيت المكتبات المطلوبة
try:
    from pyngrok import ngrok, conf
except ImportError:
    print("❌ Installing pyngrok...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])
    from pyngrok import ngrok, conf

# الحصول على token من متغير البيئة أو استخدام القيمة المباشرة
token = os.environ.get('NGROK_AUTHTOKEN', '3FghmjIhl8Oc4iIbV9Vre1J9HlH_6F5ykoVyfgacWCkGscjY9')

print("=" * 60)
print("🚀 Starting Streamlit Dashboard on Google Colab")
print("=" * 60)

# ضبط ngrok token
print(f"🔐 Setting ngrok auth token...")
conf.get_default().auth_token = token

# تشغيل Streamlit في الخلفية
print("🎬 Starting Streamlit server...")
proc = subprocess.Popen(
    ['streamlit', 'run', 'app.py',
     '--server.port', '8501',
     '--server.address', 'localhost',
     '--server.headless', 'true',
     '--browser.gatherUsageStats', 'false'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

print("⏳ Waiting for Streamlit to start (10 seconds)...")
time.sleep(10)

# إنشاء نفق ngrok
print("🔗 Creating ngrok tunnel...")
try:
    tunnel = ngrok.connect(8501)
    
    print("=" * 60)
    print("✅ Streamlit Dashboard is running!")
    print("=" * 60)
    print(f"🌐 Public URL: {tunnel.public_url}")
    print("=" * 60)
    print("\n📋 Instructions:")
    print("1. Click the link above to open the dashboard")
    print("2. The dashboard will show Regression, Classification, and Clustering results")
    print("3. You can interact with the models and visualize the data")
    print("\n⚠️  Keep this cell running to maintain the connection")
    print("=" * 60)
    
    # إبقاء النفق مفتوحاً
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping Streamlit and closing ngrok tunnel...")
        ngrok.disconnect()
        proc.terminate()
        print("Done!")
        
except Exception as e:
    print(f"❌ Error creating ngrok tunnel: {e}")
    print("\n💡 Troubleshooting tips:")
    print("1. Make sure your ngrok token is correct")
    print("2. Check if ngrok service is available in your region")
    print("3. Try restarting the runtime and run again")
    print("4. Visit https://dashboard.ngrok.com to check your account status")
    proc.terminate()
