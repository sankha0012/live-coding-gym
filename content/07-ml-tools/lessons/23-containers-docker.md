# Containers and Docker

## What problem it solves

"It works on my machine" is the oldest bug in software. In ML it is worse. A model trained with one version of scikit-learn can behave differently, or fail to load, under another. The system also depends on the Python version, system libraries and sometimes GPU drivers. Different laptops and servers have different versions of all of these.

A container packages the application together with its exact dependencies. The same package runs the same way on a laptop, in CI and in production.

## Where it sits in an ML pipeline

It sits at the boundary between building and running. Training jobs, batch scoring jobs and model services are all built into images. A registry stores the images. An orchestrator or a platform such as Kubernetes runs them. Because the image is fixed, a result from last month can be reproduced with the same image, together with the same data and seed.

Key words:

- **Image**: a read-only template with the files, libraries and start command. You build it once.
- **Container**: a running instance of an image. You can start many from one image.
- **Dockerfile**: the text recipe for building an image.
- **Registry**: a place to store and share images.
- **Layer**: each Dockerfile step creates a cached layer. Order matters for build speed.

A container is not a virtual machine. It shares the host's kernel and starts fast, and it is lighter, but its isolation is weaker.

## A minimal real example

Illustrative, not run here. Docker is not installed in this project. This is a small Dockerfile for a Python model service. It assumes a `requirements.txt` with pinned versions (including `uvicorn` and your web framework), a `service.py` that exposes an app, and a saved `model.joblib`.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first so this layer is cached when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service.py model.joblib ./

EXPOSE 8000
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
```

Typical commands:

```text
docker build -t late-model:1.0 .
docker run -p 8000:8000 late-model:1.0
```

Why this order: dependencies change rarely and code changes often. If you copy the code first, every edit forces a slow reinstall. With the order above, Docker reuses the cached install layer.

Good habits: pin dependency versions, use a slim base image, tag images with a version and not only `latest`, and never put secrets inside the image. Pass secrets at run time through environment variables or a secret manager.

## The traps

- Unpinned dependencies. The image builds today and differs tomorrow.
- Baking the model or credentials in carelessly. Large models make images huge. Secrets in an image leak to anyone who can pull it.
- Running as root without need, and using `latest` as the only tag. Both make deployments less safe and less traceable.
- Believing a container makes results deterministic. It fixes the software environment. You still need seeds and fixed data.

## What to say in an interview

Say: "I containerise the model service so the environment is identical in development, CI and production. I pin dependencies, tag images by version and keep secrets out of the image."

Say that the container fixes the environment, and the seed and data version fix the rest of reproducibility.

Do NOT claim Kubernetes experience because you know Docker. They are different tools. Do NOT say containers are virtual machines. Do NOT say a container guarantees reproducible model results by itself.

## Three likely questions

**1. What is the difference between an image and a container?**
An image is the built, read-only template. A container is a running instance of it. I can start many containers from one image, like many processes from one program.

**2. Why do ML teams use Docker?**
It makes the environment reproducible. Library versions, Python version and system packages travel with the code, so the model behaves the same in training, testing and production. It also makes deployment uniform: every service is "run this image".

**3. How do you keep a Docker build fast and the image small?**
I use a slim base image and copy the requirements file before the code, so the install layer is cached. I install with no pip cache and add a `.dockerignore` so data and notebooks do not enter the build. For large models I load from storage at start-up, instead of baking them into the image, when that fits the case.
