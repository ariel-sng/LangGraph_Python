from openai import APIConnectionError, APIError, APITimeoutError, BadRequestError, OpenAIError, RateLimitError


def invoke_chain_with_error_handling(chain, inputs, error_context="LLM"):
    try:
        return chain.invoke(inputs)
    except BadRequestError as exc:
        message = str(exc).lower()
        if "maximum context length" in message or "token" in message or "maximum tokens" in message:
            raise RuntimeError(
                f"Límite de tokens excedido al ejecutar {error_context}."
            ) from exc
        raise RuntimeError(f"Solicitud inválida al ejecutar {error_context}.") from exc
    except (RateLimitError, APITimeoutError, APIConnectionError, APIError) as exc:
        raise RuntimeError(f"Error de API al ejecutar {error_context}: {exc}") from exc
    except OpenAIError as exc:
        raise RuntimeError(f"Error de OpenAI no recuperable al ejecutar {error_context}: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Error inesperado al ejecutar {error_context}: {exc}") from exc
