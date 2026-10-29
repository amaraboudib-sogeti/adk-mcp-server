# Sogeti MCP Server (`adk-mcp-server`)

An open-source implementation of the **Model Context Protocol (MCP)** built with FastAPI to securely expose local enterprise directory data to AI agents.

## 🔌 Overview

This repository acts as an agnostic data gateway. Instead of building custom APIs for every system, it normalizes lookups using the industry-standard Model Context Protocol (MCP) over JSON-RPC 2.0.

- **Endpoint:** Exposes a single `POST /mcp` route.
- **Capability:** Dynamically answers tool discovery (`tools/list`) and tools execution (`tools/call`) requests.

---

## 🛠️ Prerequisites

- Python 3.11+
- Google Cloud SDK (`gcloud` CLI) authenticated to your project.

## 📦 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd adk-mcp-server
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally:**
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8080
   ```

---

## 🚀 Google Cloud Run Deployment

Compile and launch the data gateway as a serverless container inside the Paris region (`europe-west9`):

```bash
# 1. Build the container image securely on Artifact Registry
gcloud builds submit --tag gcr.io/data-archi/os-sogeti-mcp:v1 .

# 2. Deploy to Cloud Run
gcloud run deploy os-sogeti-mcp \
    --image gcr.io/data-archi/os-sogeti-mcp:v1 \
    --region europe-west9 \
    --allow-unauthenticated
```

> ⚠️ **Important:** Copy the live production URL generated at the end of this deployment (e.g., `https://run.app`). You will need it to configure the frontend agent.
