# **Setup Guide for TextEmbed**

This guide provides detailed instructions for setting up the **TextEmbed** server using both PyPI and Docker. Follow the steps below to get started!

## 📝 **Prerequisites**

- **Python Version**: Ensure you have **Python 3.10** or higher installed.
- **Dependencies**: Install all required dependencies for the TextEmbed server.

## ⚙️ **Installation via PyPI**

1. **Install the required dependencies:**

    ```bash
    pip install -U textembed
    ```

2. **Start the TextEmbed server with your desired models:**

    ```bash
    python3 -m textembed.server --models <Model1>,<Model2> --port <Port>
    ```

3. **For more information and additional options, run:**

    ```bash
    python3 -m textembed.server --help
    ```

### 🔧 **Available Server Options:**

- **`--models`**: Comma-separated list of Huggingface models to be used, e.g., `<Model1>,<Model2>`.
- **`--served_model_names`**: Comma-separated list of names under which the models will be served.
- **`--host`**: The host address where the application will run.
- **`--port`**: The port number where the application will run.
- **`--workers`**: Number of worker processes for batch processing.
- **`--batch_size`**: The batch size for processing requests.
- **`--embedding_dtype`**: The data type for the embeddings (`binary`, `float16`, or `float32`).
- **`--api_key`**: Your API key for authentication (Keep it secure and do not share it with others).

## 🐳 **Running with Docker (Recommended)**

Run TextEmbed using Docker for a more streamlined deployment. The Docker image is available on Docker Hub.

1. **Pull the Docker image:**

    ```bash
    docker pull kevaldekivadiya/textembed:latest
    ```

2. **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 kevaldekivadiya/textembed:latest --models <Model1>,<Model2> --port <Port>
    ```

3. **For more information and additional options, run:**

    ```bash
    docker run kevaldekivadiya/textembed:latest --help
    ```

This command displays the help message for the TextEmbed server, detailing the available options and usage instructions.

## 🌐 **Accessing the API**

Once the server is running, you can access the API documentation via Swagger UI by navigating to [`http://localhost:8000/docs`](http://localhost:8000/docs) in your web browser.

## 🖼️ **Image Embedding Example**

TextEmbed now supports generating embeddings for images, such as using the SentenceTransformer CLIP model ([`sentence-transformers/clip-ViT-B-32`](https://huggingface.co/sentence-transformers/clip-ViT-B-32)).

### 📷 **Steps to Generate Image Embeddings**

1. **Convert Image to Base64 String:**

    ```python
    import base64

    def image_to_base64(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

    image_path = '<IMAGE_PATH>'
    base64_string = image_to_base64(image_path)
    ```

2. **Make a POST Request to the TextEmbed Server:**

    ```python
    import requests

    resp = requests.post(url="http://0.0.0.0:8000/v1/image_embedding", json={
      "input": [
        base64_string
      ],
      "model": "sentence-transformers/clip-ViT-B-32",
      "user": "string"
    })

    print(resp.json())
    ```

### 📩 **Example Request and Response**

**Request:**

```json
{
  "input": [
    "<Base64EncodedImageString>"
  ],
  "model": "sentence-transformers/clip-ViT-B-32",
  "user": "string"
}
```

**Response:**

```json
{
  "embeddings": [
    [0.1, 0.2, ..., 0.3]
  ],
  "model": "sentence-transformers/clip-ViT-B-32",
  "user": "string"
}
```
