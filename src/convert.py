import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil
from glob import glob
import xmltodict
import imagesize
import cv2

from tqdm import tqdm


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def create_ann(image_path):
    labels = []
    ann_path = os.path.join(
        os.path.dirname(image_path), (sly.fs.get_file_name(image_path) + ".xml")
    )
    width, height = imagesize.get(image_path)

    if os.path.exists(ann_path):
        with open(ann_path, "r") as f:
            xml_content = f.read()
        try:
            xmldict = xmltodict.parse(xml_content)
        except Exception as e:
            sly.logger.warning(e)
            return sly.Annotation(img_size=(height, width), labels=labels)
        img_width = int(xmldict["annotation"]["size"]["width"])
        img_height = int(xmldict["annotation"]["size"]["height"])

        if (img_width, img_height) != (width, height):
            print("Image has the wrong size")
            return sly.Annotation(img_size=(height, width), labels=labels)

        if type(xmldict["annotation"]["object"]) == dict:
            keys = [xmldict["annotation"]["object"]["name"]]
            values = [xmldict["annotation"]["object"]["bndbox"].values()]
        else:
            keys = [obj["name"] for obj in xmldict["annotation"]["object"]]
            values = [obj["bndbox"].values() for obj in xmldict["annotation"]["object"]]

        for k, v in zip(keys, values):
            xmin, ymin, xmax, ymax = v
            obj_class = oc_dict.get(k)

            rectangle = sly.Rectangle(
                top=int(ymin), left=int(xmin), bottom=int(ymax), right=int(xmax)
            )
            label = sly.Label(rectangle, obj_class)
            labels.append(label)
    else:
        img_width, img_height = (width, height)

    return sly.Annotation(img_size=(img_height, img_width), labels=labels)


batch_size = 50

oc_dict = {
    "ambulance": sly.ObjClass("ambulance", geometry_type=sly.Rectangle, color=[0, 0, 255]),
    "army vehicle": sly.ObjClass("army vehicle", geometry_type=sly.Rectangle, color=[0, 255, 255]),
    "auto rickshaw": sly.ObjClass("auto rickshaw", geometry_type=sly.Rectangle, color=[0, 255, 0]),
    "bicycle": sly.ObjClass("bicycle", geometry_type=sly.Rectangle, color=[255, 0, 0]),
    "bus": sly.ObjClass("bus", geometry_type=sly.Rectangle, color=[255, 128, 0]),
    "car": sly.ObjClass("car", geometry_type=sly.Rectangle, color=[255, 0, 255]),
    "garbagevan": sly.ObjClass("garbagevan", geometry_type=sly.Rectangle, color=[255, 255, 0]),
    "human hauler": sly.ObjClass("human hauler", geometry_type=sly.Rectangle, color=[128, 0, 255]),
    "minibus": sly.ObjClass("minibus", geometry_type=sly.Rectangle, color=[0, 255, 191]),
    "minivan": sly.ObjClass("minivan", geometry_type=sly.Rectangle, color=[128, 255, 0]),
    "motorbike": sly.ObjClass("motorbike", geometry_type=sly.Rectangle, color=[255, 0, 191]),
    "pickup": sly.ObjClass("pickup", geometry_type=sly.Rectangle, color=[255, 102, 255]),
    "policecar": sly.ObjClass("policecar", geometry_type=sly.Rectangle, color=[0, 204, 102]),
    "rickshaw": sly.ObjClass("rickshaw", geometry_type=sly.Rectangle, color=[255, 80, 80]),
    "scooter": sly.ObjClass("scooter", geometry_type=sly.Rectangle, color=[153, 0, 204]),
    "suv": sly.ObjClass("suv", geometry_type=sly.Rectangle, color=[153, 102, 51]),
    "taxi": sly.ObjClass("taxi", geometry_type=sly.Rectangle, color=[0, 153, 0]),
    "three wheelers (CNG)": sly.ObjClass(
        "three wheelers (CNG)", geometry_type=sly.Rectangle, color=[153, 255, 51]
    ),
    "truck": sly.ObjClass("truck", geometry_type=sly.Rectangle, color=[255, 102, 153]),
    "van": sly.ObjClass("van", geometry_type=sly.Rectangle, color=[0, 153, 255]),
    "wheelbarrow": sly.ObjClass("wheelbarrow", geometry_type=sly.Rectangle, color=[204, 0, 204]),
}


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ann_pathes = glob("/mnt/c/users/german/documents/dhaka/train/Final Train Dataset/*.xml")

    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta(obj_classes=list(oc_dict.values()))
    api.project.update_meta(project.id, meta.to_json())

    dataset_path = "/mnt/c/users/german/documents/dhaka"
    dataset_names = {
        "train": "train/Final Train Dataset",
        "test": "test/test",
        "test2": "test round 2/test round 2",
    }

    for ds, path in dataset_names.items():
        dataset = api.dataset.create(project.id, ds, change_name_if_conflict=True)
        images_pathes = [
            filename
            for filename in glob(os.path.join(dataset_path, path, "*"))
            if not filename.endswith("xml")
        ]
        progress = sly.Progress("Create dataset {}".format(ds), len(images_pathes))
        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            img_names_batch = [
                sly.fs.get_file_name_with_ext(im_path) for im_path in img_pathes_batch
            ]
            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]
            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)
    return project
