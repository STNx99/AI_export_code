import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import multiprocessing

# -----------------------------
# Config
# -----------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_LEN = 512       # payload_str max length
BATCH_SIZE = 16     # batch size, tăng nếu GPU đủ memory
NUM_WORKERS = 0     # Windows safe, Linux có thể tăng lên 2-4
EPOCHS = 50         # thử nghiệm trước, tăng nếu cần

DATA_PATH = Path("dataset.jsonl")
MODEL_PATH = Path("model.pt")

print(f"⚡ Training on {DEVICE}")

# -----------------------------
# Dataset
# -----------------------------
class JsonLinedDataset(Dataset):
    def __init__(self, path=DATA_PATH, max_len=MAX_LEN):
        self.max_len = max_len
        self.samples = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                self.samples.append(json.loads(line))

        if len(self.samples) == 0:
            raise ValueError("File dataset.jsonl rỗng!")

        chars = set()
        for s in self.samples:
            chars.update(s.get("payload_str", ""))
        self.char2idx = {c: i + 1 for i, c in enumerate(sorted(chars))}  # 0=pad
        self.idx2char = {i: c for c, i in self.char2idx.items()}
        self.vocab_size = len(self.char2idx) + 1

    def __len__(self):
        return len(self.samples)

    def encode(self, text):
        ids = [self.char2idx.get(c, 0) for c in text[:self.max_len]]
        if len(ids) < self.max_len:
            ids += [0] * (self.max_len - len(ids))
        return ids

    def __getitem__(self, idx):
        sample = self.samples[idx]
        x = torch.tensor(self.encode(sample.get("payload_str", "")))
        return x, x.clone()

# -----------------------------
# Model
# -----------------------------
class Autoencoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, hidden=256):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.layernorm = nn.LayerNorm(embed_dim)
        self.encoder = nn.LSTM(embed_dim, hidden, batch_first=True)
        self.decoder = nn.LSTM(embed_dim, hidden, batch_first=True)
        self.fc = nn.Linear(hidden, vocab_size)

    def forward(self, x):
        emb = self.layernorm(self.emb(x))
        _, (h, c) = self.encoder(emb)
        dec_out, _ = self.decoder(emb, (h, c))
        return self.fc(dec_out)

# -----------------------------
# Train
# -----------------------------
if __name__ == "__main__":
    multiprocessing.freeze_support()  # Windows safe

    dataset = JsonLinedDataset()
    loader = DataLoader(
        dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS
    )

    model = Autoencoder(dataset.vocab_size).to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=1e-4)
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for ep in range(EPOCHS):
        total_loss = 0
        for x, y in loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            opt.zero_grad()
            out = model(x)

            if torch.isnan(out).any():
                print("❌ NaN detected!")

            loss = loss_fn(out.view(-1, dataset.vocab_size), y.view(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
            opt.step()

            total_loss += loss.item()
        print(f"Epoch {ep+1}/{EPOCHS} loss={total_loss / len(loader):.4f}")

    # Save model + vocab
    torch.save(
        {
            "model": model.state_dict(),
            "char2idx": dataset.char2idx,
            "idx2char": dataset.idx2char,
            "vocab_size": dataset.vocab_size,
        },
        MODEL_PATH,
    )
    print(f"✅ Saved model to {MODEL_PATH}")
