from openai import OpenAI

class LLMGenerator:

    def __init__(
        self,
        client: OpenAI,
        model: str,
    ):
        self.client = client
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text