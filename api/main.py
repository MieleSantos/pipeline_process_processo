from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="Api to process PDF files",
    description="API to process/extrarct data from PDF files",
    version="0.1.0",
)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
