"""
تشغيل Streamlit Dashboard على Google Colab عبر ngrok
Run Streamlit Dashboard on Google Colab via ngrok

طريقة الاستخدام في Colab:
1. !pip install pyngrok streamlit scikit-learn pandas numpy matplotlib seaborn plotly
2. !wget <رابط ملف run_colab_ngrok.py>
3. !python run_colab_ngrok.py

ملاحظة هامة: إذا ظهر خطأ ERR_NGROK_334 أو ERR_NGROK_3200، قم بعمل "Restart Runtime" ثم شغّل مرة أخرى
"""
import os
import time
import subprocess
import sys
import random
import string

def generate_random_subdomain():
    """توليد اسم فرعي عشوائي لتجنب تعارض الأسماء"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

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

# قتل أي عمليات سابقة
print("🧹 Cleaning up previous processes...")
subprocess.run(["pkill", "-f", "streamlit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-f", "ngrok"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

# ضبط ngrok token
print(f"🔐 Setting ngrok auth token...")
conf.get_default().auth_token = token

# تشغيل Streamlit في الخلفية
print("🎬 Starting Streamlit server...")
proc = subprocess.Popen(
    ['streamlit', 'run', 'app.py',
     '--server.port', '8501',
     '--server.address', '0.0.0.0',
     '--server.headless', 'true',
     '--browser.gatherUsageStats', 'false'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

print("⏳ Waiting for Streamlit to start (10 seconds)...")
time.sleep(10)

# إنشاء نفق ngrok باسم عشوائي لتجنب التعارض
random_subdomain = generate_random_subdomain()
print(f"🔗 Creating ngrok tunnel with random subdomain: {random_subdomain}...")

try:
    # استخدام options لتحديد اسم عشوائي
    tunnel = ngrok.connect(addr=8501, bind_tls=True, options={"subdomain": random_subdomain})
    
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
    print("⚠️  If you see an error, do 'Runtime > Restart Runtime' and try again")
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
    print("1. ⭐ IMPORTANT: Do 'Runtime > Restart Runtime' in Colab and try again")
    print("2. Make sure your ngrok token is correct")
    print("3. Check if ngrok service is available in your region")
    print("4. Visit https://dashboard.ngrok.com to check your account status")
    print("5. The error might be due to a conflicting tunnel - restarting runtime fixes this")
    proc.terminate()
