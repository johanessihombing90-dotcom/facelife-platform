from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="FaceLife+ Gen-AI Pro Backend")

# Mengaktifkan CORS agar Frontend (index.html) bisa berkomunikasi dengan Backend ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

# ==================== 1. DATABASE UTAMA SOSIAL MEDIA & MARKETPLACE ====================
feed_db = [
    {
        "id": 1,
        "username": "Andi Wijaya",
        "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150",
        "status": "Hari ini produktif sekali mencoba fitur FaceLife+ Gen-AI Pro! Keren banget hasilnya. ✨",
        "media_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600",
        "likes": 24
    },
    {
        "id": 2,
        "username": "Siti Rahma",
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
        "status": "Mencoba jualan produk lewat fitur Marketplace-nya. Semoga cepat laku keras! 🚀🛍️",
        "media_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600",
        "likes": 42
    }
]

market_db = [
    {
        "id": 1,
        "shop_name": "Sinar Jaya Tech",
        "product_name": "Mouse Gaming Logitech G502",
        "price": "Rp 850.000",
        "description": "Mouse gaming sensor HERO 25K berakurasi tinggi, RGB customizable, kondisi mulus 100% garansi resmi."
    },
    {
        "id": 2,
        "shop_name": "Fashion Horizon",
        "product_name": "Jaket Bomber Waterproof Pro",
        "price": "Rp 320.000",
        "description": "Bahan taslan premium tahan angin dan air, sangat cocok untuk dipakai berkendara malam atau musim hujan."
    }
]

# ==================== 2. ROUTE FITUR SOSIAL MEDIA & MARKETPLACE ====================
@app.get("/api/feed")
async def get_feed(): 
    return feed_db

@app.post("/api/feed/like/{feed_id}")
async def like_feed(feed_id: int):
    for post in feed_db:
        if post["id"] == feed_id:
            post["likes"] += 1
            return {"success": True, "likes": post["likes"]}
    return {"success": False, "message": "Post tidak ditemukan"}

@app.get("/api/market/products")
async def get_products(): 
    return market_db

@app.post("/api/market/products")
async def add_product(request: Request):
    body = await request.json()
    new_product = {
        "id": len(market_db) + 1,
        "shop_name": body.get("shop_name", "Toko Anonim"),
        "product_name": body.get("product_name", "Produk Tanpa Nama"),
        "price": body.get("price", "Hubungi Penjual"),
        "description": body.get("description", "")
    }
    market_db.insert(0, new_product)
    return {"success": True, "message": "Produk Anda berhasil diterbitkan ke pasar!"}

# ==================== 3. ROUTE ENGINE AI GENERATOR (FIXED) ====================
@app.post("/api/ai/image")
async def ai_image(data: PromptRequest):
    keyword = data.prompt.strip().lower()
    random_sig = random.randint(1, 1000)
    dynamic_url = f"https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&sig={random_sig}"
    
    if "ikan" in keyword or "fish" in keyword:
        dynamic_url = f"https://images.unsplash.com/photo-1524704659697-9f7500b70448?w=600&sig={random_sig}"
    elif "indonesia" in keyword:
        dynamic_url = f"https://images.unsplash.com/photo-1505993597083-3bd19f7c839b?w=600&sig={random_sig}"
    elif "mobil" in keyword or "car" in keyword:
        dynamic_url = f"https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&sig={random_sig}"
    elif "kucing" in keyword or "cat" in keyword:
        dynamic_url = f"https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&sig={random_sig}"
    return {"url": dynamic_url}

@app.post("/api/ai/text")
async def ai_text(data: PromptRequest):
    prompt_user = data.prompt.strip().lower()
    if "indonesia" in prompt_user:
        return {"data": "[FaceLife AI]: Indonesia terletak di Asia Tenggara, dilalui garis khatulistiwa dan berada di antara Benua Asia & Australia serta Samudra Pasifik & Hindia. Indonesia merupakan negara kepulauan terbesar di dunia!"}
    if "ikan" in prompt_user:
        return {"data": "[FaceLife AI]: Ikan adalah hewan vertebrata berdarah dingin yang hidup di air dan bernapas menggunakan insang. Untuk melihat visualisasinya, silakan tekan tombol 'Gambar' atau 'Video' di dashboard Anda."}
    
    responses = [
        f"Analisis AI FaceLife untuk '{data.prompt}': Konsep ini memiliki potensi keterlibatan (engagement) hingga 88%. Disarankan menggunakan pendekatan visual minimalis modern.",
        f"Menurut algoritma FaceLife+, topik '{data.prompt}' sedang naik tren di mesin pencarian. Sangat cocok untuk dijadikan pilar konten digital Anda minggu ini."
    ]
    return {"data": random.choice(responses)}

@app.post("/api/ai/video")
async def ai_video(data: PromptRequest):
    keyword = data.prompt.strip().lower()
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-abstract-laser-lights-background-41753-large.mp4"
    
    if "ikan" in keyword or "fish" in keyword or "laut" in keyword or "ocean" in keyword:
        video_url = "https://vjs.zencdn.net/v/oceans.mp4"
    elif "mobil" in keyword or "car" in keyword:
        video_url = "https://assets.mixkit.co/videos/preview/mixkit-sports-car-driving-on-a-highway-at-sunset-40243-large.mp4"
    elif "indonesia" in keyword or "alam" in keyword:
        video_url = "https://assets.mixkit.co/videos/preview/mixkit-waterfall-in-forest-2213-large.mp4"
    return {"url": video_url}

@app.post("/api/ai/suggest-description")
async def ai_suggest_desc(data: PromptRequest):
    product_name = data.prompt.strip()
    return {"suggestion": f"Dapatkan {product_name} kualitas premium terbaik hanya di toko kami! Produk 100% original, bergaransi resmi, paking ekstra aman, dan siap kirim ke seluruh Indonesia. Yuk, checkout sekarang!"}

# ==================== 4. ROUTE FITUR TOOLS QUICK EDITORS ====================
@app.post("/api/tools/edit-photo")
async def edit_photo(request: Request):
    return {"url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=600"}

@app.post("/api/tools/edit-video")
async def edit_video(request: Request):
    return {"url": "https://assets.mixkit.co/videos/preview/mixkit-waves-in-the-ocean-near-a-cliff-43187-large.mp4"}
