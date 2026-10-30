# CI/CD Final Project - Counter Service

**Project name:** CI/CD Final Project: Counter Service with GitHub Actions, Tekton and OpenShift Pipelines

A small Flask microservice that manages named counters, used to demonstrate a full CI/CD pipeline:

- **GitHub Actions** - lint with `flake8` and run unit tests with `nose` on every push / pull request
- **Tekton** - tasks (`cleanup`, `flake8`, `nose`) and a pipeline that run on OpenShift
- **OpenShift Pipelines** - PersistentVolumeClaim workspace, pipeline run, build and deploy

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /counters/<name> | Create a counter (409 if exists) |
| GET | /counters/<name> | Read a counter |
| PUT | /counters/<name> | Increment a counter |
| DELETE | /counters/<name> | Delete a counter |

## Run locally
```bash
pip install -r requirements.txt
flask --app service:app run
nosetests
flake8 service tests --max-line-length=127
```

## Repository layout
```
.github/workflows/workflow.yml   GitHub Actions CI
.tekton/tasks.yml                Tekton tasks (cleanup, flake8, nose)
.tekton/pipeline.yml             Tekton pipeline
.tekton/pvc.yml                  PersistentVolumeClaim for the pipeline workspace
service/                         Flask application
tests/                           Unit tests
```

## OpenShift commands
```bash
oc apply -f .tekton/pvc.yml
oc apply -f .tekton/tasks.yml
oc apply -f .tekton/pipeline.yml
tkn pipeline start cd-pipeline -p repo-url="<YOUR_REPO_URL>" -p branch=main \
    -p build-image="image-registry.openshift-image-registry.svc:5000/$SN_ICR_NAMESPACE/counter:latest" \
    -w name=pipeline-workspace,claimName=pipelinerun-pvc --showlog
oc get pvc pipelinerun-pvc
oc logs deployment/counter-service
```
