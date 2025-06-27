# 🎬 Azure Multi-Cloud Video Processor

This project is a secure and scalable Flask-based application deployed on **Azure Container Apps**, designed to process videos by copying them from one Azure Blob container to another.

## 🧠 Key Features

- Built using **Python Flask**
- Containerized with **Docker**
- Deployed via **Azure Container App**
- Integrates with **Azure Blob Storage**
- Secure secrets via **Azure Key Vault**
- Uses **System-Assigned Managed Identity**
- Triggered by `curl` or API call with filename input

---

## ☁️ Cloud Services Used

| Cloud        | Service                       | Purpose                                      |
|--------------|-------------------------------|----------------------------------------------|
| **Azure**    | Azure Blob Storage            | Input/Output video files                     |
| **Azure**    | Azure Container Registry      | Docker image storage                         |
| **Azure**    | Azure Container App           | Runs the Flask API                           |
| **Azure**    | Azure Key Vault               | Secure secret management                     |
| **Azure**    | Azure CLI / ARM               | Infrastructure management                    |

---

## 🚀 How It Works

1. You upload a video (e.g. `jugrafiya.mov`) to the source blob container `inputfiles777`.
2. You POST the filename to the container app endpoint:
   ```bash
   curl -X POST https://<your-app-url> \
     -H "Content-Type: application/json" \
     -d '{"filename": "jugrafiya.mov"}'
