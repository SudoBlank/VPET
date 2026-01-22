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

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                r = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.config.get('openrouter_api_key', '')}"
                    },
                    json={
                        "model": self.config.get("model", "mistralai/mistral-7b-instruct"),
                        "messages": messages,
                        "temperature": self.config.get("temperature", 1.0),
                        "max_tokens": self.config.get("max_tokens", 200)
                    }
                )
                r.raise_for_status()

            reply = r.json()["choices"][0]["message"]["content"].strip()
            self.memory.append({"role": "assistant", "content": reply})
            return reply
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                error_reply = (
                    "*looks confused* I think my voice box is broken! "
                    "(Check your OpenRouter API key in config.json)"
                )
            else:
                error_reply = f"*confused noises* (HTTP {e.response.status_code} error)"
            self.memory.append({"role": "assistant", "content": error_reply})
            return error_reply
        except Exception as e:
            error_reply = f"*meow?* (Error: {str(e)[:100]})"
            self.memory.append({"role": "assistant", "content": error_reply})
            return error_reply
