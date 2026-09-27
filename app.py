import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agente Afiliado Backend", version="1.0.0")

origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE = {
    "agent_active": False,
    "hunter_running": False,
    "mercado_livre_connected": False,
    "products": [],
    "activity": [],
}

def now_iso():
    return datetime.now(timezone.utc).isoformat()

@app.get("/")
def root():
    return {"service": "agente-afiliado-backend", "status": "online"}

@app.get("/health")
def health():
    return {"status": "ok", "time": now_iso()}

@app.get("/dashboard")
def dashboard():
    return {
        "products": len(STATE["products"]),
        "clicks": 0,
        "orders": 0,
        "earnings": 0.0,
        "conversion": 0.0,
        "agent_active": STATE["agent_active"],
        "mercado_livre_connected": STATE["mercado_livre_connected"],
    }

@app.get("/products")
def products():
    return STATE["products"]

@app.get("/activity")
def activity():
    return STATE["activity"][-100:]

@app.get("/agent")
def agent_status():
    return {"active": STATE["agent_active"]}

@app.post("/agent")
def set_agent(active: bool):
    STATE["agent_active"] = active
    STATE["activity"].append({"type": "agent", "active": active, "time": now_iso()})
    return {"active": active}

@app.get("/hunter/status")
def hunter_status():
    return {
        "running": STATE["hunter_running"],
        "mercado_livre_connected": STATE["mercado_livre_connected"],
    }

@app.post("/hunter/run")
def hunter_run():
    if not STATE["mercado_livre_connected"]:
        raise HTTPException(status_code=409, detail="Mercado Livre ainda não está conectado.")
    STATE["hunter_running"] = True
    STATE["activity"].append({"type": "hunter", "status": "started", "time": now_iso()})
    return {"ok": True, "message": "Caçador iniciado."}

@app.get("/auth/mercadolivre")
def mercado_livre_auth_placeholder():
    return {
        "status": "pending_configuration",
        "message": "OAuth do Mercado Livre será ativado após configurar CLIENT_ID, CLIENT_SECRET e REDIRECT_URI no Render.",
        "pkce": "S256",
    }
