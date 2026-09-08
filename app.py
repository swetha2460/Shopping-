import json
import os
import re
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PORT = int(os.getenv("PORT", "8000"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

app = FastAPI(title="ShopMate AI Python API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

products = [
    {"id": "P1001", "name": "AeroFlex Running Shoes", "category": "Footwear", "price": 2499, "stock": 18, "rating": 4.6},
    {"id": "P1002", "name": "UrbanPulse Smart Watch", "category": "Wearables", "price": 3999, "stock": 7, "rating": 4.4},
    {"id": "P1003", "name": "SoundWave Pro Headphones", "category": "Audio", "price": 2999, "stock": 24, "rating": 4.7},
    {"id": "P1004", "name": "NovaFit Backpack", "category": "Bags", "price": 1599, "stock": 11, "rating": 4.5},
    {"id": "P1005", "name": "Lumina Desk Lamp", "category": "Home", "price": 1299, "stock": 32, "rating": 4.3},
    {"id": "P1006", "name": "TrailMark Everyday Sneakers", "category": "Footwear", "price": 2199, "stock": 14, "rating": 4.5},
    {"id": "P1007", "name": "CloudStep Recovery Slides", "category": "Footwear", "price": 899, "stock": 29, "rating": 4.2},
    {"id": "P1008", "name": "PulseBand Activity Tracker", "category": "Wearables", "price": 1899, "stock": 16, "rating": 4.3},
    {"id": "P1009", "name": "EchoBud Wireless Earbuds", "category": "Audio", "price": 1799, "stock": 21, "rating": 4.4},
    {"id": "P1010", "name": "QuietTone Desk Speakers", "category": "Audio", "price": 2499, "stock": 9, "rating": 4.6},
    {"id": "P1011", "name": "MetroCrossbody Bag", "category": "Bags", "price": 1199, "stock": 20, "rating": 4.1},
    {"id": "P1012", "name": "Atlas Travel Duffel", "category": "Bags", "price": 2799, "stock": 8, "rating": 4.5},
    {"id": "P1013", "name": "Hearth & Home Candle", "category": "Home", "price": 699, "stock": 40, "rating": 4.6},
    {"id": "P1014", "name": "Sora Ceramic Mug Set", "category": "Home", "price": 999, "stock": 26, "rating": 4.4},
    {"id": "P1015", "name": "FocusFlow Mechanical Keyboard", "category": "Tech", "price": 3499, "stock": 12, "rating": 4.7},
    {"id": "P1016", "name": "GlowMini Portable Charger", "category": "Tech", "price": 1499, "stock": 33, "rating": 4.3},
]

catalog_seeds = [
    ("Footwear", ["Harbor Knit Trainers", "StrideLite Court Shoes", "Peakline Walking Shoes", "Motive Trail Runners", "Everyday Canvas Sneakers", "Northstar Slip-On Shoes", "FlexForm Training Shoes", "Wayfarer Casual Loafers", "CloudRun Mesh Trainers", "RidgeWalk Hiking Shoes"], 1299),
    ("Wearables", ["HaloSleep Ring", "MoveMate Smart Band", "CoreTrack Fitness Watch", "Tempo Heart Monitor", "LoopLink Smart Ring", "Daylight Health Watch", "MotionPulse Band", "Orbit Mini Watch", "Balance Activity Band", "Venture GPS Watch"], 1599),
    ("Audio", ["StudioBloom Headphones", "PocketBeat Earbuds", "RoomTone Bluetooth Speaker", "WaveNest Over-Ear Headphones", "ClearCall Conference Buds", "Bassline Mini Speaker", "Drift Noise-Canceling Buds", "SoundArc Portable Speaker", "FocusPod Headphones", "Chime Wireless Earphones"], 999),
    ("Bags", ["Canvas Day Tote", "Summit Laptop Bag", "Daybreak Sling Bag", "Fieldwork Messenger", "CarryOn Weekender", "Willow Mini Backpack", "Transit Laptop Sleeve", "Coastline Beach Tote", "Rover Gym Bag", "Lumen Travel Organizer"], 799),
    ("Home", ["CalmGlow Table Lamp", "Woven Throw Blanket", "Cedar Room Diffuser", "Mellow Stone Vase", "Morning Brew Kettle", "Softline Cushion Set", "Arc Wall Clock", "Linen Storage Basket", "Stillwater Water Bottle", "Kindred Photo Frame"], 599),
    ("Tech", ["KeyNest Wireless Keyboard", "BrightPoint USB Hub", "PocketPixel Webcam", "SwiftCharge Wall Adapter", "DeskDock Laptop Stand", "LinkLoop USB-C Cable", "AeroNote Tablet Sleeve", "BeamLite Monitor Light", "GridPad Desk Mat", "Signal Bluetooth Adapter"], 699),
    ("Beauty", ["Dewdrop Face Mist", "Velvet Tint Lip Balm", "CloudSilk Hand Cream", "GlowKind Body Lotion", "FreshStart Cleansing Gel", "Moonlit Hair Serum", "PetalSoft Bath Salts", "BareBloom Face Mask", "Citrus Grove Hand Wash", "QuietMorning Eye Gel"], 399),
    ("Stationery", ["Everyday Hardcover Journal", "Studio Grid Notebook", "SoftMark Gel Pen Set", "Desk Day Planner", "Archive Document Folder", "ColorStory Marker Set", "Pocket Notes Pack", "FineLine Drawing Pencils", "Weekly Focus Pad", "PaperCraft Card Set"], 249),
    ("Kitchen", ["Oakridge Cutting Board", "Savor Glass Storage Set", "Daily Pour Water Jug", "Moss Ceramic Plate Set", "BrewBar Coffee Press", "Gather Serving Bowl", "SpiceTrail Jar Set", "EasyPrep Measuring Cups", "Harvest Cotton Apron", "Stoneware Snack Tray"], 449),
    ("Fitness", ["CoreGrip Yoga Mat", "LiftLoop Resistance Bands", "Stride Foam Roller", "Balance Cork Block Set", "Pulse Jump Rope", "TrainWell Water Bottle", "FlexFit Ankle Weights", "Recovery Massage Ball", "MoveDaily Exercise Towel", "FormFit Training Gloves"], 499),
]

generated_product_number = 1017
for category, names, base_price in catalog_seeds:
    for index, name in enumerate(names):
        products.append({
            "id": f"P{generated_product_number}",
            "name": name,
            "category": category,
            "price": base_price + (index % 5) * 200,
            "stock": 6 + ((index * 7) % 35),
            "rating": round(4.1 + ((index * 3) % 8) / 10, 1),
        })
        generated_product_number += 1

orders = {
    "ORD1001": {"id": "ORD1001", "item": "AeroFlex Running Shoes", "status": "Out for delivery", "eta": "Today, 7 PM", "amount": 2499},
    "ORD1002": {"id": "ORD1002", "item": "SoundWave Pro Headphones", "status": "Shipped", "eta": "Tomorrow", "amount": 2999},
    "ORD1003": {"id": "ORD1003", "item": "NovaFit Backpack", "status": "Delivered", "eta": "Delivered yesterday", "amount": 1599},
}
memory: dict[str, list[dict[str, str]]] = {}

class ChatRequest(BaseModel):
    sessionId: str = "default"
    message: str


def search_products(query: str) -> list[dict[str, Any]]:
    text = query.lower()
    budget_match = re.search(r"(?:under|below|less than)\s*(?:₹|rs\.?\s*)?(\d[\d,]*)", text)
    max_price = int(budget_match.group(1).replace(",", "")) if budget_match else None
    cleaned = re.sub(r"(?:under|below|less than)\s*(?:₹|rs\.?\s*)?\d[\d,]*", "", text)
    cleaned = re.sub(r"\b(find|show|search|product|products|please|me|a|for)\b", " ", cleaned)
    cleaned = " ".join(cleaned.split())
    matches = [product for product in products if cleaned in f"{product['name']} {product['category']}".lower()]
    if max_price is not None:
        matches = [product for product in matches if product["price"] <= max_price]
    return matches[:5]


def recommend_products(preferences: str) -> list[dict[str, Any]]:
    text = preferences.lower()
    selected = products[:]
    categories = {
        "audio": "Audio", "music": "Audio", "headphone": "Audio", "shoe": "Footwear", "run": "Footwear",
        "watch": "Wearables", "fitness": "Wearables", "travel": "Bags", "commute": "Tech", "home": "Home",
    }
    for keyword, category in categories.items():
        if keyword in text:
            selected = [product for product in selected if product["category"] == category]
            break
    budget = re.search(r"(?:under|below|less than)\s*(?:₹|rs\.?\s*)?(\d[\d,]*)", text)
    if budget:
        selected = [product for product in selected if product["price"] <= int(budget.group(1).replace(",", ""))]
    return sorted(selected, key=lambda product: product["rating"], reverse=True)[:3]


def offline_reply(message: str) -> str:
    text = message.lower()
    order_id = re.search(r"ord\d+", text)
    if order_id or "track" in text or "order status" in text:
        order = orders.get(order_id.group(0).upper()) if order_id else None
        return f"{order['id']} is {order['status']}. Estimated arrival: {order['eta']}." if order else "I can track ORD1001, ORD1002, or ORD1003."
    if "return" in text or "refund" in text:
        return "Our demo policy allows unused items to be returned within 30 days. This demo does not process refunds."
    if any(word in text for word in ("recommend", "suggest", "best for")):
        return "Recommendations: " + "; ".join(f"{p['name']} - INR {p['price']:,}" for p in recommend_products(message))
    results = search_products(message)
    if results:
        return "I found: " + "; ".join(f"{p['name']} - INR {p['price']:,}" for p in results)
    return "I can help find products, recommend items, track orders, or explain returns."


def return_policy() -> dict[str, Any]:
    return {"window_days": 30, "condition": "Items should be unused", "refund_note": "This demo does not process refunds"}


def run_tool(action: str, args: dict[str, Any]) -> dict[str, Any] | None:
    if action == "search_products":
        return {"tool": action, "results": search_products(str(args.get("query", "")))}
    if action == "track_order":
        order_id = str(args.get("order_id", "")).upper()
        return {"tool": action, "order": orders.get(order_id)}
    if action == "recommend_products":
        return {"tool": action, "results": recommend_products(str(args.get("preferences", "")))}
    if action == "return_policy":
        return {"tool": action, "policy": return_policy()}
    return None


def extract_action(text: str) -> dict[str, Any] | None:
    try:
        candidate = json.loads(text)
        return candidate if isinstance(candidate, dict) else None
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None
        try:
            candidate = json.loads(match.group(0))
            return candidate if isinstance(candidate, dict) else None
        except json.JSONDecodeError:
            return None


def remember(session_id: str, role: str, content: str) -> None:
    history = memory.setdefault(session_id, [])
    history.append({"role": role, "content": content})
    del history[:-12]


async def ollama_chat(messages: list[dict[str, str]]) -> str:
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(f"{OLLAMA_URL}/api/chat", json={"model": OLLAMA_MODEL, "messages": messages, "stream": False, "options": {"temperature": 0.2}})
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")


@app.get("/api/config")
async def config() -> dict[str, str]:
    return {"model": OLLAMA_MODEL, "ollamaUrl": OLLAMA_URL, "backend": "python"}

@app.get("/api/products")
async def get_products() -> list[dict[str, Any]]:
    return products

@app.post("/api/chat")
async def chat(request: ChatRequest) -> dict[str, Any]:
    message = request.message.strip()
    if not message:
        return {"error": "Message is required."}
    remember(request.sessionId, "user", message)
    prompt = """You are ShopMate AI, a concise and friendly ecommerce agent.
Use tools whenever the user asks to search products, track an order, get recommendations, or ask about returns.
When a tool is needed, output ONLY JSON in this format:
{"action":"search_products|track_order|recommend_products|return_policy","args":{}}
Use search_products args {"query":"..."}; track_order args {"order_id":"ORD1001"}; recommend_products args {"preferences":"..."}; return_policy args {}.
Never invent prices, stock, order status, or policy facts. For a normal conversation, answer directly.
Catalog:\n""" + json.dumps(products)
    try:
        messages = [{"role": "system", "content": prompt}, *memory[request.sessionId][-8:]]
        draft = await ollama_chat(messages)
        action = extract_action(draft)
        tool_result = run_tool(str(action.get("action")), action.get("args", {})) if action and action.get("action") else None
        if tool_result:
            reply = await ollama_chat([
                *messages,
                {"role": "assistant", "content": json.dumps(action)},
                {"role": "user", "content": f"Tool result: {json.dumps(tool_result)}. Answer the customer directly. Do not mention internal tools."},
            ])
            remember(request.sessionId, "assistant", reply)
            return {"reply": reply, "mode": "ollama", "tool": tool_result["tool"], "data": tool_result}
        reply = draft
        remember(request.sessionId, "assistant", reply)
        return {"reply": reply, "mode": "ollama"}
    except Exception:
        reply = offline_reply(message)
        remember(request.sessionId, "assistant", reply)
        return {"reply": reply, "mode": "offline", "hint": f"Install the Ollama model '{OLLAMA_MODEL}' for richer answers."}

@app.post("/api/reset")
async def reset(request: dict[str, str]) -> dict[str, bool]:
    memory.pop(request.get("sessionId", "default"), None)
    return {"ok": True}

app.mount("/", StaticFiles(directory="public", html=True), name="public")
