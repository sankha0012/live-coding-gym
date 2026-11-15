---
title: Containers and Docker
summary: A container packages the application with its exact dependencies so it runs the same on a laptop, in CI and in production.
tags: [ml tools, docker, containers]
---
- Docker solves "it works on my machine": a model can behave differently, or fail to load, under another library version.
- A container packages the application together with its exact dependencies.
- It sits between building and running: training jobs, batch scoring jobs and model services are all built into images.
- Key terms: image, container, Dockerfile, registry, layer.
- A container fixes the software environment. The seed and the data version fix the rest of reproducibility.

Illustrative, not run here:

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

<!-- more -->

## Details

An image is a read-only template with the files, libraries and start command. A container is a running instance of it, and you can start many from one image. Each Dockerfile step creates a cached layer, so order matters for build speed.

A container is not a virtual machine. It shares the host's kernel, starts fast and is lighter, but its isolation is weaker.

Good habits: pin dependency versions, use a slim base image, tag images with a version and not only `latest`, and never put secrets inside the image. Pass secrets at run time through environment variables or a secret manager.

Traps:

- Unpinned dependencies. The image builds today and differs tomorrow.
- Believing a container makes results deterministic.

## What to say and what not to claim

Say: "I containerise the model service so the environment is identical in development, CI and production. I pin dependencies, tag images by version and keep secrets out of the image."

Do not claim Kubernetes experience because you know Docker. Do not say containers are virtual machines. Do not say a container guarantees reproducible model results by itself.

## Likely interview questions

- **Image versus container?** The image is the built, read-only template; a container is a running instance of it.
- **Why do ML teams use Docker?** The Python version, libraries and system packages travel with the code, and every deployment is "run this image".
- **How do you keep the build fast and the image small?** Slim base image, requirements copied before code, no pip cache, and a `.dockerignore`.

## See also

- [Model serving: batch versus online, FastAPI](#/kb/tool-model-serving)
- [CI/CD for ML](#/kb/tool-ci-cd-ml)
- [Determinism: seeds, ordering, time](#/kb/prod-determinism)
