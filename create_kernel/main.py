import asyncio
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.core_plugins.time_plugin import TimePlugin

load_dotenv()


# 🔹 1️⃣ Cargar y validar configuración con Pydantic
class ConfigSettings(BaseModel):
    azure_deployment_model_name: str = os.environ.get("AZURE_DEPLOYMENT_MODEL_NAME", "")
    azure_openai_endpoint: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_api_key: str = os.environ.get("AZURE_OPENAI_API_KEY", "")


# 🔹 2️⃣ Definir estructura de entrada para solicitudes de viaje
class TravelRequest(BaseModel):
    activities: list[str] = Field(..., description="List of activities the user enjoys")
    budget: float = Field(..., gt=0, description="Travel budget in USD")


async def main():
    print("Hello from create-kernel!")

    # 🔹 3️⃣ Cargar y validar la configuración
    try:
        config = ConfigSettings()
    except Exception as e:
        print(f"Error en configuración: {e}")
        return

    # 🔹 4️⃣ Inicializar Kernel y Azure OpenAI
    kernel = Kernel()

    chat_completion = AzureChatCompletion(
        deployment_name=config.azure_deployment_model_name,
        endpoint=config.azure_openai_endpoint,
        api_key=config.azure_openai_api_key,
    )

    kernel.add_service(chat_completion)

    # 🔹 5️⃣ Agregar el plugin de fecha y hora
    kernel.add_plugin(TimePlugin(), plugin_name="TimePlugin")

    # Obtener el día de la semana
    current_day = await kernel.invoke(
        plugin_name="TimePlugin", function_name="dayOfWeek"
    )
    print(f"Today is: {current_day}")

    # 🔹 6️⃣ Validar y procesar solicitud de viaje
    travel_request = TravelRequest(
        activities=["hiking", "mountains", "beaches"], budget=15000.0
    )

    prompt = f"""The following is a conversation with an AI travel assistant. 
    The assistant is helpful, creative, and very friendly.

    <message role="user">Can you give me some travel destination suggestions?</message>

    <message role="assistant">Of course! Do you have a budget or any specific activities in mind?</message>

    <message role="user">I'm planning an anniversary trip with my spouse. 
    We like {", ".join(travel_request.activities)}. Our travel budget is ${travel_request.budget}</message>"""

    result = await kernel.invoke_prompt(prompt)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
