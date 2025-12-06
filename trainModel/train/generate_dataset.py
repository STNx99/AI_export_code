import json
from pathlib import Path

input_file = Path("samples.json")
output_file = Path("dataset.jsonl")
NUM_RECORDS = 1000  # có thể tăng tùy ý

# Đọc toàn bộ array từ samples.json
with input_file.open("r", encoding="utf-8") as f:
    samples = json.load(f)

num_samples = len(samples)
if num_samples == 0:
    raise ValueError("❌ File samples.json rỗng!")

print(f"⚡ Đã load {num_samples} mẫu gốc từ samples.json")

# Ghi dataset.jsonl
with output_file.open("w", encoding="utf-8") as out:
    for i in range(NUM_RECORDS):
        sample = samples[i % num_samples]

        # payload_str chứa đầy đủ content + tên file + type + parentPath
        payload_str = f"{sample.get('name','')} {sample.get('type','')} {sample.get('parentPath','')} {sample.get('content','')}"

        record = {
            "id": i,
            "payload": sample,       # giữ nguyên JSON để reconstruct FileTree
            "payload_str": payload_str
        }

        out.write(json.dumps(record, ensure_ascii=False) + "\n")

        # log tiến độ
        if (i + 1) % 1000 == 0:
            print(f"✅ Đã tạo {i + 1} mẫu")

print(f"🎉 Hoàn thành: đã tạo {NUM_RECORDS} dòng trong {output_file}")
