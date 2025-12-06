import re

def extract_sections(react_app_code: str):
    """Extract SectionComponent blocks from App.js"""
    pattern = r"(<SectionComponent[\s\S]*?<\/SectionComponent>)"
    matches = re.findall(pattern, react_app_code)
    sections = []
    for i, section in enumerate(matches, start=1):
        section_content = f"""import React from 'react';
import {{ SectionComponent, DivComponent, TextComponent, ImageComponent }} from './CustomComponents';

export default function Section{i}() {{
  return (
    {section.strip()}
  );
}}"""
        sections.append({
            "name": f"Section{i}.js",
            "content": section_content
        })
    return sections

def create_custom_components():
    """Create CustomComponents.js content"""
    return """import React from 'react';

export const SectionComponent = ({ children, className = '', ...props }) => (
  <section className={className} {...props}>{children}</section>
);

export const DivComponent = ({ children, className = '', styles = {}, ...props }) => (
  <div className={className} style={styles} {...props}>{children}</div>
);

export const TextComponent = ({ as: Component = 'p', children, content, className = '', styles = {}, ...props }) => (
  <Component className={className} style={styles} {...props}>
    {content || children}
  </Component>
);

export const ImageComponent = ({ src, alt, className = '', ...props }) => (
  <img src={src} alt={alt} className={className} loading="lazy" {...props} />
);"""

def create_app_js(sections):
    imports = ["import React, { useState, useEffect } from 'react';", "import './index.css';"]
    for i in range(1, len(sections)+1):
        imports.append(f"import Section{i} from './components/Section{i}';")
    component_calls = [f"      <Section{i} />" for i in range(1, len(sections)+1)]
    return f"""{chr(10).join(imports)}

function App() {{
  return (
    <div className="min-h-screen">
{chr(10).join(component_calls)}
    </div>
  );
}}

export default App;"""

def create_index_js():
    return """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);"""

def create_index_css():
    return """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}"""

def create_tailwind_config():
    return """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}"""

def create_index_html():
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="AI Generated React App" />
    <title>React App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>"""

def generate_react_project(react_app_code, package_json=""):
    reconstructed = []

    # Extract sections
    sections = extract_sections(react_app_code)

    # Root folder
    reconstructed.append({"type":"folder","parentPath":"","name":"react-app"})

    # package.json
    if package_json:
        reconstructed.append({"type":"file","parentPath":"react-app","name":"package.json","content":package_json})

    # src & components
    reconstructed.append({"type":"folder","parentPath":"react-app","name":"src"})
    reconstructed.append({"type":"folder","parentPath":"react-app/src","name":"components"})

    # CustomComponents.js
    reconstructed.append({"type":"file","parentPath":"react-app/src/components","name":"CustomComponents.js","content":create_custom_components()})

    # Section components
    for section in sections:
        reconstructed.append({"type":"file","parentPath":"react-app/src/components","name":section["name"],"content":section["content"]})

    # App.js
    reconstructed.append({"type":"file","parentPath":"react-app/src","name":"App.js","content":create_app_js(sections)})

    # index.js, index.css, tailwind.config.js
    reconstructed.append({"type":"file","parentPath":"react-app/src","name":"index.js","content":create_index_js()})
    reconstructed.append({"type":"file","parentPath":"react-app/src","name":"index.css","content":create_index_css()})
    reconstructed.append({"type":"file","parentPath":"react-app","name":"tailwind.config.js","content":create_tailwind_config()})

    # public/index.html
    reconstructed.append({"type":"folder","parentPath":"react-app","name":"public"})
    reconstructed.append({"type":"file","parentPath":"react-app/public","name":"index.html","content":create_index_html()})

    return reconstructed
