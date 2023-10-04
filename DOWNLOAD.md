Dataset **Dhaka-AI** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/f/Q/mX/xDbygzFBtEAH4jWj0Qrwf140O7Y0Pa5zn2WVlczUuakI7i6igk10UZif5rDe9AcOZ6tTsaKEuAaeTCA0GZW4E61uzQXcWht86lAv8GehijXBU54M3V2fAt5J3nr0.tar)

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