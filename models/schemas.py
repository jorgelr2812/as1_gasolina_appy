from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

class ConsumoGasolina(BaseModel):
    modelo: str | None = Field(min_length=2, max_length=50, description="Modelo de vehículo ( entre 2 y 50 caracteres )") 
    consumo_medio: float = Field(gt=0, description="Consumo medio de combustible en litros a los 100 km")
    capacidad_tanque: int = Field(gt=0, description="Capacidad del tanque ( Litros )")
    distancia_recorrida: int = Field(gt=0, description="Distancia en km")
    combustible_restante: int = Field(ge=0, description="Combustible restante en litros ( >= 0 )")
    precio_gasolina: float = Field(gt=0, description="Precio de la gasolina por litro ( mayor que 0 )")
    electrico: bool = Field(description="Indica si el vehículo es eléctrico o no")
    
class ResultadoGasolina(BaseModel):
    mensaje: str = Field(description="Resultado del cálculo")
    litros_consumidos: float = Field(description="Litros de combustible consumidos")
    litros_restantes: float = Field(description="Litros de combustible restantes")
    autonomia_restante: float = Field(description="Autonomía restante en km con el combustible restante")
    dinero_gastado: float = Field(description="Dinero gastado")
    veredicto: str = Field(description="Veredicto sobre si el vehículo puede completar el trayecto con el combustible restante")
    score_eficiencia: float = Field(description="Puntuación de eficiencia del vehículo basada en el consumo de combustible")