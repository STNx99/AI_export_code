import re

def extract_sections(angular_template: str):
    pattern = r"(<app-section[\s\S]*?<\/app-section>)"
    matches = re.findall(pattern, angular_template)
    sections = []
    for i, section in enumerate(matches, start=1):
        sections.append({
            "name": f"section{i}",
            "template": section.strip()
        })
    return sections


def create_section_component(section_name: str, template: str):
    """Create Angular component files for a section"""
    ts_content = f"""import {{ Component }} from '@angular/core';

@Component({{
  selector: 'app-{section_name}',
  templateUrl: './{section_name}.component.html',
  styleUrls: ['./{section_name}.component.css']
}})
export class {section_name.capitalize()}Component {{
  constructor() {{ }}
}}"""

    html_content = template
    css_content = """/* Section styles */"""

    return {
        "ts": ts_content,
        "html": html_content,
        "css": css_content
    }


def create_custom_components():
    """Create custom reusable components module"""
    module_content = """import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SectionComponent } from './section/section.component';
import { DivComponent } from './div/div.component';
import { TextComponent } from './text/text.component';
import { ImageComponent } from './image/image.component';

@NgModule({
  declarations: [
    SectionComponent,
    DivComponent,
    TextComponent,
    ImageComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    SectionComponent,
    DivComponent,
    TextComponent,
    ImageComponent
  ]
})
export class CustomComponentsModule { }"""

    section_ts = """import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-section',
  template: '<section [className]="className" [ngStyle]="styles"><ng-content></ng-content></section>',
  styles: []
})
export class SectionComponent {
  @Input() className: string = '';
  @Input() styles: any = {};
}"""

    div_ts = """import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-div',
  template: '<div [className]="className" [ngStyle]="styles"><ng-content></ng-content></div>',
  styles: []
})
export class DivComponent {
  @Input() className: string = '';
  @Input() styles: any = {};
}"""

    text_ts = """import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-text',
  template: '<ng-container [ngSwitch]="as"><p *ngSwitchCase="\\'p\\'" [className]="className" [ngStyle]="styles">{{content}}<ng-content></ng-content></p><h1 *ngSwitchCase="\\'h1\\'" [className]="className" [ngStyle]="styles">{{content}}<ng-content></ng-content></h1><h2 *ngSwitchCase="\\'h2\\'" [className]="className" [ngStyle]="styles">{{content}}<ng-content></ng-content></h2><span *ngSwitchDefault [className]="className" [ngStyle]="styles">{{content}}<ng-content></ng-content></span></ng-container>',
  styles: []
})
export class TextComponent {
  @Input() as: string = 'p';
  @Input() content: string = '';
  @Input() className: string = '';
  @Input() styles: any = {};
}"""

    image_ts = """import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-image',
  template: '<img [src]="src" [alt]="alt" [className]="className" loading="lazy" />',
  styles: []
})
export class ImageComponent {
  @Input() src: string = '';
  @Input() alt: string = '';
  @Input() className: string = '';
}"""

    return {
        "module": module_content,
        "section": section_ts,
        "div": div_ts,
        "text": text_ts,
        "image": image_ts
    }


def create_app_component(sections):
    ts_content = """import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular-app';
}"""

    section_tags = [f"  <app-{section['name']}></app-{section['name']}>" for section in sections]
    joined_sections = "\n".join(section_tags)

    html_content = f"""<div class="min-h-screen">
{joined_sections}
</div>"""

    css_content = """/* App styles */"""

    return {
        "ts": ts_content,
        "html": html_content,
        "css": css_content
    }


def create_app_module(sections):
    """Create app.module.ts"""
    imports = [
        "import { NgModule } from '@angular/core';",
        "import { BrowserModule } from '@angular/platform-browser';",
        "import { AppComponent } from './app.component';",
        "import { CustomComponentsModule } from './custom-components/custom-components.module';"
    ]

    declarations = ["    AppComponent"]

    for section in sections:
        section_name = section['name']
        imports.append(f"import {{ {section_name.capitalize()}Component }} from './components/{section_name}/{section_name}.component';")
        declarations.append(f"    {section_name.capitalize()}Component")

    imports_joined = "\n".join(imports)
    declarations_joined = ",\n".join(declarations)

    return f"""{imports_joined}

@NgModule({{
  declarations: [
{declarations_joined}
  ],
  imports: [
    BrowserModule,
    CustomComponentsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
}})
export class AppModule {{ }}"""


def create_main_ts():
    return """import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));"""


def create_index_html():
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Angular App</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>"""


def create_styles_css():
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


def create_angular_json():
    return """{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "angular-app": {
      "projectType": "application",
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "outputPath": "dist/angular-app",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": ["zone.js"],
            "tsConfig": "tsconfig.app.json",
            "assets": ["src/favicon.ico", "src/assets"],
            "styles": ["src/styles.css"],
            "scripts": []
          }
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "options": {
            "buildTarget": "angular-app:build"
          }
        }
      }
    }
  }
}"""


def create_tsconfig_json():
    return """{
  "compileOnSave": false,
  "compilerOptions": {
    "baseUrl": "./",
    "outDir": "./dist/out-tsc",
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "sourceMap": true,
    "declaration": false,
    "downlevelIteration": true,
    "experimentalDecorators": true,
    "moduleResolution": "node",
    "importHelpers": true,
    "target": "ES2022",
    "module": "ES2022",
    "useDefineForClassFields": false,
    "lib": ["ES2022", "dom"]
  },
  "angularCompilerOptions": {
    "enableI18nLegacyMessageIdFormat": false,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  }
}"""


def create_tsconfig_app_json():
    return """{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "./out-tsc/app",
    "types": []
  },
  "files": ["src/main.ts"],
  "include": ["src/**/*.d.ts"]
}"""


def create_tailwind_config():
    return """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}"""


def create_package_json(custom_package_json=""):
    if custom_package_json:
        return custom_package_json

    return """{
  "name": "angular-app",
  "version": "0.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development",
    "test": "ng test"
  },
  "private": true,
  "dependencies": {
    "@angular/animations": "^17.0.0",
    "@angular/common": "^17.0.0",
    "@angular/compiler": "^17.0.0",
    "@angular/core": "^17.0.0",
    "@angular/forms": "^17.0.0",
    "@angular/platform-browser": "^17.0.0",
    "@angular/platform-browser-dynamic": "^17.0.0",
    "@angular/router": "^17.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.2"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^17.0.0",
    "@angular/cli": "^17.0.0",
    "@angular/compiler-cli": "^17.0.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "typescript": "~5.2.2"
  }
}"""


def generate_angular_project(angular_template: str, package_json=""):
    reconstructed = []

    sections = extract_sections(angular_template)

    reconstructed.append({"type": "folder", "parentPath": "", "name": "angular-app"})
    reconstructed.append({"type": "file", "parentPath": "angular-app", "name": "package.json",
                         "content": create_package_json(package_json)})
    reconstructed.append({"type": "file", "parentPath": "angular-app", "name": "angular.json",
                         "content": create_angular_json()})
    reconstructed.append({"type": "file", "parentPath": "angular-app", "name": "tsconfig.json",
                         "content": create_tsconfig_json()})
    reconstructed.append({"type": "file", "parentPath": "angular-app", "name": "tsconfig.app.json",
                         "content": create_tsconfig_app_json()})
    reconstructed.append({"type": "file", "parentPath": "angular-app", "name": "tailwind.config.js",
                         "content": create_tailwind_config()})

    reconstructed.append({"type": "folder", "parentPath": "angular-app", "name": "src"})
    reconstructed.append({"type": "file", "parentPath": "angular-app/src", "name": "main.ts",
                         "content": create_main_ts()})
    reconstructed.append({"type": "file", "parentPath": "angular-app/src", "name": "index.html",
                         "content": create_index_html()})
    reconstructed.append({"type": "file", "parentPath": "angular-app/src", "name": "styles.css",
                         "content": create_styles_css()})

    reconstructed.append({"type": "folder", "parentPath": "angular-app/src", "name": "app"})
    reconstructed.append({"type": "file", "parentPath": "angular-app/src/app", "name": "app.module.ts",
                         "content": create_app_module(sections)})

    app_component = create_app_component(sections)
    reconstructed.append({"type": "file", "parentPath": "angular-app/src/app", "name": "app.component.ts",
                         "content": app_component["ts"]})
    reconstructed.append({"type": "file", "parentPath": "angular-app/src/app", "name": "app.component.html",
                         "content": app_component["html"]})
    reconstructed.append({"type": "file", "parentPath": "angular-app/src/app", "name": "app.component.css",
                         "content": app_component["css"]})

    reconstructed.append({"type": "folder", "parentPath": "angular-app/src/app", "name": "custom-components"})
    custom_components = create_custom_components()
    reconstructed.append({"type": "file", "parentPath": "angular-app/src/app/custom-components",
                         "name": "custom-components.module.ts", "content": custom_components["module"]})

    for comp_name in ["section", "div", "text", "image"]:
        reconstructed.append({"type": "folder", "parentPath": "angular-app/src/app/custom-components",
                             "name": comp_name})
        reconstructed.append({"type": "file",
                             "parentPath": f"angular-app/src/app/custom-components/{comp_name}",
                             "name": f"{comp_name}.component.ts", "content": custom_components[comp_name]})

    reconstructed.append({"type": "folder", "parentPath": "angular-app/src/app", "name": "components"})

    for section in sections:
        section_name = section["name"]
        section_folder = f"angular-app/src/app/components/{section_name}"

        reconstructed.append({"type": "folder", "parentPath": "angular-app/src/app/components",
                             "name": section_name})

        section_files = create_section_component(section_name, section["template"])
        reconstructed.append({"type": "file", "parentPath": section_folder,
                             "name": f"{section_name}.component.ts", "content": section_files["ts"]})
        reconstructed.append({"type": "file", "parentPath": section_folder,
                             "name": f"{section_name}.component.html", "content": section_files["html"]})
        reconstructed.append({"type": "file", "parentPath": section_folder,
                             "name": f"{section_name}.component.css", "content": section_files["css"]})

    reconstructed.append({"type": "folder", "parentPath": "angular-app/src", "name": "assets"})

    return reconstructed
