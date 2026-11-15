# Data and model versioning with DVC

## What problem it solves

Git tracks code well. It tracks big data files badly. But a model result depends on three things: the code, the data and the parameters. If you only version the code, you cannot reproduce last month's model. Someone changed the data file and nobody knows when.

DVC (Data Version Control) versions large files and pipelines next to git. Git stores a small text pointer file. The real data lives in remote storage such as an object store or a shared disk.

## Where it sits in an ML pipeline

At the start and the end. Raw and processed datasets are tracked as inputs. Trained model files are tracked as outputs. DVC can also describe the steps in between (prepare, train, evaluate) so the pipeline reruns only what changed.

## Registry versus artifact store

These are often confused.

- **Artifact store.** A place that keeps files: model binaries, plots, datasets. It is storage. Examples: an object bucket, a DVC remote, an MLflow artifact location.
- **Model registry.** A catalog on top of the artifacts. It gives each model a name, a version number and a stage such as staging or production. It records which run and which data produced it. Examples: the MLflow Model Registry, cloud registries.

The artifact store answers "where is the file". The registry answers "which model is in production right now and where did it come from".

## A minimal real example

The core idea is a content hash. A pointer holds the hash of the data, so any change shows up as a different hash. This runs on Python 3.12.

```python
import hashlib
import tempfile
from pathlib import Path


def file_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "train.csv"
    p.write_text("a,b\n1,2\n")
    before = file_hash(p)
    p.write_text("a,b\n1,3\n")
    after = file_hash(p)
    print(before != after)   # True: the data changed, the hash shows it
```

DVC does this for you. These commands were run with DVC 3.67 in a throwaway git repository, using a local folder as the remote in place of the S3 bucket. `dvc add` wrote a pointer file holding the md5 hash and size and added the data file to `data/.gitignore`. After deleting the data file, `dvc pull` restored it.

```bash
dvc init
dvc add data/train.csv          # creates data/train.csv.dvc, ignores the big file in git
git add data/train.csv.dvc data/.gitignore
git commit -m "track training data"
dvc remote add -d storage s3://my-bucket/dvc
dvc push                        # upload data to the remote
dvc pull                        # on another machine, fetch the matching data
```

To go back to an old dataset, check out the old git commit and run `dvc checkout` or `dvc pull`.

## Three traps

1. Committing large data files into git. The repository becomes slow and huge.
2. Versioning data but not parameters and code version. The run is still not reproducible.
3. Treating the artifact store as a registry. Files with no names, versions or stages are hard to promote or roll back.

## What to say in an interview

Say: "I version data and models so any result can be reproduced from a commit. Git holds code and small pointer files. A remote holds the large files. A registry gives models names, versions and stages."

Do NOT claim:

- That DVC trains or tracks metrics by itself in the way MLflow does. It has experiment features, but its core job is versioning data and pipelines.
- That data versioning replaces good data quality checks.
- Experience with a real DVC remote if you have not used one.

## Three likely questions

**1. Why not just put the data in git?**
Git stores full copies of changed files and is slow with large ones. DVC keeps a small pointer in git and the data in remote storage, so history stays light and the data is still tied to a commit.

**2. How do you reproduce a model from six months ago?**
Check out the git commit for that model. It holds the code, the parameters and the data pointer. Pull the matching data and rerun the pipeline with the same seeds.

**3. What is the difference between a model registry and an artifact store?**
The artifact store holds files. The registry adds names, versions, stages and lineage on top. I use the registry to decide which version serves production and to roll back.
