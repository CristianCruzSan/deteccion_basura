from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import shutil
import uuid
import os

app = FastAPI()

# Montar carpetas estáticas y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Cargar modelo YOLO
model = YOLO("best.pt")  # tu modelo aquí

# Carpeta temporal para uploads
os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Guardar imagen temporalmente
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Hacer predicción
    results = model(file_path)
    detecciones = []

    for r in results:
        for box in r.boxes:
            clase = model.names[int(box.cls)]
            confianza = float(box.conf)
            detecciones.append({
                "clase": clase,
                "confianza": round(confianza, 2)
            })

    # Borrar imagen temporal
    os.remove(file_path)

    return JSONResponse(content={"detecciones": detecciones})
