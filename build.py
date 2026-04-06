import os
import subprocess
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

def convert_notebooks(docs_dir):
    """Converts all .ipynb files in the docs directory to .html using nbconvert."""
    print("Converting notebooks to HTML...")
    ipynb_files = [f for f in os.listdir(docs_dir) if f.endswith(".ipynb")]
    
    for f in ipynb_files:
        ipynb_path = os.path.join(docs_dir, f)
        html_path = os.path.join(docs_dir, f.replace(".ipynb", ".html"))
        
        # Skip conversion if HTML is newer than IPYNB
        if os.path.exists(html_path) and os.path.getmtime(html_path) > os.path.getmtime(ipynb_path):
            print(f"Skipping {f} (HTML is up to date)")
            continue
            
        print(f"Converting {f}...")
        try:
            subprocess.run([
                "jupyter-nbconvert.exe", 
                "--to", "html", 
                ipynb_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {f}: {e.stderr.decode()}")
        except FileNotFoundError:
            print("Error: 'jupyter-nbconvert.exe' command not found. Run 'pip install jupyterlab'")
            break

def main():
    docs_dir = "docs"
    output_file = "index.html"
    template_dir = "templates"
    template_name = "index_template.html"
    
    if not os.path.exists(docs_dir):
        print(f"Error: Directory '{docs_dir}' not found.")
        return
    
    # 1. Convert IPYNB to HTML
    convert_notebooks(docs_dir)
        
    # 2. Group files by their base name
    file_groups = defaultdict(dict)
    for f in os.listdir(docs_dir):
        if f == "index.html":
            continue
        base_name, ext = os.path.splitext(f)
        if ext in ['.html', '.csv', '.ipynb']:
            file_groups[base_name][ext] = f
            
    # 3. Use Jinja2 to render index.html
    env = Environment(loader=FileSystemLoader(template_dir))
    try:
        template = env.get_template(template_name)
        rendered_html = template.render(
            title="Machine Learning Examples",
            docs_dir=docs_dir,
            file_groups=file_groups
        )
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        print(f"Successfully generated {output_file}")
    except Exception as e:
        print(f"Error rendering template: {e}")

if __name__ == "__main__":
    main()
