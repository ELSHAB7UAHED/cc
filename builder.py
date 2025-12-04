import PyInstaller.__main__
import os
import sys
import shutil

def build_exe():
    print("🧙‍♂️ جاري تجميع الساحر الإلكتروني...")
    
    # تنظيف الملفات القديمة
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # إعدادات PyInstaller المتقدمة
    options = [
        'cs_aimbot.py',  # الملف الرئيسي
        '--name=CS_Aimbot_Elite',
        '--onefile',  # ملف واحد فقط
        '--windowed',  # بدون نافذة كونسول
        '--icon=icon.ico',  # إذا كان لديك أيقونة
        '--add-data=config.ini;.',  # إضافة ملفات إضافية
        '--uac-admin',  # طلب صلاحيات أدمن
        '--hidden-import=win32timezone',
        '--hidden-import=keyboard._winkeyboard',
        '--hidden-import=mss',
        '--clean',
        '--noconfirm',
        '--upx-dir=upx',  # لضغط الملف النهائي
    ]
    
    try:
        PyInstaller.__main__.run(options)
        print("✅ التجميع اكتمل بنجاح!")
        print(f"📁 الملف النهائي: dist/CS_Aimbot_Elite.exe")
        
        # إنشاء ملف معلومات
        with open('dist/README.txt', 'w', encoding='utf-8') as f:
            f.write("""
            🎮 CS Aimbot Elite v2.0 🎮
            ========================
            
            🚀 ميزات النظام:
            • كشف تلقائي للعدو
            • تتبع ذكي
            • إطلاق نار تلقائي
            • حركات واقعية غير ميكانيكية
            
            ⚙️ كيفية الاستخدام:
            1. شغل اللعبة (Counter Strike)
            2. شغل البرنامج كـ Administrator
            3. اضغط F2 لتفعيل النظام
            4. اضغط F10 للإيقاف
            
            ⚠️ ملاحظات هامة:
            • للاستخدام التعليمي فقط
            • لا تستخدم في سيرفرات عامة
            • قد يتم كشفه من أنظمة Anti-Cheat
            
            📞 الدعم: للأغراض التعليمية فقط
            """)
        
    except Exception as e:
        print(f"❌ خطأ في التجميع: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
