from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from AI_export_code.components.htmlExport.htmlexport import generate_html_project
from AI_export_code.components.reactJSExport.reactjsexport import generate_react_project
from AI_export_code.components.angularExporrt.angularexport import generate_angular_project
from AI_export_code.components.vueExport.vueexport import generate_vue_project
import os
import torch
from AI_export_code.trainModel.train.train import Autoencoder

app = Flask(__name__)
CORS(app)

# ===== LOAD MODEL =====
checkpoint = torch.load("model.pt", map_location="cpu", weights_only=False)
model = Autoencoder(checkpoint["vocab_size"])
model.load_state_dict(checkpoint["model"])
model.eval()
char2idx = checkpoint["char2idx"]
idx2char = checkpoint["idx2char"]


# ===== ANSI COLORS =====
class Color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


# ===== UTILITIES =====
def reconstruct_name(name):
    if not name:
        return name
    import torch
    x = torch.tensor([char2idx.get(c, 0) for c in name]).unsqueeze(0)
    with torch.no_grad():
        out = model(x)
        pred_idx = out.argmax(-1).squeeze().tolist()
        pred_name = "".join([idx2char.get(i, "") for i in pred_idx]).strip()
        return pred_name if pred_name else name


# ===== MAIN API =====
@app.post("/reconstruct")
def reconstruct():
    try:
        data = request.json
        print(f"{Color.BLUE}================= 🧠 [AI RECONSTRUCT REQUEST] ================={Color.END}")
        print(f"{Color.YELLOW}📦 Raw request data:{Color.END}")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:500])

        # fileTreeData có thể là array hoặc object
        file_tree_data = data.get("fileTreeData", [])

        # Nếu fileTreeData là list (array of file nodes)
        if isinstance(file_tree_data, list):
            print(f"{Color.YELLOW}⚠️  fileTreeData is array, extracting metadata from first file...{Color.END}")
            # Lấy export format từ root folder name hoặc file extension
            export_format = "react"  # default

            # Check root folder name để determine format
            for item in file_tree_data:
                if item.get("type") == "folder" and item.get("parentPath") == "":
                    folder_name = item.get("name", "").lower()
                    if "react" in folder_name:
                        export_format = "react"
                    elif "vue" in folder_name:
                        export_format = "vue"
                    elif "angular" in folder_name:
                        export_format = "angular"
                    elif "html" in folder_name:
                        export_format = "html"
                    break

            # Extract content từ files
            react_app = ""
            package_json = ""
            for item in file_tree_data:
                if item.get("type") == "file":
                    name = item.get("name", "")
                    if name == "App.js" or name == "template.txt":
                        react_app = item.get("content", "")
                    elif name == "package.json":
                        package_json = item.get("content", "")

            angular_template = react_app
            vue_template = react_app

        # Nếu fileTreeData là object (có metadata)
        elif isinstance(file_tree_data, dict):
            export_format = file_tree_data.get("exportFormat", "react")
            react_app = file_tree_data.get("reactApp", "")
            angular_template = file_tree_data.get("angularTemplate", "")
            vue_template = file_tree_data.get("vueTemplate", "")
            package_json = file_tree_data.get("packageJson", "")
        else:
            return jsonify({"error": "Invalid fileTreeData format"}), 400

        print(f"{Color.GREEN}📦 Export Format:{Color.END} {export_format}")
        print(f"{Color.GREEN}📝 Content Length:{Color.END} {len(react_app or angular_template or vue_template)} chars")

        reconstructed = []

        if export_format == "react":
            print(f"{Color.BLUE}--- Generating React structure ---{Color.END}")
            reconstructed = generate_react_project(react_app, package_json)

        elif export_format == "angular":
            print(f"{Color.BLUE}--- Generating Angular structure ---{Color.END}")
            reconstructed = generate_angular_project(angular_template, package_json)

        elif export_format == "vue":
            print(f"{Color.BLUE}--- Generating Vue structure ---{Color.END}")
            reconstructed = generate_vue_project(vue_template, package_json)

        elif export_format == "html":
            print(f"{Color.BLUE}--- Generating HTML structure ---{Color.END}")
            reconstructed = generate_html_project(file_tree_data if isinstance(file_tree_data, dict) else {})

        print(f"{Color.BLUE}----------------------------------------------------------{Color.END}")
        print(f"{Color.GREEN}✅ Total files generated:{Color.END} {len(reconstructed)}")
        print(f"{Color.BLUE}=========================================================={Color.END}\n")

        return jsonify({"reconstructed": reconstructed})

    except Exception as e:
        import traceback
        print(f"{Color.RED}[AI ERROR]: {e}{Color.END}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# ===== HEALTH CHECK =====
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": True})


if __name__ == "__main__":
    print(f"{Color.BLUE}🚀 AI Server starting...{Color.END}")
    print(f"{Color.GREEN}Model loaded: vocab_size={checkpoint['vocab_size']}{Color.END}")
    app.run(host="0.0.0.0", port=5001, debug=True)