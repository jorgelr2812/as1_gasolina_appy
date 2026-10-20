from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models.schemas import ConsumoGasolina, ResultadoGasolina


app = FastAPI(
    title="Calculo de Consumo de Gasolina",
    description="API para calcular el consumo de gasolina, litros restantes, autonomía y dinero gastado en un trayecto.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
def inicio():
    return FileResponse("index.html")

@app.get("/api/v1/status", summary="Estado del servicio")
def get_status():
    """Ruta informativa que devuelve en formato JSON el estado del servicio y detalles de consulta."""
    return {
        "service_name": "API de Cálculo de Consumo de Gasolina e Inferencia de Trayecto",
        "status": "online",
        "version": "1.0.0",
        "endpoints_disponibles": {
            "GET /api/v1/status": "Estado del servicio",
            "POST /api/v1/calcular": "Endpoint de inferencia y evaluación del modelo"
        }
    }

@app.post("/api/v1/calcular", response_model=ResultadoGasolina)
def calcular_consumo_gasolina(consumo: ConsumoGasolina):
    litros_consumidos = (consumo.consumo_medio / 100) * consumo.distancia_recorrida
    dinero_gastado = litros_consumidos * consumo.precio_gasolina

    if consumo.electrico:
        litros_consumidos = 0
        litros_restantes = consumo.combustible_restante
        autonomia_restante = None
        dinero_gastado = 0.0
        veredicto = "vehiculo_electrico"
        mensaje = "Vehículo eléctrico: no se consume gasolina en este trayecto."
    else:
        combustible_insuficiente = litros_consumidos > consumo.combustible_restante
        litros_restantes = max(consumo.combustible_restante - litros_consumidos, 0)
        autonomia_restante = round((litros_restantes / consumo.consumo_medio) * 100, 2) if consumo.consumo_medio > 0 else 0.0        
        veredicto = (
            "combustible_insuficiente"
            if combustible_insuficiente
            else "combustible_suficiente"
        )
        mensaje = (
            "El combustible disponible no cubre el consumo estimado del trayecto."
            if combustible_insuficiente
            else "El combustible disponible cubre el consumo estimado del trayecto."
        )
    if consumo.electrico:
        score_eficiencia = 100.0
    else:
        margen = consumo.combustible_restante - litros_consumidos
        if margen < 0:
            score_eficiencia = 0.0
        else:
            score_eficiencia = min(100.0, round((margen / consumo.capacidad_tanque) * 100, 1))
    return ResultadoGasolina(
        veredicto=veredicto,
        mensaje=mensaje,
        litros_consumidos=litros_consumidos,
        litros_restantes=litros_restantes,
        autonomia_restante=autonomia_restante,
        dinero_gastado=dinero_gastado,
        score_eficiencia=score_eficiencia
    )

