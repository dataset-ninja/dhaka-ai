Dataset **Dhaka-AI** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMjQzMl9EaGFrYS1BSS9kaGFrYS1haS1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICIrYXBZSVk5TXdOWlA1MG1ZdE5DemFYSXRJWEYvdVgvRUNQdWRBRnJjNkVrPSJ9?response-content-disposition=attachment%3B%20filename%3D%22dhaka-ai-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Dhaka-AI', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/rifat963/dhakaai-dhaka-based-traffic-detection-dataset/download?datasetVersionNumber=2).