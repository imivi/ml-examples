# Machine Learning Examples

**Visit the website** ➡️ https://imivi.github.io/ml-examples/

This repository contains a collection of example jupyter notebooks for machine learning, including regression and classification.

## Use Cases Included

Currently, the repository features:
- **Regression**: Predict housing prices and diamond values.
- **Classification**: Categorize diamonds based on their attributes.

## Build the website

```bash
pip install jupyterlab jinja2 nbconvert
```

To refresh the exported HTML reports and update the `index.html` file, simply run the build script:

```bash
python build.py
```

- **`docs/`**: Contains the source data (`.csv`), the interactive notebooks (`.ipynb`), and the exported reports (`.html`).
- **`templates/`**: Contains the Jinja2 template (`index_template.html`) used to generate the main index page.
- **`build.py`**: A Python automation script that handles notebook-to-HTML conversion and site indexing.

## License

This project is open-source and available under the MIT License.
