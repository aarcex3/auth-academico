from fastapi import FastAPI
import models
from database import engine
from routes import router
import uvicorn
# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the API routes
app.include_router(router)


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)