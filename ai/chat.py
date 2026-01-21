import json
import httpx

class AIChat:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.memory = []

    async def ask(self, system_prompt: str, user_text: str, pet_state: dict):
        self.memory.append({"role": "user", "content": user_text})

        messages = [
            {
                "role": "system",
                "content": (
                    f"{system_prompt}\n"
                    f"Current pet state: {pet_state}"
                )
            },
            *self.memory[-8:]
        ]

        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config['openrouter_api_key']}"
                },
                json={
                    "model": self.config["model"],
                    "messages": messages,
                    "temperature": self.config["temperature"],
                    "max_tokens": self.config["max_tokens"]
                }
            )
            r.raise_for_status()

        reply = r.json()["choices"][0]["message"]["content"].strip()
        self.memory.append({"role": "assistant", "content": reply})
        return reply
