1. Simple LLM

### Using LangChain with Ollama Local Model

To use LangChain with the Ollama local model, follow these steps:

1. Install the necessary packages:
    ```bash
    pip install langchain ollama
    ```

2. Initialize the Ollama model and integrate it with LangChain:
    ```python
    from langchain import Ollama

    # Initialize the Ollama model
    ollama_model = Ollama(model_name="your_model_name")

    # Use the model in your LangChain pipeline
    response = ollama_model.generate("Your prompt here")
    print(response)
    ```

3. Customize the model parameters as needed:
    ```python
    ollama_model.set_params(max_tokens=100, temperature=0.7)
    ```

4. Run your LangChain pipeline with the Ollama model integrated.

For more detailed information, refer to the [LangChain documentation](https://langchain.readthedocs.io/) and the [Ollama documentation](https://ollama.readthedocs.io/).

### Using LangChain Language Model

To use LangChain with its built-in language model, follow these steps:

1. Install the necessary package:
    ```bash
    pip install langchain
    ```

2. Initialize the LangChain language model:
    ```python
    from langchain import LanguageModel

    # Initialize the LangChain language model
    langchain_model = LanguageModel(model_name="your_model_name", local=True)

    # Use the model in your LangChain pipeline
    response = langchain_model.generate("Your prompt here")
    print(response)
    ```

3. Customize the model parameters as needed:
    ```python
    langchain_model.set_params(max_tokens=100, temperature=0.7)
    ```

4. Run your LangChain pipeline with the language model integrated.

For more detailed information, refer to the [LangChain documentation](https://langchain.readthedocs.io/).

### Using LangChain with ChatOllama

To use LangChain with the ChatOllama model, follow these steps:

1. Install the necessary packages:
    ```bash
    pip install langchain chatollama
    ```

2. Initialize the ChatOllama model and integrate it with LangChain:
    ```python
    from langchain import ChatOllama

    # Initialize the ChatOllama model
    chatollama_model = ChatOllama(model_name="your_model_name")

    # Use the model in your LangChain pipeline
    response = chatollama_model.generate("Your prompt here")
    print(response)
    ```

3. Customize the model parameters as needed:
    ```python
    chatollama_model.set_params(max_tokens=100, temperature=0.7)
    ```

4. Run your LangChain pipeline with the ChatOllama model integrated.

For more detailed information, refer to the [LangChain documentation](https://langchain.readthedocs.io/) and the [ChatOllama documentation](https://chatollama.readthedocs.io/).