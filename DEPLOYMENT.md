# PythonAnywhere Deployment

This project is deployed on PythonAnywhere as an ASGI FastAPI app.

## Live URLs

- App base URL: `https://MideasternM.pythonanywhere.com`
- Health endpoint: `https://MideasternM.pythonanywhere.com/health`
- Swagger UI: `https://MideasternM.pythonanywhere.com/docs`

The PythonAnywhere web app is live and serving the FastAPI application.

## Runtime configuration

The application reads these environment variables when present:

- `APP_NAME`
- `API_KEY`
- `DATABASE_URL`

For PythonAnywhere, the current deployment uses:

- `APP_NAME=Nutrition and Recipe Analytics API`
- `API_KEY=dev-secret-key`
- `DATABASE_URL=sqlite:////home/MideasternM/nutrition-api/nutrition.db`

## Deploy command

PythonAnywhere runs the app with:

```bash
/bin/bash -lc 'python3.11 -m pip install --user -r /home/MideasternM/nutrition-api/requirements.txt >/home/MideasternM/nutrition-api/pythonanywhere_pip.log 2>&1 && exec /usr/bin/python3.11 /home/MideasternM/nutrition-api/pythonanywhere_run.py'
```

## Redeploy

After pushing new changes to GitHub:

```bash
cd /home/MideasternM/nutrition-api
git pull
python3.11 -m pip install --user -r requirements.txt
```

Then reload the PythonAnywhere web app from the dashboard or API.
