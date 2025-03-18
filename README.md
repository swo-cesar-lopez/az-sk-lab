# Laboratorio de Integración Azure + Semantic Kernel

Este proyecto demuestra la integración entre Azure OpenAI, Semantic Kernel y CrewAI para crear aplicaciones potenciadas por IA con orquestación de agentes.

## Estructura del Proyecto

El repositorio está organizado en tres componentes principales:

### 1. `create_kernel`

Un ejemplo básico de uso de Semantic Kernel con Azure OpenAI, que demuestra:

- Configuración de un kernel con Azure OpenAI
- Uso de plugins nativos (TimePlugin)
- Generación de prompts e invocación de llamadas a la API

### 2. `sk_service`

Microservicio basado en FastAPI que implementa un orquestador utilizando Semantic Kernel:

- Expone un endpoint `/orchestrate` que coordina llamadas a otros servicios
- Demuestra cómo crear plugins personalizados para Semantic Kernel
- Manejo de errores y respuestas consistentes

### 3. `crew_ai_agents`

Implementación de agentes con CrewAI que pueden ejecutar tareas complejas:

- Define agentes (researcher, reporting_analyst)
- Configura tareas que pueden ser ejecutadas por los agentes
- Expone endpoints para ejecutar, entrenar y probar los agentes
- Permite reproducir ejecuciones anteriores mediante task_id

## Requisitos

- Python 3.10+
- Acceso a Azure OpenAI Service

## Configuración

Cada componente tiene su propio entorno virtual y requisitos específicos.

### Variables de Entorno

Crea un archivo `.env` en cada directorio de proyecto con las siguientes variables:

#### `create_kernel/.env`

```
AZURE_DEPLOYMENT_MODEL_NAME=your-deployment-name
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_KEY=your-api-key
```

#### `crew_ai_agents/.env`

```
OPENAI_API_KEY=your-openai-api-key
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=your-azure-endpoint
AZURE_OPENAI_API_VERSION=your-api-version
AZURE_DEPLOYMENT_NAME=your-deployment-name
```

## Instalación

### `create_kernel`

```bash
cd create_kernel
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### `sk_service`

```bash
cd sk_service
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn httpx semantic-kernel
```

### `crew_ai_agents`

```bash
cd crew_ai_agents
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Ejecución

### `create_kernel`

```bash
cd create_kernel
python main.py
```

### `sk_service`

```bash
cd sk_service
uvicorn app:app --reload --port 8001
```

### `crew_ai_agents`

```bash
cd crew_ai_agents
uvicorn src.crew_ai_agents.app:app --reload --port 8000
```

## Uso

### Flujo de Orquestación

1. El usuario hace una solicitud al servicio de Semantic Kernel:

   ```bash
   curl -X POST "http://localhost:8001/orchestrate" -H "Content-Type: application/json" -d "{}"
   ```

2. Semantic Kernel coordina la ejecución de CrewAI:
   - El endpoint `/orchestrate` llama al servicio CrewAI en `http://localhost:8000/run`
   - CrewAI ejecuta los agentes y tareas configurados
   - El resultado se devuelve a través de Semantic Kernel

### Funcionalidades Adicionales

- **Ejecución de Agentes**: `POST /run` - Ejecuta el crew con inputs predefinidos
- **Entrenamiento**: `POST /train` - Entrena el crew con un número específico de iteraciones
- **Reproducción**: `POST /replay` - Reproduce una ejecución específica usando task_id
- **Pruebas**: `POST /test` - Prueba el crew con parámetros específicos

## Arquitectura

```
                         ┌────────────────┐
                         │    Usuario     │
                         └────────┬───────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────┐
│                Semantic Kernel                    │
│  ┌────────────────────────────────────────────┐  │
│  │             Orquestador (8001)             │  │
│  └─────────────────────┬──────────────────────┘  │
└─────────────────────────┼────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────┐
│                     CrewAI                        │
│  ┌────────────────────────────────────────────┐  │
│  │              Agentes (8000)                │  │
│  └────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────┘
```

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
