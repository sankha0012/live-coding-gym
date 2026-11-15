---
title: Cloud ML platforms (SageMaker, Vertex AI, Databricks)
summary: Managed services for training, registry, serving and monitoring, traded against vendor lock-in and cost.
tags: [ml tools, cloud, managed services]
---
- Training and serving need machines, storage, security, scheduling and monitoring. A cloud ML platform sells these as managed services.
- Shared pattern: data in cloud storage, a job trains on a rented machine, the model goes to a registry, an endpoint serves it.
- They cover most of the pipeline, and you can use only a part.
- The key tradeoff is convenience against lock-in and cost. Idle endpoints still cost money.
- Explain the concepts, not the buttons, and be honest about your level.

<!-- more -->

## Details

- **Amazon SageMaker**: managed notebooks, training jobs, a model registry, real-time endpoints and batch jobs, pipelines and monitoring. It fits teams already in AWS.
- **Vertex AI**: the same ideas on Google Cloud, plus access to Google's hosted models. It connects well with BigQuery.
- **Databricks**: built around Apache Spark and a "lakehouse". Strong for large data processing and shared notebooks. It includes MLflow and runs on top of AWS, Azure or Google Cloud.

A managed training job runs your plain training script somewhere else. Make the script read paths and settings from arguments and write the model to an output folder. The submit call differs on each platform, so look it up in the docs.

Cost control: stop idle endpoints, use batch when latency does not matter, set budgets and alerts.

Security basics: least-privilege access, no secrets in code, data staying in your own account or region.

## What to say and what not to claim

Say: "I have built and run the pipeline pieces locally and with open-source tools. I have not run production workloads on SageMaker, but I understand what it manages and I would read its docs to map my pipeline onto it."

Do not say you have used a platform if you have only read about it. Do not say one platform is "the best".

## Likely interview questions

- **When a managed platform instead of your own servers?** When the team is small, the work is bursty and time to production matters more than fine control.
- **Batch versus online prediction there?** Online is an endpoint that costs money while it runs; batch scores a table on a schedule and is cheaper and simpler.
- **Have you used SageMaker, Vertex or Databricks?** Answer with the truth, and map the steps you have built onto what the platform manages.

## See also

- [Model serving: batch versus online, FastAPI](#/kb/tool-model-serving)
- [Experiment tracking and the model registry (MLflow)](#/kb/tool-experiment-tracking)
