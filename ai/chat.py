import json
import httpx

class AIChat:
    def __init__(self, config_path="config.json"):
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            print(f"✓ AI config loaded from {config_path}")
        except Exception as e:
            print(f"❌ Failed to load AI config: {e}")
            self.config = {}

        self.memory = []

    async def ask(self, system_prompt: str, user_text: str, pet_state: dict):
        print(f"  📝 System prompt: {system_prompt[:100]}...")
        print(f"  📝 User text: {user_text}")
        
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
            api_key = self.config.get('openrouter_api_key', '')
            model = self.config.get("model", "mistralai/mistral-7b-instruct")
            
            if not api_key:
                print("❌ OpenRouter API key not found in config.json!")
                error_reply = "I can't respond right now - missing API key!"
                return error_reply
            
            print(f"  🔐 Using model: {model}")
            print(f"  🔐 Calling OpenRouter API...")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                r = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": self.config.get("temperature", 1.0),
                        "max_tokens": self.config.get("max_tokens", 200)
                    }
                )
                print(f"  📡 API Response status: {r.status_code}")
                r.raise_for_status()

            response_data = r.json()
            reply = response_data["choices"][0]["message"]["content"].strip()
            print(f"  ✓ Got response: {reply[:100]}...")
            self.memory.append({"role": "assistant", "content": reply})
            return reply
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP Error: {e.response.status_code}")
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
            print(f"❌ API Error: {type(e).__name__}: {e}")
            error_reply = f"*meow?* (Error: {str(e)[:100]})"
            self.memory.append({"role": "assistant", "content": error_reply})
            return error_reply
