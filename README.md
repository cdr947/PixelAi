# PixelMind AI

PixelMind AI is a Django-based object detection web app that lets users upload an image, run YOLO inference, and view both detection metadata and annotated output images.

## About This Project

This project is built to provide a practical, end-to-end computer vision workflow:

- Upload an image from the browser.
- Run inference using a YOLO segmentation model.
- Save and display the predicted image with annotations.
- Store detection output and recent upload history in the database.

The app is designed as a simple base for experimentation, learning, and extension into larger AI products.

## Tech Stack

- Python 3
- Django
- Ultralytics YOLO
- PyTorch
- SQLite (local) / PostgreSQL (deploy)
- Gunicorn + Uvicorn worker for ASGI deployment

## Project Structure

- `config/`: Django project settings and URL configuration
- `webapp/`: Core app logic (views, models, inference, templates)
- `media/uploads/`: Original uploaded files
- `media/predicted/`: Inference outputs grouped by upload ID
- `staticfiles/`: Collected static assets for deployment

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python3 manage.py migrate
```

4. Start the development server:

```bash
python3 manage.py runserver
```

5. Open the app at `http://127.0.0.1:8000/`.

## Configuration Notes

- `MEDIA_ROOT` is set to `media/` and `MEDIA_URL` is `/media/`.
- In development, Django can serve media files when `DEBUG=true`.
- In production (`DEBUG=false`), serve media through your web server or object storage.

## Running with Gunicorn

ASGI mode:

```bash
python3 -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```

WSGI mode:

```bash
python3 -m gunicorn config.wsgi:application
```

Use WSGI mode unless you specifically need ASGI features.

## Current Status

PixelMind AI currently supports image upload and detection result visualization. Video streaming and advanced filtering options are present in UI placeholders and can be extended in future iterations.
