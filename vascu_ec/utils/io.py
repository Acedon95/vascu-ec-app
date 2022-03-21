import glob
import os
from pathlib import Path
import pandas as pd
import numpy as np
import skimage.io
import yaml


def read_parameters(parameter_file):
    """Reads in default parameters and replaces user defined parameters."""
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    param_base_file = Path(current_path).joinpath("base", "parameters.yml")

    with open(param_base_file, 'r') as yml_f:
        parameters = yaml.safe_load(yml_f)

    with open(parameter_file) as file:
        parameters_local = yaml.safe_load(file)

    # overwrite global parameters with local setting
    for key in parameters_local:
        parameters[key] = parameters_local[key]

    return parameters


def read_image(filename):
    """Reads an image and reshapes to channel last."""
    img_ = skimage.io.imread(filename)

    print("Loading image of shape:", img_.shape)

    if len(img_.shape) <= 2:
        img_ = np.array([img_, img_])

    if img_.shape[0] < min(img_.shape[1], img_.shape[2]):
        print("Warning: channel is on the first dimension of the image.")
        img = np.swapaxes(np.swapaxes(img_,0,2),0,1)
    else:
        img = img_

    return img


def write_dict_to_yml(yml_file, d):
    """Writes a dictionary to a file in yml format."""
    yml_file = Path(yml_file)
    p = Path(yml_file.parent)
    p.mkdir(parents=True, exist_ok=True)

    with open(yml_file, 'w+') as yml_f:
        yml_f.write(yaml.dump(d, Dumper=yaml.Dumper))

    return True


def create_path_recursively(path):
    """Creates a path. Creates missing parent folders."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    return True


def get_tif_list(path):
    path = str(path)
    if not path.endswith(os.path.sep):
        path = path + os.path.sep

    return glob.glob(path + "*.tif")


def read_key_file(path):
    return pd.read_csv(path)


def list_files_recursively(path, root=None, relative=False) -> list:
    """Lists all files in a repository recursively"""
    path = Path(path)
    if not root:
        root = path
    files_list = []

    for cur_root, dirs, files in os.walk(path):
        cur_root = Path(cur_root)

        for d in dirs:
            files_list += list_files_recursively(cur_root.joinpath(d), root, relative)
        for fi in files:
            if relative:
                files_list.append(cur_root.joinpath(fi).relative_to(root))
            else:
                files_list.append(cur_root.joinpath(fi))
        break

    return files_list
