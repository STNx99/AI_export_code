import json
import random
import string

def random_name(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_tailwind_class():
    classes = [
        "bg-blue-500", "bg-red-500", "text-white", "p-4", "m-2", "rounded",
        "text-xl", "font-bold", "flex", "justify-center", "items-center",
        "w-full", "h-10", "border", "border-gray-300"
    ]
    return ' '.join(random.choices(classes, k=random.randint(1, 4)))

def random_react_component():
    name = random_name().capitalize()
    tailwind = random_tailwind_class()
    return f"export default function {name}() {{ return <div className='{tailwind}'>{name} content</div> }}"

def random_html_file():
    tailwind = random_tailwind_class()
    return f"<div class='{tailwind}'>{random_name()} content</div>"

def random_js_file():
    var = random_name()
    return f"const {var} = {{ value: '{var}' }}; export default {var};"

def random_css_file():
    cls = random_name().lower()
    return f".{cls} {{ color: #{random.randint(0, 0xFFFFFF):06x}; font-size: {random.randint(12, 36)}px; }}"

folders = ["components", "services", "lib", "api", "layouts", "middleware", "modules", "src", "styles"]
samples = []

for i in range(100):
    folder = random.choice(folders)
    if not any(f for f in samples if f["type"] == "folder" and f["name"] == folder):
        samples.append({"type": "folder", "parentPath": "", "name": folder})

    file_type = random.choices(
        ["js", "jsx", "css", "html", "json", "md", "py"],
        weights=[15, 25, 15, 15, 10, 10, 10],
        k=1
    )[0]

    file_name = f"{random_name()}.{file_type}"

    if file_type == "jsx":
        content = random_react_component()
    elif file_type == "html":
        content = random_html_file()
    elif file_type == "js":
        content = random_js_file()
    elif file_type == "css":
        content = random_css_file()
    elif file_type == "json":
        content = json.dumps({"config": {"enabled": True, "port": random.randint(3000, 4000)}})
    elif file_type == "md":
        content = f"# {random_name()} Documentation\n\nSome description"
    elif file_type == "py":
        content = f"def {random_name().lower()}():\n    return '{random_name()}'"

    samples.append({
        "type": "file",
        "parentPath": folder,
        "name": file_name,
        "content": content
    })

# save to samples.json
with open("samples.json", "w", encoding="utf-8") as f:
    json.dump(samples, f, ensure_ascii=False, indent=2)

print("✅ Created samples.json with 100 entries (ReactJS + HTML + Tailwind)")
