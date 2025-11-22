import json
import torch
from train import Autoencoder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----- Load model -----
checkpoint = torch.load("model.pt", map_location=device)
char2idx = checkpoint["char2idx"]
idx2char = checkpoint["idx2char"]
vocab_size = checkpoint["vocab_size"]

model = Autoencoder(vocab_size)
model.load_state_dict(checkpoint["model"])
model.to(device)
model.eval()

# ----- Example input -----
input_data = [
    {"type": "folder", "parentPath": "", "name": "components"},
    {
        "type": "file",
        "parentPath": "components",
        "name": "Button.js",
        "content": "export default function Button(){ return <button className='btn'>Click</button> }"
    },
    {
        "type": "file",
        "parentPath": "components",
        "name": "Card.jsx",
        "content": "export default function Card(){ return <div className='p-4 border rounded'>Card</div> }"
    }
]

reconstructed_data = []

# ----- Encode & decode 'content' -----
def reconstruct_text(text: str, max_len: int = 512) -> str:
    text = text[:max_len]
    x = torch.tensor([char2idx.get(c, 0) for c in text]).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(x)
    pred_idx = out.argmax(-1).squeeze().cpu().tolist()
    # Nếu đầu ra là int, wrap thành list
    if isinstance(pred_idx, int):
        pred_idx = [pred_idx]
    pred_text = "".join([idx2char.get(i, "") for i in pred_idx]).strip()
    return pred_text

for item in input_data:
    new_item = item.copy()
    if item["type"] == "file":
        content = item.get("content", "")
        new_item["content"] = reconstruct_text(content, max_len=512)
    reconstructed_data.append(new_item)

# ----- Print -----
print("=== INPUT DATA ===")
print(json.dumps(input_data, ensure_ascii=False, indent=2))

print("\n=== RECONSTRUCTED DATA ===")
print(json.dumps(reconstructed_data, ensure_ascii=False, indent=2))
