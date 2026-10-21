# API de cálculo de consumo de gasolina

## Descripción de la aplicación

Esta aplicación web permite estimar el combustible que consume un vehículo durante un trayecto, el combustible que queda en el depósito, la autonomía restante y el coste del viaje. También indica si el combustible disponible es suficiente y calcula una puntuación de eficiencia.

El servicio está implementado con FastAPI. La interfaz web envía los datos del formulario a la API de forma asíncrona y muestra el resultado sin recargar la página. El cálculo se basa en los datos introducidos; no se utiliza un modelo de inteligencia artificial entrenado.

## URL pública

**Aplicación desplegada en Render:** [https://as1-gasolina-appy-kthz.onrender.com](https://as1-gasolina-appy-kthz.onrender.com).

## Plataforma de despliegue

**Render** (despliegue web de Python).

## API

- `GET /`: muestra el formulario web.
- `GET /api/v1/status`: devuelve el estado y la versión del servicio.
- `POST /api/v1/calcular`: calcula el resultado del trayecto.
- `GET /docs`: documentación interactiva de FastAPI.

Ejemplo de petición a `POST /api/v1/calcular`:

```json
{
  "modelo": "Seat Leon",
  "consumo_medio": 6.5,
  "capacidad_tanque": 50,
  "distancia_recorrida": 350,
  "combustible_restante": 40,
  "precio_gasolina": 1.65,
  "electrico": false
}
```

Los campos numéricos deben ser positivos, salvo `combustible_restante`, que admite cero. La respuesta incluye el veredicto, un mensaje explicativo, los litros consumidos y restantes, la autonomía restante, el coste estimado y la puntuación de eficiencia.

## Ejecución local

Desde la carpeta `as1_gasolina_appy`:

1. Crea y activa un entorno virtual.
2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicia el servidor:

   ```bash
   uvicorn app:app --reload
   ```

4. Abre `http://127.0.0.1:8000`. La documentación de la API está en `http://127.0.0.1:8000/docs`.

## Despliegue en Render

Estos pasos permiten desplegar el servicio desde un repositorio GitHub:

1. Comprueba que el repositorio contiene `app.py`, `index.html`, la carpeta `static`, la carpeta `models` y `requirements.txt`.
2. Inicia sesión en [Render](https://render.com/) y selecciona **New +** → **Web Service**.
3. Conecta la cuenta de GitHub y selecciona el repositorio que contiene el proyecto.
4. Configura el servicio:
   - **Name**: el nombre que quieras para el servicio; formará parte de la URL pública.
   - **Branch**: la rama que quieres desplegar, normalmente `main`.
   - **Root Directory**: `as1_gasolina_appy` si el proyecto está dentro de un repositorio que contiene más carpetas. Déjalo vacío si el repositorio es directamente esta carpeta.
   - **Runtime**: `Python 3`.
   - **Build Command**: `pip install -r requirements.txt`.
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`.
5. Selecciona **Create Web Service** y espera a que Render instale las dependencias e inicie la aplicación.
6. Cuando el despliegue aparezca como correcto, abre la URL `onrender.com` que muestra Render. Comprueba la página principal, `/api/v1/status` y `/docs`, y sustituye en este README el enlace pendiente por la URL asignada.
7. Para publicar cambios posteriores, súbelos a la rama conectada. Render volverá a desplegar el servicio automáticamente si está activada la opción de despliegue automático.

Si el repositorio usa una carpeta raíz distinta, ajusta **Root Directory** para que apunte a la carpeta donde están `app.py` y `requirements.txt`. No añadas secretos: esta aplicación no requiere variables de entorno propias.


