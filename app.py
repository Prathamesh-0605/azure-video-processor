import os
import tempfile
import subprocess
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

AZURE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)

@app.route("/", methods=["POST"])
def process_file():
    data = request.json
    filename = data.get("filename")

    try:
        src_container = "inputfiles777"
        dest_container = "finalvideos777"

        src_blob = blob_service_client.get_blob_client(container=src_container, blob=filename)
        dest_blob = blob_service_client.get_blob_client(container=dest_container, blob=f"compressed-{filename}")

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, filename)
            output_path = os.path.join(tmpdir, f"compressed-{filename}")

            with open(input_path, "wb") as f:
                f.write(src_blob.download_blob().readall())

            subprocess.run([
                "ffmpeg", "-i", input_path,
                "-vcodec", "libx264", "-crf", "28",
                output_path
            ], check=True)

            with open(output_path, "rb") as out_f:
                dest_blob.upload_blob(out_f, overwrite=True)

        return jsonify({"message": f"✅ {filename} compressed and uploaded."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
