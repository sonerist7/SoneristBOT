import discord
from discord.ext import commands
import json
import os
import time
import random

# =========================
# BOT AYARLARI
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=("s.", "S."),
    intents=intents
)

DOSYA = "data.json"
MAKS_GUMUS = 250000
GUNLUK_GUMUS = 5000


# =========================
# VERİ SİSTEMİ
# =========================

def verileri_yukle():
    if not os.path.exists(DOSYA):
        return {}

    try:
        with open(DOSYA, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    except:
        return {}


def verileri_kaydet(veriler):
    with open(DOSYA, "w", encoding="utf-8") as dosya:
        json.dump(veriler, dosya, ensure_ascii=False, indent=4)


veriler = verileri_yukle()


def kullanici_olustur(user_id):
    user_id = str(user_id)

    if user_id not in veriler:
        veriler[user_id] = {
            "gumus": 0,
            "son_gunluk": 0,

            "kazma": 1,
            "kazma_kullanim": 100,

            "cevherler": {},

            "maden_sayisi": 0,
            "toplam_cevher": 0,
            "en_degerli_cevher": ""
        }

        verileri_kaydet(veriler)

    # Eski kullanıcı verileri için eksik alanları tamamla
    kullanici = veriler[user_id]

    if "kazma" not in kullanici:
        kullanici["kazma"] = 1

    if "kazma_kullanim" not in kullanici:
        kullanici["kazma_kullanim"] = 100

    if "cevherler" not in kullanici:
        kullanici["cevherler"] = {}

    if "maden_sayisi" not in kullanici:
        kullanici["maden_sayisi"] = 0

    if "toplam_cevher" not in kullanici:
        kullanici["toplam_cevher"] = 0

    if "en_degerli_cevher" not in kullanici:
        kullanici["en_degerli_cevher"] = ""

    return kullanici


def sayi_yaz(sayi):
    return f"{sayi:,}".replace(",", ".")


# =========================
# KAZMALAR
# =========================

KAZMALAR = {
    1: {"ad": "Taş Kazma", "emoji": "🪨", "fiyat": 0, "kullanim": 100},
    2: {"ad": "Bakır Kazma", "emoji": "🟠", "fiyat": 1000, "kullanim": 200},
    3: {"ad": "Demir Kazma", "emoji": "⚙️", "fiyat": 5000, "kullanim": 300},
    4: {"ad": "Çelik Kazma", "emoji": "🔩", "fiyat": 15000, "kullanim": 400},
    5: {"ad": "Gümüş Kazma", "emoji": "🩶", "fiyat": 30000, "kullanim": 500},
    6: {"ad": "Altın Kazma", "emoji": "🟡", "fiyat": 50000, "kullanim": 600},
    7: {"ad": "Titanyum Kazma", "emoji": "🔷", "fiyat": 100000, "kullanim": 750},
    8: {"ad": "Kobalt Kazma", "emoji": "🔵", "fiyat": 175000, "kullanim": 900},
    9: {"ad": "Mithril Kazma", "emoji": "🔹", "fiyat": 300000, "kullanim": 1000},
    10: {"ad": "Elmas Kazma", "emoji": "💎", "fiyat": 500000, "kullanim": 1250},
    11: {"ad": "Yakut Kazma", "emoji": "❤️", "fiyat": 750000, "kullanim": 1500},
    12: {"ad": "Safir Kazma", "emoji": "💙", "fiyat": 1000000, "kullanim": 1750},
    13: {"ad": "Zümrüt Kazma", "emoji": "💚", "fiyat": 1500000, "kullanim": 2000},
    14: {"ad": "Obsidyen Kazma", "emoji": "🖤", "fiyat": 2000000, "kullanim": 2250},
    15: {"ad": "Kristal Kazma", "emoji": "🔮", "fiyat": 3000000, "kullanim": 2500},
    16: {"ad": "Lav Kazma", "emoji": "🌋", "fiyat": 4000000, "kullanim": 2750},
    17: {"ad": "Ejderha Kazma", "emoji": "🐉", "fiyat": 5500000, "kullanim": 3000},
    18: {"ad": "Kadim Kazma", "emoji": "🏺", "fiyat": 7500000, "kullanim": 3500},
    19: {"ad": "Efsane Kazma", "emoji": "🌟", "fiyat": 10000000, "kullanim": 4000},
    20: {"ad": "Kraliyet Kazma", "emoji": "👑", "fiyat": 15000000, "kullanim": 5000},
}


# =========================
# CEVHERLER
# =========================

CEVHERLER = {
    "taş": {"ad": "Taş", "emoji": "🪨", "fiyat": 10},
    "kömür": {"ad": "Kömür", "emoji": "⚫", "fiyat": 25},
    "bakır": {"ad": "Bakır", "emoji": "🟠", "fiyat": 50},
    "demir": {"ad": "Demir", "emoji": "⛓️", "fiyat": 100},
    "kalay": {"ad": "Kalay", "emoji": "🩶", "fiyat": 150},
    "kurşun": {"ad": "Kurşun", "emoji": "⚙️", "fiyat": 200},
    "çinko": {"ad": "Çinko", "emoji": "🔘", "fiyat": 300},
    "gümüş": {"ad": "Gümüş", "emoji": "🥈", "fiyat": 500},
    "altın": {"ad": "Altın", "emoji": "🟡", "fiyat": 750},
    "nikel": {"ad": "Nikel", "emoji": "🪙", "fiyat": 1000},
    "krom": {"ad": "Krom", "emoji": "🪞", "fiyat": 1250},
    "kobalt": {"ad": "Kobalt", "emoji": "🔵", "fiyat": 1500},
    "titanyum": {"ad": "Titanyum", "emoji": "🔷", "fiyat": 2000},
    "platin": {"ad": "Platin", "emoji": "⚪", "fiyat": 3000},
    "paladyum": {"ad": "Paladyum", "emoji": "💿", "fiyat": 4000},
    "uranyum": {"ad": "Uranyum", "emoji": "☢️", "fiyat": 5000},
    "mithril": {"ad": "Mithril", "emoji": "🔹", "fiyat": 7500},
    "adamantit": {"ad": "Adamantit", "emoji": "💠", "fiyat": 10000},
    "obsidyen": {"ad": "Obsidyen", "emoji": "🖤", "fiyat": 12500},
    "ametist": {"ad": "Ametist", "emoji": "🟣", "fiyat": 15000},
    "kuvars": {"ad": "Kuvars", "emoji": "🤍", "fiyat": 17500},
    "akik": {"ad": "Akik", "emoji": "🟤", "fiyat": 20000},
    "kehribar": {"ad": "Kehribar", "emoji": "🟧", "fiyat": 25000},
    "topaz": {"ad": "Topaz", "emoji": "🟨", "fiyat": 30000},
    "safir": {"ad": "Safir", "emoji": "💙", "fiyat": 40000},
    "yakut": {"ad": "Yakut", "emoji": "❤️", "fiyat": 50000},
    "zümrüt": {"ad": "Zümrüt", "emoji": "💚", "fiyat": 65000},
    "opal": {"ad": "Opal", "emoji": "🌈", "fiyat": 80000},
    "oniks": {"ad": "Oniks", "emoji": "🌑", "fiyat": 100000},
    "granat": {"ad": "Granat", "emoji": "🔴", "fiyat": 125000},
    "aytaşı": {"ad": "Aytaşı", "emoji": "🌙", "fiyat": 150000},
    "güneştaşı": {"ad": "Güneştaşı", "emoji": "☀️", "fiyat": 175000},
    "kara kristal": {"ad": "Kara Kristal", "emoji": "🌘", "fiyat": 200000},
    "buz kristali": {"ad": "Buz Kristali", "emoji": "🧊", "fiyat": 225000},
    "kan kristali": {"ad": "Kan Kristali", "emoji": "🩸", "fiyat": 250000},
    "ruh kristali": {"ad": "Ruh Kristali", "emoji": "👻", "fiyat": 300000},
    "ejderha kristali": {"ad": "Ejderha Kristali", "emoji": "🐲", "fiyat": 400000},
    "kadim cevher": {"ad": "Kadim Cevher", "emoji": "🏺", "fiyat": 500000},
    "efsane cevher": {"ad": "Efsane Cevher", "emoji": "🌟", "fiyat": 750000},
    "kraliyet cevheri": {"ad": "Kraliyet Cevheri", "emoji": "👑", "fiyat": 1000000},
}


# =========================
# MADEN HAVUZLARI
# =========================

# Her kazma bir önceki kazmanın cevherlerini de bulabilir.
# Daha yüksek kazma = daha fazla cevher türünün açılması.

MADEN_HAVUZLARI = {
    1: ["taş", "kömür"],

    2: ["taş", "kömür", "bakır", "demir"],

    3: ["taş", "kömür", "bakır", "demir", "kalay"],

    4: ["taş", "kömür", "bakır", "demir", "kalay", "kurşun", "çinko"],

    5: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş"
    ],

    6: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel", "krom"
    ],

    7: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin"
    ],

    8: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum"
    ],

    9: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit"
    ],

    10: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist"
    ],

    11: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik"
    ],

    12: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz"
    ],

    13: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz", "safir", "yakut", "zümrüt"
    ],

    14: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz", "safir", "yakut", "zümrüt",
        "opal", "oniks"
    ],

    15: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz", "safir", "yakut", "zümrüt",
        "opal", "oniks", "granat", "aytaşı"
    ],

    16: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz", "safir", "yakut", "zümrüt",
        "opal", "oniks", "granat", "aytaşı", "güneştaşı",
        "kara kristal", "buz kristali"
    ],

    17: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz", "safir", "yakut", "zümrüt",
        "opal", "oniks", "granat", "aytaşı", "güneştaşı",
        "kara kristal", "buz kristali", "kan kristali",
        "ruh kristali", "ejderha kristali"
    ],

    18: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz", "safir", "yakut", "zümrüt",
        "opal", "oniks", "granat", "aytaşı", "güneştaşı",
        "kara kristal", "buz kristali", "kan kristali",
        "ruh kristali", "ejderha kristali", "kadim cevher"
    ],

    19: [
        "taş", "kömür", "bakır", "demir", "kalay",
        "kurşun", "çinko", "gümüş", "altın", "nikel",
        "krom", "kobalt", "titanyum", "platin",
        "paladyum", "uranyum", "mithril", "adamantit",
        "obsidyen", "ametist", "kuvars", "akik",
        "kehribar", "topaz", "safir", "yakut", "zümrüt",
        "opal", "oniks", "granat", "aytaşı", "güneştaşı",
        "kara kristal", "buz kristali", "kan kristali",
        "ruh kristali", "ejderha kristali", "kadim cevher",
        "efsane cevher"
    ],

    20: list(CEVHERLER.keys())
}


# =========================
# PING
# =========================

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")


# =========================
# BAKİYE
# =========================

@bot.command()
async def bakiye(ctx):
    kullanici = kullanici_olustur(ctx.author.id)

    await ctx.send(
        f"💰 **{ctx.author.display_name}**\n"
        f"Gümüş: **{sayi_yaz(kullanici['gumus'])}**"
    )


@bot.command()
async def para(ctx):
    await bakiye(ctx)


# =========================
# GÜNLÜK
# =========================

@bot.command()
async def günlük(ctx):
    kullanici = kullanici_olustur(ctx.author.id)

    simdi = time.time()
    gecen = simdi - kullanici["son_gunluk"]

    if gecen < 86400:
        kalan = int(86400 - gecen)
        saat = kalan // 3600
        dakika = (kalan % 3600) // 60

        await ctx.send(
            f"⏳ Günlük ödülünü zaten aldın.\n"
            f"Tekrar almak için **{saat} saat {dakika} dakika** bekle."
        )
        return

    kullanici["gumus"] += GUNLUK_GUMUS
    kullanici["son_gunluk"] = simdi

    verileri_kaydet(veriler)

    await ctx.send(
        f"🎁 Günlük ödülünü aldın!\n"
        f"💰 **+{sayi_yaz(GUNLUK_GUMUS)} Gümüş**"
    )


# =========================
# GÜMÜŞ GÖNDER
# =========================

@bot.command()
async def gönder(ctx, uye: discord.Member = None, miktar: int = None):

    if uye is None or miktar is None:
        await ctx.send("❌ Kullanım: `s.gönder @kişi miktar`")
        return

    if miktar <= 0:
        await ctx.send("❌ Miktar 0'dan büyük olmalı.")
        return

    if uye.id == ctx.author.id:
        await ctx.send("❌ Kendine Gümüş gönderemezsin.")
        return

    gonderen = kullanici_olustur(ctx.author.id)
    alan = kullanici_olustur(uye.id)

    if gonderen["gumus"] < miktar:
        await ctx.send("❌ Yeterli Gümüşün yok.")
        return

    gonderen["gumus"] -= miktar
    alan["gumus"] += miktar

    verileri_kaydet(veriler)

    await ctx.send(
        f"💸 **{ctx.author.display_name}** → **{uye.display_name}**\n"
        f"💰 **{sayi_yaz(miktar)} Gümüş** gönderildi."
    )


# =========================
# CF
# =========================

@bot.command()
async def cf(ctx, *args):

    kullanici = kullanici_olustur(ctx.author.id)

    if len(args) == 1:
        secim = "yazı"
        miktar_text = args[0]

    elif len(args) == 2:
        secim = args[0].lower()
        miktar_text = args[1]

        if secim not in ["yazı", "tura"]:
            await ctx.send("❌ Seçim `yazı` veya `tura` olmalı.")
            return

    else:
        await ctx.send(
            "❌ Kullanım:\n"
            "`s.cf 500`\n"
            "`s.cf yazı 500`\n"
            "`s.cf tura 500`\n"
            "`s.cf all`"
        )
        return

    if miktar_text.lower() == "all":
        miktar = min(kullanici["gumus"], MAKS_GUMUS)
    else:
        try:
            miktar = int(miktar_text)
        except:
            await ctx.send("❌ Geçerli bir miktar yaz.")
            return

    if miktar <= 0:
        await ctx.send("❌ Geçerli bir miktar yaz.")
        return

    if kullanici["gumus"] < miktar:
        await ctx.send("❌ Yeterli Gümüşün yok.")
        return

    sonuc = random.choice(["yazı", "tura"])

    kullanici["gumus"] -= miktar

    if secim == sonuc:
        kazanc = miktar * 2
        kullanici["gumus"] += kazanc

        await ctx.send(
            f"🪙 **{sonuc.upper()}!**\n"
            f"🎉 Kazandın!\n"
            f"💰 Kazanç: **{sayi_yaz(miktar)} Gümüş**"
        )

    else:
        await ctx.send(
            f"🪙 **{sonuc.upper()}!**\n"
            f"❌ Kaybettin.\n"
            f"💸 Kayıp: **{sayi_yaz(miktar)} Gümüş**"
        )

    verileri_kaydet(veriler)


# =========================
# SLOT
# =========================

async def slot_oyna(ctx, miktar_text):

    kullanici = kullanici_olustur(ctx.author.id)

    if miktar_text.lower() == "all":
        miktar = min(kullanici["gumus"], MAKS_GUMUS)
    else:
        try:
            miktar = int(miktar_text)
        except:
            await ctx.send("❌ Geçerli bir miktar yaz.")
            return

    if miktar <= 0:
        await ctx.send("❌ Geçerli bir miktar yaz.")
        return

    if kullanici["gumus"] < miktar:
        await ctx.send("❌ Yeterli Gümüşün yok.")
        return

    semboller = ["🍒", "🍋", "🍊", "🔔", "⭐", "💎"]
    sonuc = [random.choice(semboller) for _ in range(3)]

    kullanici["gumus"] -= miktar

    if sonuc[0] == sonuc[1] == sonuc[2]:
        odeme = miktar * 2
        kullanici["gumus"] += odeme

        mesaj = (
            f"{' | '.join(sonuc)}\n\n"
            f"🎉 **3'lü eşleşme!**\n"
            f"💰 Kazanç: **{sayi_yaz(miktar)} Gümüş**"
        )

    elif sonuc[0] == sonuc[1] or sonuc[0] == sonuc[2] or sonuc[1] == sonuc[2]:
        odeme = int(miktar * 1.5)
        kullanici["gumus"] += odeme

        mesaj = (
            f"{' | '.join(sonuc)}\n\n"
            f"✨ **2'li eşleşme!**\n"
            f"💰 Kazanç: **{sayi_yaz(odeme)} Gümüş**"
        )

    else:
        mesaj = (
            f"{' | '.join(sonuc)}\n\n"
            f"❌ Eşleşme yok.\n"
            f"💸 **{sayi_yaz(miktar)} Gümüş** kaybettin."
        )

    verileri_kaydet(veriler)
    await ctx.send(mesaj)


@bot.command()
async def slot(ctx, miktar: str = None):

    if miktar is None:
        await ctx.send("❌ Kullanım: `s.slot 500` veya `s.slot all`")
        return

    await slot_oyna(ctx, miktar)


@bot.command()
async def s(ctx, miktar: str = None):

    if miktar is None:
        await ctx.send("❌ Kullanım: `s.s 500` veya `s.s all`")
        return

    await slot_oyna(ctx, miktar)


# =========================
# MADEN
# =========================

@bot.command()
async def maden(ctx):

    kullanici = kullanici_olustur(ctx.author.id)

    kazma_kodu = kullanici["kazma"]

    if kazma_kodu not in KAZMALAR:
        kazma_kodu = 1
        kullanici["kazma"] = 1
        kullanici["kazma_kullanim"] = 100

    kazma = KAZMALAR[kazma_kodu]

    if kullanici["kazma_kullanim"] <= 0:
        await ctx.send(
            f"❌ Kazmanın kullanım hakkı bitti.\n"
            f"⛏️ Mevcut kazman: {kazma['emoji']} **{kazma['ad']}**\n"
            f"🏪 Yeni kazma almak için `s.market`"
        )
        return

    havuz = MADEN_HAVUZLARI[kazma_kodu]

    # Kaç farklı cevher çıkacağını belirle
    adet = random.choices(
        [1, 2, 3],
        weights=[55, 35, 10]
    )[0]

    bulunanlar = {}

    for _ in range(adet):

        # Kraliyet Kazması özel nadirlik sistemi
        if kazma_kodu == 20:

            sans = random.random()

            if sans < 0.01:
                secilen = "kraliyet cevheri"

            elif sans < 0.06:
                secilen = "efsane cevher"

            else:
                secilen = random.choice(havuz[:-2])

        else:
            secilen = random.choice(havuz)

        bulunanlar[secilen] = bulunanlar.get(secilen, 0) + 1

    # Kazma kullan
    kullanici["kazma_kullanim"] -= 1
    kullanici["maden_sayisi"] += 1
    kullanici["toplam_cevher"] += adet

    toplam_deger = 0
    mesaj_satiri = []

    for isim, miktar in bulunanlar.items():

        cevher = CEVHERLER[isim]

        kullanici["cevherler"][isim] = (
            kullanici["cevherler"].get(isim, 0) + miktar
        )

        toplam_deger += cevher["fiyat"] * miktar

        mesaj_satiri.append(
            f'{cevher["emoji"]} {cevher["ad"]} ×{miktar}'
        )

    # En değerli bulunan cevheri kaydet
    en_degerli = max(
        bulunanlar.keys(),
        key=lambda x: CEVHERLER[x]["fiyat"]
    )

    kullanici["en_degerli_cevher"] = CEVHERLER[en_degerli]["ad"]

    verileri_kaydet(veriler)

    mesaj = (
        "⛏️ **MADEN**\n\n"
        "Kazmanla kayaları kazdın...\n\n"
        "✨ **Buldukların:**\n"
        + "\n".join(mesaj_satiri)
        + "\n\n"
        f"💰 Bulunan cevherlerin toplam değeri: "
        f"**{sayi_yaz(toplam_deger)} Gümüş**\n\n"
        f"⛏️ Kullandığın kazma: "
        f"{kazma['emoji']} **{kazma['ad']}**\n"
        f"🔨 Kalan kullanım: **{kullanici['kazma_kullanim']}**"
    )

    await ctx.send(mesaj)


# =========================
# ENVANTER
# =========================

@bot.command()
async def envanter(ctx):

    kullanici = kullanici_olustur(ctx.author.id)

    bulunan = []

    for isim, miktar in kullanici["cevherler"].items():

        if miktar <= 0:
            continue

        if isim not in CEVHERLER:
            continue

        cevher = CEVHERLER[isim]

        bulunan.append(
            (
                cevher["fiyat"],
                f'{cevher["emoji"]} **{cevher["ad"]}** ×{miktar}'
            )
        )

    if not bulunan:
        await ctx.send(
            "🎒 **ENVANTER**\n\n"
            "Envanterin şu anda boş."
        )
        return

    bulunan.sort(reverse=True)

    mesaj = "🎒 **ENVANTER**\n\n"

    for _, satir in bulunan:
        mesaj += satir + "\n"

    await ctx.send(mesaj)


# =========================
# MARKET
# =========================

@bot.command()
async def market(ctx):

    mesaj = "🏪 **KAZMA MARKETİ**\n\n"

    for kod, kazma in KAZMALAR.items():

        if kazma["fiyat"] == 0:
            fiyat = "Ücretsiz"
        else:
            fiyat = f"{sayi_yaz(kazma['fiyat'])} Gümüş"

        mesaj += (
            f"**{kod:02d}.** "
            f"{kazma['emoji']} **{kazma['ad']}** "
            f"— {fiyat}\n"
        )

    mesaj += (
        "\n🛒 **Kazma almak için:**\n"
        "`s.al <kod>`\n\n"
        "Örnek: `s.al 10`"
    )

    await ctx.send(mesaj)


# =========================
# KAZMA AL
# =========================

@bot.command()
async def al(ctx, kod: int = None):

    if kod is None:
        await ctx.send(
            "❌ Bir kazma kodu yazmalısın.\n"
            "Örnek: `s.al 10`"
        )
        return

    if kod not in KAZMALAR:
        await ctx.send("❌ Geçersiz kazma kodu.")
        return

    kullanici = kullanici_olustur(ctx.author.id)
    kazma = KAZMALAR[kod]

    mevcut_kazma = kullanici["kazma"]

    if kod == mevcut_kazma:
        await ctx.send(
            f"❌ Zaten {kazma['emoji']} **{kazma['ad']}** kullanıyorsun."
        )
        return

    if kod < mevcut_kazma:
        await ctx.send(
            "❌ Zaten bundan daha yüksek seviyeli bir kazman var."
        )
        return

    if kullanici["gumus"] < kazma["fiyat"]:
        eksik = kazma["fiyat"] - kullanici["gumus"]

        await ctx.send(
            f"❌ Yeterli Gümüşün yok.\n"
            f"💰 Gereken: **{sayi_yaz(kazma['fiyat'])} Gümüş**\n"
            f"💸 Eksik: **{sayi_yaz(eksik)} Gümüş**"
        )
        return

    kullanici["gumus"] -= kazma["fiyat"]
    kullanici["kazma"] = kod
    kullanici["kazma_kullanim"] = kazma["kullanim"]

    verileri_kaydet(veriler)

    await ctx.send(
        f"✅ {kazma['emoji']} **{kazma['ad']}** satın alındı!\n\n"
        f"🔨 Kullanım: **{kazma['kullanim']}**\n"
        f"💰 Kalan Gümüş: **{sayi_yaz(kullanici['gumus'])}**"
    )


# =========================
# KAZMA BİLGİ
# =========================

@bot.command()
async def kazma(ctx):

    kullanici = kullanici_olustur(ctx.author.id)

    kod = kullanici["kazma"]
    kazma = KAZMALAR[kod]

    await ctx.send(
        "⛏️ **KAZMA BİLGİSİ**\n\n"
        f"{kazma['emoji']} **{kazma['ad']}**\n"
        f"🔨 Kalan kullanım: **{kullanici['kazma_kullanim']}**\n"
        f"🔢 Kod: **{kod:02d}**"
    )


# =========================
# CEVHER SAT
# =========================

@bot.command()
async def sat(ctx, *args):

    kullanici = kullanici_olustur(ctx.author.id)

    if len(args) == 0:
        await ctx.send(
            "💰 **CEVHER SATIŞI**\n\n"
            "`s.sat all` → Tüm cevherleri satar.\n"
            "`s.sat demir` → Belirli bir cevheri satar.\n\n"
            "Örnek:\n"
            "`s.sat kömür`\n"
            "`s.sat altın`"
        )
        return

    hedef = " ".join(args).lower()

    # Hepsini sat
    if hedef == "all":

        toplam = 0
        satilan = []

        for isim, miktar in list(kullanici["cevherler"].items()):

            if miktar <= 0:
                continue

            if isim not in CEVHERLER:
                continue

            cevher = CEVHERLER[isim]
            kazanc = cevher["fiyat"] * miktar

            toplam += kazanc

            satilan.append(
                f"{cevher['emoji']} {cevher['ad']} ×{miktar}"
            )

            kullanici["cevherler"][isim] = 0

        if toplam == 0:
            await ctx.send("❌ Satacak cevherin yok.")
            return

        kullanici["gumus"] += toplam

        verileri_kaydet(veriler)

        await ctx.send(
            "💰 **TÜM CEVHERLER SATILDI!**\n\n"
            + "\n".join(satilan)
            + "\n\n"
            f"💵 Kazanç: **{sayi_yaz(toplam)} Gümüş**"
        )
        return

    # Belirli cevheri sat
    if hedef not in CEVHERLER:

        await ctx.send(
            "❌ Böyle bir cevher bulunamadı.\n"
            "Örnek: `s.sat demir`"
        )
        return

    miktar = kullanici["cevherler"].get(hedef, 0)

    if miktar <= 0:
        await ctx.send(
            f"❌ Envanterinde **{CEVHERLER[hedef]['ad']}** yok."
        )
        return

    cevher = CEVHERLER[hedef]
    kazanc = miktar * cevher["fiyat"]

    kullanici["cevherler"][hedef] = 0
    kullanici["gumus"] += kazanc

    verileri_kaydet(veriler)

    await ctx.send(
        f"💰 {cevher['emoji']} **{cevher['ad']} ×{miktar}** satıldı.\n"
        f"💵 Kazanç: **{sayi_yaz(kazanc)} Gümüş**"
    )


# =========================
# PROFİL
# =========================

@bot.command()
async def profil(ctx, uye: discord.Member = None):

    if uye is None:
        uye = ctx.author

    kullanici = kullanici_olustur(uye.id)
    kazma = KAZMALAR[kullanici["kazma"]]

    await ctx.send(
        f"👤 **{uye.display_name} PROFİLİ**\n\n"
        f"💰 Gümüş: **{sayi_yaz(kullanici['gumus'])}**\n"
        f"⛏️ Kazma: {kazma['emoji']} **{kazma['ad']}**\n"
        f"🔨 Kalan kullanım: **{kullanici['kazma_kullanim']}**\n"
        f"⛏️ Maden sayısı: **{kullanici['maden_sayisi']}**\n"
        f"🎒 Toplam bulunan cevher: **{kullanici['toplam_cevher']}**\n"
        f"✨ En değerli buluntu: "
        f"**{kullanici['en_degerli_cevher'] or 'Yok'}**"
    )


# =========================
# SIRALAMA
# =========================

@bot.command()
async def sıralama(ctx):

    liste = []

    for user_id, kullanici in veriler.items():

        try:
            miktar = kullanici.get("gumus", 0)
            liste.append((miktar, user_id))
        except:
            pass

    liste.sort(reverse=True)

    if not liste:
        await ctx.send("📊 Henüz sıralama oluşmadı.")
        return

    mesaj = "🏆 **GÜMÜŞ SIRALAMASI**\n\n"

    for sira, (miktar, user_id) in enumerate(liste[:10], 1):

        uye = ctx.guild.get_member(int(user_id))

        if uye:
            isim = uye.display_name
        else:
            isim = f"Kullanıcı {user_id}"

        mesaj += (
            f"**{sira}.** {isim} — "
            f"💰 **{sayi_yaz(miktar)} Gümüş**\n"
        )

    await ctx.send(mesaj)


# =========================
# BAŞARIMLAR
# =========================

@bot.command()
async def başarımlar(ctx):

    kullanici = kullanici_olustur(ctx.author.id)

    maden = kullanici["maden_sayisi"]
    toplam = kullanici["toplam_cevher"]

    basarimlar = []

    if maden >= 10:
        basarimlar.append("⛏️ İlk Kazılar — 10 kez maden kaz")

    if maden >= 100:
        basarimlar.append("⛏️ Maden İşçisi — 100 kez maden kaz")

    if maden >= 500:
        basarimlar.append("⛏️ Usta Madenci — 500 kez maden kaz")

    if toplam >= 100:
        basarimlar.append("🎒 Cevher Koleksiyoncusu — 100 cevher bul")

    if toplam >= 1000:
        basarimlar.append("💎 Büyük Koleksiyoncu — 1.000 cevher bul")

    if kullanici["en_degerli_cevher"] in [
        "Efsane Cevher",
        "Kraliyet Cevheri"
    ]:
        basarimlar.append("✨ Nadir Buluntu — Çok nadir cevher bul")

    if not basarimlar:
        mesaj = (
            "🏆 **BAŞARIMLAR**\n\n"
            "Henüz tamamladığın bir başarım yok."
        )
    else:
        mesaj = (
            "🏆 **BAŞARIMLAR**\n\n"
            + "\n".join(f"✅ {x}" for x in basarimlar)
        )

    await ctx.send(mesaj)


# =========================
# ADMIN PARA
# =========================

@bot.command()
async def adminpara(ctx, *args):

    if ctx.author.id != bot.owner_id:
        await ctx.send("❌ Bu komutu sadece bot sahibi kullanabilir.")
        return

    if len(args) == 1:

        try:
            miktar = int(args[0])
        except:
            await ctx.send("❌ Geçerli bir miktar yaz.")
            return

        hedef = ctx.author

    elif len(args) == 2:

        try:
            hedef = await commands.MemberConverter().convert(ctx, args[0])
            miktar = int(args[1])
        except:
            await ctx.send(
                "❌ Kullanım: `s.adminpara miktar`\n"
                "veya `s.adminpara @kişi miktar`"
            )
            return

    else:
        await ctx.send(
            "❌ Kullanım:\n"
            "`s.adminpara 100000`\n"
            "`s.adminpara @kişi 100000`"
        )
        return

    if miktar <= 0:
        await ctx.send("❌ Miktar 0'dan büyük olmalı.")
        return

    kullanici = kullanici_olustur(hedef.id)
    kullanici["gumus"] += miktar

    verileri_kaydet(veriler)

    await ctx.send(
        f"🔐 **Admin işlemi başarılı.**\n"
        f"👤 {hedef.display_name}\n"
        f"💰 +**{sayi_yaz(miktar)} Gümüş**"
    )


# =========================
# ADMIN PARA SİL
# =========================

@bot.command()
async def adminsil(ctx, uye: discord.Member = None, miktar: str = None):

    if ctx.author.id != bot.owner_id:
        await ctx.send("❌ Bu komutu sadece bot sahibi kullanabilir.")
        return

    if uye is None or miktar is None:
        await ctx.send(
            "❌ Kullanım:\n"
            "`s.adminsil @kişi 5000`\n"
            "`s.adminsil @kişi all`"
        )
        return

    kullanici = kullanici_olustur(uye.id)

    if miktar.lower() == "all":

        silinen = kullanici["gumus"]
        kullanici["gumus"] = 0

    else:

        try:
            silinen = int(miktar)
        except:
            await ctx.send("❌ Geçerli bir miktar yaz.")
            return

        if silinen <= 0:
            await ctx.send("❌ Miktar 0'dan büyük olmalı.")
            return

        silinen = min(silinen, kullanici["gumus"])
        kullanici["gumus"] -= silinen

    verileri_kaydet(veriler)

    await ctx.send(
        f"🔐 **Admin işlemi başarılı.**\n"
        f"👤 {uye.display_name}\n"
        f"💸 Silinen: **{sayi_yaz(silinen)} Gümüş**"
    )


# =========================
# YARDIM
# =========================

@bot.command()
async def yardım(ctx):

    mesaj = """
📜 **SONERISTBOT KOMUTLARI**

💰 **EKONOMİ**
`s.bakiye` — Gümüş bakiyeni gösterir.
`s.para` — Gümüş bakiyeni gösterir.
`s.günlük` — Günlük Gümüşünü alırsın.
`s.gönder @kişi miktar` — Gümüş gönderirsin.

🎰 **OYUNLAR**
`s.cf miktar` — Yazı/tura oynar.
`s.cf yazı miktar` — Yazı seçerek oynar.
`s.cf tura miktar` — Tura seçerek oynar.
`s.cf all` — Uygun bakiyenle oynar.
`s.slot miktar` — Slot oynar.
`s.slot all` — Slotu uygun bakiyeyle oynar.
`s.s miktar` — Slot kısayolu.
`s.s all` — Slot kısayolu.

⛏️ **MADEN**
`s.maden` — Maden kazarsın.
`s.envanter` — Cevherlerini görürsün.
`s.market` — Kazma marketini görürsün.
`s.al kod` — Koduna göre kazma alırsın.
`s.kazma` — Kazmanı ve kalan kullanımını gösterir.
`s.sat` — Cevher satış bilgilerini gösterir.
`s.sat all` — Tüm cevherlerini satarsın.
`s.sat demir` — Belirli bir cevheri satarsın.

📊 **DİĞER**
`s.profil` — Profilini gösterir.
`s.sıralama` — Gümüş sıralamasını gösterir.
`s.başarımlar` — Başarımlarını gösterir.
`s.ping` — Botun pingini gösterir.
`s.yardım` — Bu komut listesini gösterir.

🔐 **ADMİN**
`s.adminpara miktar` — Kendine Gümüş ekler.
`s.adminpara @kişi miktar` — Kullanıcıya Gümüş ekler.
`s.adminsil @kişi miktar` — Kullanıcının Gümüşünü siler.
`s.adminsil @kişi all` — Kullanıcının tüm Gümüşünü siler.
"""

    await ctx.send(mesaj)


# =========================
# BOT HAZIR
# =========================

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")
    print("SoneristBOT aktif!")


# =========================
# TOKEN
# =========================

bot.run("")