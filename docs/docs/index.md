# **TextEmbed**: Embedding Inference Server

[![GitHub release](https://img.shields.io/github/v/release/kevaldekivadiya2415/textembed)](https://github.com/kevaldekivadiya2415/textembed/releases) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/kevaldekivadiya2415/textembed/blob/main/LICENSE)

**TextEmbed** is a high-throughput, low-latency REST API for serving vector embeddings. Built to be flexible and scalable, TextEmbed supports a wide range of sentence-transformer models and frameworks.

> This documentation reflects the latest updates from the `main` branch. For earlier versions, visit the [TextEmbed repository](https://github.com/kevaldekivadiya2415/textembed).

## 🚀 **Get Started Now!**

[![Get Started](https://img.shields.io/badge/GET%20STARTED%20NOW-Informational)](#getting-started)

Explore the key features and setup instructions below.

## 🔍 **Key Features**

- **🌐 Flexible Model Support**: Deploy any model from supported sentence-transformer frameworks, including SentenceTransformers.
- **⚡ High-Performance Inference**: Leverages efficient backends like Torch for optimal performance across various devices.
- **🔄 Dynamic Batching**: Processes new embedding requests as soon as resources are available, ensuring high throughput and low latency.
- **✔️ Accurate and Tested**: Provides embeddings consistent with SentenceTransformers, validated with unit and end-to-end tests for reliability.
- **📜 User-Friendly API**: Built with FastAPI and fully documented via Swagger, conforming to OpenAI's Embedding specs.

## 🛠 **Getting Started**

### **Installation via PyPI**

1. **Install TextEmbed:**

    ```bash
    pip install -U textembed
    ```

2. **Start the Server:**

    ```bash
    python3 -m textembed.server --models <Model1>,<Model2> --port <Port>
    ```

3. **View Help Options:**

    ```bash
    python3 -m textembed.server --help
    ```

### **Running with Docker (Recommended)**

1. **Pull the Docker Image:**

    ```bash
    docker pull kevaldekivadiya/textembed:latest
    ```

2. **Run the Docker Container:**

    ```bash
    docker run -it --gpus all \
     -v $PWD/data:/app/.cache \
     -p 8000:8000 \
     kevaldekivadiya/textembed:latest \
     --models <Model1>,<Model2> \
     --port 8000
    ```

3. **View Help Options:**

    ```bash
    docker run kevaldekivadiya/textembed:latest --help
    ```

## 🌐 **Accessing the API**

Access the API documentation via Swagger UI at `http://localhost:8000/docs`.

---

## 📥 **Contributing**

Contributions are welcome! Please read the [Contributing Guide](https://github.com/kevaldekivadiya2415/textembed/blob/main/CONTRIBUTING.md) to get started.

## 📄 **License**

This project is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/kevaldekivadiya2415/textembed/blob/main/LICENSE) file for details.

## 📧 **Contact**

For questions or support, please reach out through [GitHub Issues](https://github.com/kevaldekivadiya2415/textembed/issues).

---

## 🌟 **Stay Updated**

Stay tuned for updates by following the [TextEmbed repository](https://github.com/kevaldekivadiya2415/textembed). Don't forget to give us a ⭐ if you find this project helpful!

[Back to Top](#textembed-embedding-inference-server)
