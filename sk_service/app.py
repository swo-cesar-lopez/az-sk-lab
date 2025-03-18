from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import traceback
import json
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

app = FastAPI(title="Semantic Kernel Orchestrator API")

# URL del endpoint del agente expuesto por el otro servicio
AGENT_RUN_URL = "http://localhost:8000/run"

# Modelo de solicitud para la orquestación
class OrchestrateRequest(BaseModel):
    pass

# Modelo de respuesta para asegurar que sea serializable
class OrchestrateResponse(BaseModel):
    result: str

# Definir un plugin de Semantic Kernel para orquestar la llamada al agente
class CrewAIOrchestrator:
    @kernel_function(description="Orquesta la ejecución del agente CrewAI llamando al endpoint /run")
    async def orchestrate(self) -> str:
        try:
            print(f"Iniciando llamada al agente en {AGENT_RUN_URL}")
            async with httpx.AsyncClient(timeout=30.0) as client:
                print("Enviando solicitud...")
                response = await client.post(AGENT_RUN_URL)
                print(f"Respuesta recibida con status code: {response.status_code}")
                print(f"Contenido de la respuesta: {response.text}")
                response.raise_for_status()
                
                # Convertir la respuesta JSON a un diccionario y luego a una cadena JSON formateada
                try:
                    response_data = response.json()
                    print(f"Respuesta JSON parseada: {response_data}")
                    return json.dumps(response_data)
                except json.JSONDecodeError as json_err:
                    error_msg = f"Error al decodificar JSON: {str(json_err)}. Contenido: {response.text}"
                    print(error_msg)
                    return error_msg
        except httpx.RequestError as req_err:
            error_msg = f"Error en la solicitud HTTP: {str(req_err)}"
            print(f"Error detallado: {error_msg}\n{traceback.format_exc()}")
            return error_msg
        except Exception as e:
            error_msg = f"Error al llamar al agente: {str(e)}"
            print(f"Error detallado: {error_msg}\n{traceback.format_exc()}")
            return error_msg

# Inicializar el kernel e importar el plugin
kernel = Kernel()
orchestrator_plugin = CrewAIOrchestrator()
kernel.add_plugin(orchestrator_plugin, "orchestrator")

# Endpoint de FastAPI para orquestar el agente mediante Semantic Kernel
@app.post("/orchestrate", response_model=OrchestrateResponse)
async def orchestrate_endpoint(request: OrchestrateRequest):
    try:
        # Obtener la función del plugin
        plugin = kernel.plugins["orchestrator"]
        # Invocar la función pasando el kernel como argumento
        result = await plugin["orchestrate"].invoke(kernel=kernel)
        
        # Asegurarse de que el resultado sea serializable
        if not isinstance(result, str):
            result = str(result)
            
        return OrchestrateResponse(result=result)
    except Exception as e:
        error_detail = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)  # Imprimir el error completo en los logs
        raise HTTPException(status_code=500, detail=error_detail)
