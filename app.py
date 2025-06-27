import os
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()

app = Flask(__name__)

AZURE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Debug print to verify the connection string is loaded
print("DEBUG: AZURE_CONN_STR =", AZURE_CONN_STR)

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)

@app.route("/", methods=["POST"])
def process_file():
    data = request.json
    filename = data.get("filename")

    try:
        src_container = "inputfiles777"
        dest_container = "finalvideos777"

        src_blob = blob_service_client.get_blob_client(container=src_container, blob=filename)
        dest_blob = blob_service_client.get_blob_client(container=dest_container, blob=f"processed-{filename}")

        blob_data = src_blob.download_blob().readall()
        dest_blob.upload_blob(blob_data, overwrite=True)

        return jsonify({"message": f"✅ {filename} processed and saved!"})
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
