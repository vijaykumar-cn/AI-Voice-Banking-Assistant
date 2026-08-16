from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.customer import router as customer_router
from app.api.loan import router as loan_router
from app.api.ai import router as ai_router
from app.websocket.voice import router as voice_router
from fastapi.staticfiles import StaticFiles



app = FastAPI(
    title="Voice Bank AI",
    version="1.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)
app.include_router(loan_router)
app.include_router(ai_router)
app.include_router(voice_router)
app.mount("/audio", StaticFiles(directory="audio"), name="audio")


@app.get("/")
async def home():
    return {
        "message": "Voice Bank AI is running"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }