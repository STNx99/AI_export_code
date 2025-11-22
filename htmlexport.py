def generate_html_project(file_tree_data):
    """
    Tạo project HTML tĩnh từ dữ liệu JSON.
    Hiện tại là tạo 1 project cơ bản gồm index.html, style.css
    """
    reconstructed = []

    # Root folder
    reconstructed.append({"type":"folder","parentPath":"","name":"html-project"})

    # public folder
    reconstructed.append({"type":"folder","parentPath":"html-project","name":"public"})

    # index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTML Export</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>Hello HTML Export</h1>
</body>
</html>"""
    reconstructed.append({"type":"file","parentPath":"html-project/public","name":"index.html","content":html_content})

    # style.css
    css_content = """body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}"""
    reconstructed.append({"type":"file","parentPath":"html-project/public","name":"style.css","content":css_content})

    return reconstructed
