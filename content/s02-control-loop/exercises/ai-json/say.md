In production I'd prefer the provider's structured output or tool-calling mode, validate against a schema (Pydantic), and on failure retry once with the error message before falling back.
