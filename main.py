from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, stocks, news, strategy, trades
from database import Base, engine

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(stocks.router, prefix="/stocks", tags=["Stock Data"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(strategy.router, prefix="/strategy", tags=["AI Strategies"])
app.include_router(trades.router, prefix="/trades", tags=["Trade Execution"])

@app.get("/")
def read_root():
    return {"message": "Hello Guru - Stock Trading AI Backend"}
