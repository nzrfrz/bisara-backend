### Create venv for this project
``` bash
python -m venv venv
```

### Install Library
``` bash
pip install -r requirements.txt
```

### Run the Server
``` bash
uvicorn app.main:app --reload
```