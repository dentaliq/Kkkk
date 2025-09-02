# app.py

import os
import socket
from flask import Flask, render_template, request, jsonify

# إعداد تطبيق Flask
app = Flask(__name__)

# قائمة لتخزين جميع رسائل الدردشة
messages = []

# دالة للحصول على عنوان IP المحلي لجهاز الكمبيوتر
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # هذه الحيلة تسمح بالحصول على عنوان IP الصحيح للشبكة المحلية دون الحاجة لإنترنت فعلي
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# المسار الرئيسي الذي يعرض واجهة المحادثة
@app.route('/')
def index():
    return render_template('index.html')

# مسار لإرسال الرسائل الجديدة
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    sender = data.get('sender', 'مجهول')
    message = data.get('message', '')
    if message:
        messages.append({'sender': sender, 'message': message})
    return jsonify(success=True)

# مسار لجلب الرسائل من الخادم
@app.route('/get_messages')
def get_messages():
    return jsonify(messages=messages)

if __name__ == '__main__':
    host_ip = get_local_ip()
    print("==================================================")
    print("  خادم الدردشة المحلي جاهز!")
    print(f"  للانضمام، اطلب من أصدقائك فتح المتصفح وكتابة هذا العنوان: http://{host_ip}:5000")
    print("  تأكد أن جميع الأجهزة متصلة بنفس الشبكة المحلية.")
    print("==================================================")
    
    # تشغيل التطبيق على الشبكة المحلية
    app.run(host='0.0.0.0', port=5000)
