# 3d-photo-inpainting port for RunwayML (Work in progress)

[![RunwayML Badge](https://open-app.runwayml.com/gh-badge.svg)](https://open-app.runwayml.com/)

https://github.com/vt-vl-lab/3d-photo-inpainting

(This port us using forked version of the original repo.)

## Testing the Model

While you're developing your model it's useful to run and test it locally.

```bash
## Optionally create and activate a Python 3 virtual environment
# virtualenv -p python3 venv && source venv/bin/activate

pip install -r requirements.txt

# Run the entrypoint script
python runway_model.py
```

You should see an output similar to this, indicating your model is running.

```
Setting up model...
[SETUP] Ran with options: seed = 0, truncation = 10
Starting model server at http://0.0.0.0:8000...
```

# License

This port is Licensed under the MIT License.  
3d-photo-inpainting licensed as MIT License.  
MiDaS licensed as MIT License.  
EdgeConnect licensed as Attribution-NonCommercial 4.0 International.
