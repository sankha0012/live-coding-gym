---
title: Data and model versioning (DVC)
summary: Version large data and model files next to git, so any result can be reproduced from a commit.
tags: [ml tools, dvc, reproducibility]
---
- A model result depends on the code, the data and the parameters. Git tracks code well and big data files badly.
- DVC (Data Version Control) versions large files and pipelines next to git.
- Git stores a small text pointer file. The real data lives in remote storage such as an object store or a shared disk.
- It sits at the start and the end of the pipeline: datasets in, model files out.

Checked with DVC 3.67 (a remote must be set once with `dvc remote add -d <name> <url>` before `dvc push`):

```bash
dvc init
dvc add data/train.csv          # creates data/train.csv.dvc, ignores the big file in git
dvc push                        # upload data to the remote
dvc pull                        # on another machine, fetch the matching data
```

<!-- more -->

## Details

The core idea is a content hash. The pointer holds the hash of the data, so any change to the file shows up as a different hash.

To go back to an old dataset, check out the old git commit and run `dvc checkout` or `dvc pull`.

- **Artifact store.** Storage for files: model binaries, plots, datasets. Examples: an object bucket, a DVC remote.
- **Model registry.** A catalog on top. It gives each model a name, a version number and a stage such as staging or production.

Traps:

- Committing large data files into git. The repository becomes slow and huge.
- Versioning data but not parameters and code version. The run is still not reproducible.

## What to say and what not to claim

Say: "I version data and models so any result can be reproduced from a commit. Git holds code and small pointer files. A remote holds the large files. A registry gives models names, versions and stages."

Do not claim that DVC tracks metrics in the way MLflow does. Its core job is versioning data and pipelines.

## Likely interview questions

- **Why not put the data in git?** Git is slow with large files; DVC keeps a small pointer in git and the data in remote storage, still tied to a commit.
- **How do you reproduce a model from six months ago?** Check out its commit, pull the matching data and rerun the pipeline with the same seeds.
- **Registry versus artifact store?** The store holds files; the registry adds names, versions, stages and lineage on top.

## See also

- [Experiment tracking and the model registry (MLflow)](#/kb/tool-experiment-tracking)
- [Stable hashing with hashlib (and why not hash())](#/kb/py-hashlib)
- [Determinism: seeds, ordering, time](#/kb/prod-determinism)
