import re

def extract_sections(vue_template: str):
    pattern = r"(<section[\s\S]*?<\/section>)"
    matches = re.findall(pattern, vue_template)
    sections = []
    for i, section in enumerate(matches, start=1):
        sections.append({
            "name": f"Section{i}",
            "template": section.strip()
        })
    return sections


def create_section_component(section_name: str, template: str):
    """Create Vue SFC (Single File Component) for a section"""
    vue_content = f"""<template>
  {template}
</template>

<script>
export default {{
  name: '{section_name}',
  props: {{}}
}}
</script>

<style scoped>
/* Section styles */
</style>"""
    return vue_content


def create_custom_components():
    """Create custom reusable components"""
    section_component = """<template>
  <section :class="className" :style="styles">
    <slot></slot>
  </section>
</template>

<script>
export default {
  name: 'SectionComponent',
  props: {
    className: {
      type: String,
      default: ''
    },
    styles: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>"""

    div_component = """<template>
  <div :class="className" :style="styles">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'DivComponent',
  props: {
    className: {
      type: String,
      default: ''
    },
    styles: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>"""

    text_component = """<template>
  <component :is="as" :class="className" :style="styles">
    {{ content || '' }}<slot></slot>
  </component>
</template>

<script>
export default {
  name: 'TextComponent',
  props: {
    as: {
      type: String,
      default: 'p'
    },
    content: {
      type: String,
      default: ''
    },
    className: {
      type: String,
      default: ''
    },
    styles: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>"""

    image_component = """<template>
  <img :src="src" :alt="alt" :class="className" loading="lazy" v-bind="$attrs" />
</template>

<script>
export default {
  name: 'ImageComponent',
  props: {
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      default: ''
    },
    className: {
      type: String,
      default: ''
    }
  }
}
</script>"""

    return {
        "SectionComponent": section_component,
        "DivComponent": div_component,
        "TextComponent": text_component,
        "ImageComponent": image_component
    }


def create_app_vue(sections):
    """Create App.vue"""
    imports = []
    components = []
    component_tags = []

    for i, section in enumerate(sections, start=1):
        section_name = section['name']
        imports.append(f"import {section_name} from './components/{section_name}.vue'")
        components.append(f"    {section_name}")
        component_tags.append(f"    <{section_name} />")

    imports_joined = "\n".join(imports)
    components_joined = ",\n".join(components)
    tags_joined = "\n".join(component_tags)

    return f"""<template>
  <div id="app" class="min-h-screen">
{tags_joined}
  </div>
</template>

<script>
{imports_joined}

export default {{
  name: 'App',
  components: {{
{components_joined}
  }}
}}
</script>

<style>
#app {{
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}
</style>"""


def create_main_js():
    """Create main.js"""
    return """import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'

createApp(App).mount('#app')"""


def create_main_css():
    """Create main.css with Tailwind"""
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


def create_index_html():
    """Create index.html"""
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vue App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>"""


def create_vite_config():
    """Create vite.config.js"""
    return """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})"""


def create_tailwind_config():
    """Create tailwind.config.js"""
    return """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}"""


def create_postcss_config():
    """Create postcss.config.js"""
    return """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""


def create_package_json(custom_package_json=""):
    """Create package.json"""
    if custom_package_json:
        return custom_package_json

    return """{
  "name": "vue-app",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.0"
  }
}"""


def generate_vue_project(vue_template: str, package_json=""):
    """Generate complete Vue 3 + Vite project structure"""
    reconstructed = []

    sections = extract_sections(vue_template)

    # Root folder
    reconstructed.append({"type": "folder", "parentPath": "", "name": "vue-app"})

    # Config files
    reconstructed.append({"type": "file", "parentPath": "vue-app", "name": "package.json",
                         "content": create_package_json(package_json)})
    reconstructed.append({"type": "file", "parentPath": "vue-app", "name": "vite.config.js",
                         "content": create_vite_config()})
    reconstructed.append({"type": "file", "parentPath": "vue-app", "name": "tailwind.config.js",
                         "content": create_tailwind_config()})
    reconstructed.append({"type": "file", "parentPath": "vue-app", "name": "postcss.config.js",
                         "content": create_postcss_config()})
    reconstructed.append({"type": "file", "parentPath": "vue-app", "name": "index.html",
                         "content": create_index_html()})

    # src folder
    reconstructed.append({"type": "folder", "parentPath": "vue-app", "name": "src"})
    reconstructed.append({"type": "file", "parentPath": "vue-app/src", "name": "main.js",
                         "content": create_main_js()})
    reconstructed.append({"type": "file", "parentPath": "vue-app/src", "name": "App.vue",
                         "content": create_app_vue(sections)})

    # assets folder
    reconstructed.append({"type": "folder", "parentPath": "vue-app/src", "name": "assets"})
    reconstructed.append({"type": "file", "parentPath": "vue-app/src/assets", "name": "main.css",
                         "content": create_main_css()})

    # components folder
    reconstructed.append({"type": "folder", "parentPath": "vue-app/src", "name": "components"})

    # Custom components
    custom_components = create_custom_components()
    for comp_name, comp_content in custom_components.items():
        reconstructed.append({"type": "file", "parentPath": "vue-app/src/components",
                             "name": f"{comp_name}.vue", "content": comp_content})

    # Section components
    for section in sections:
        section_name = section["name"]
        section_content = create_section_component(section_name, section["template"])
        reconstructed.append({"type": "file", "parentPath": "vue-app/src/components",
                             "name": f"{section_name}.vue", "content": section_content})

    # public folder
    reconstructed.append({"type": "folder", "parentPath": "vue-app", "name": "public"})

    return reconstructed