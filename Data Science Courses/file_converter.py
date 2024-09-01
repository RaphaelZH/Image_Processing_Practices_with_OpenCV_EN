from datetime import datetime
from functools import wraps
from ipynbcompress import compress
import nbformat
import pandas as pd
from pathlib import Path
import pytz


def hidden_file_cleaner(path_object):
    if Path(str(path_object).rstrip("/") + "/.DS_Store").exists():
        path_object = Path(str(path_object).rstrip("/") + "/.DS_Store")
        path_object.unlink()


def date_format(stat_time):
    return datetime.fromtimestamp(stat_time, tz=pytz.timezone("cet"))


def alteration_monitor(index, file_object, recorded_size, recorded_time):
    global alterations_dict
    # Statement 4: If condition 4 is True, update the modification date information and size
    # information of the file to the corresponding entry in the record, and likewise record its
    # corresponding index in the list of indexes dedicated to recording altered or newly added
    # entries.
    if str(date_format(file_object.stat().st_mtime)) != recorded_time.item():
        recorded_size = f"{file_object.stat().st_size:,}"
        recorded_time = str(date_format(file_object.stat().st_mtime))
        alterations_dict[index] = str(file_object)
        return recorded_size, recorded_time
    else:
        return recorded_size.item(), recorded_time.item()


def notebook_selector(path_object):
    return [
        file_object.name
        for file_object in sorted(path_object.iterdir())
        if (
            file_object.name.split(".")[-1] == "ipynb"
            and file_object.name.find("(Compressed)") == -1
        )
    ]


def info_collector(course, subpath, file_name, info_dict):
    info_dict["File Path"].append(course)
    info_dict["File Name"].append(file_name)
    file_object = Path(f"{subpath}/" + file_name)
    info_dict["File Size"].append(f"{file_object.stat().st_size:,}")
    info_dict["Modification Date"].append(str(date_format(file_object.stat().st_mtime)))
    for key in ["Compressed File", "Compressed Size", "Compressed Date"]:
        info_dict[key].append("")
    return info_dict


def dataframe_creation():
    global courses_list, dir_notebook
    info_dict = {
        "File Path": [],
        "File Name": [],
        "File Size": [],
        "Modification Date": [],
        "Compressed File": [],
        "Compressed Size": [],
        "Compressed Date": [],
    }
    for course in courses_list:
        hidden_file_cleaner(Path(course))
        path_object = Path(course.join(dir_notebook))
        hidden_file_cleaner(path_object)
        for subpath_object in sorted(path_object.iterdir()):
            hidden_file_cleaner(subpath_object)
            subpath = str(subpath_object)
            file_list = notebook_selector(subpath_object)
            for file_name in file_list:
                info_dict = info_collector(course, subpath, file_name, info_dict)
    return pd.DataFrame.from_dict(data=info_dict)


def file_checker(func):
    @wraps(func)
    def wrapper():
        global alterations_dict, courses_list, csv_object, dir_notebook
        # Condition 1: Check whether there exists a record for all Jupyter Notebook files in
        # the current directory.
        if csv_object.is_file():
            # Condition 2: If Condition 1 is True, read this record and check whether there are
            # certain entries in this record for which the corresponding Jupyter Notebook file
            # cannot be found.
            df = pd.read_csv(csv_object)
            combined_list = []
            for course in courses_list:
                hidden_file_cleaner(Path(course))
                path_object = Path(course.join(dir_notebook))
                hidden_file_cleaner(path_object)
                for subpath_object in sorted(path_object.iterdir()):
                    combined_list.append((course, subpath_object.name + ".ipynb"))
            for index, row in df.iterrows():
                if (row["File Path"], row["File Name"]) not in combined_list:
                    # Statement 2: If Condition 2 is True, delete these entries and eventually
                    # reset the index.
                    df.drop(axis=0, index=index, inplace=True)
            df.reset_index()
            info_dict = df.to_dict(orient="list")
            # Condition 3: Regardless of whether Condition 2 is True or False, check whether
            # there are any Jupyter Notebook files in the current directory that do not have
            # a corresponding entry in this record.
            for course in courses_list:
                path_object = Path(course.join(dir_notebook))
                for subpath_object in sorted(path_object.iterdir()):
                    hidden_file_cleaner(subpath_object)
                    subpath = str(subpath_object)
                    file_list = notebook_selector(subpath_object)
                    for file_name in file_list:
                        file_path = f"{subpath}/" + file_name
                        # Statement 3: If condition 3 is True, the information relating to the
                        # file will be added to the record as the most recent entry, and its
                        # corresponding indexes will be recorded separately in a list of
                        # indexes dedicated to recording altered or newly added entries.
                        if (
                            file_name
                            not in df.loc[df["File Path"] == course][
                                "File Name"
                            ].to_list()
                        ):
                            info_dict = info_collector(
                                course, subpath, file_name, info_dict
                            )

                            ###
                            df = pd.DataFrame.from_dict(data=info_dict)
                            target_index = df.shape[0] - 1
                            alterations_dict[target_index] = file_path
                        # Condition 4: If condition 3 is False, check whether the actual
                        # modification date of the file is the same as the modification date
                        # recorded for the corresponding entry in the record.
                        else:
                            target_index = df.index[
                                (df["File Path"] == course)
                                & (df["File Name"] == file_name)
                            ].tolist()[0]
                            df.loc[
                                (df["File Path"] == course)
                                & (df["File Name"] == file_name),
                                ["File Size", "Modification Date"],
                            ] = alteration_monitor(
                                target_index,
                                Path(file_path),
                                df.loc[
                                    (df["File Path"] == course)
                                    & (df["File Name"] == file_name),
                                    "File Size",
                                ],
                                df.loc[
                                    (df["File Path"] == course)
                                    & (df["File Name"] == file_name),
                                    "Modification Date",
                                ],
                            )
            for key, value in alterations_dict.items():
                df.loc[key, "Compressed File"] = func(value)
        else:
            # Statement 1: If Condition 1 is False, create a record for all Jupyter Notebook
            # files in the current directory immediately, while generating the corresponding
            # pre-compressed copy for each file as well as compressing any copies that exceed
            # the preset size limit, and recording relevant information about the copies.
            df = dataframe_creation()
            for index, row in df.iterrows():
                subpath = (
                    row["File Path"].join(dir_notebook)
                    + row["File Name"].split(".ipynb")[0]
                )
                file_path = subpath + "/" + row["File Name"]
                df.loc[index, "Compressed File"] = func(file_path)
                alterations_dict[index] = file_path
        return df, alterations_dict

    return wrapper


def compression_record(func):
    @wraps(func)
    def wrapper():
        global csv_object
        df, alterations_dict = func()
        if not df.empty:
            for index, row in df.iterrows():
                if index in alterations_dict.keys():
                    compressed_file_path = " (Compressed).ipynb".join(
                        alterations_dict[index].split(".ipynb")
                    )
                    compressed_file_object = Path(compressed_file_path)
                    scale = 1
                    while compressed_file_object.stat().st_size > 15 * (10**6):
                        compress(
                            alterations_dict[index],
                            compressed_file_path,
                            img_width=800 - 40 * scale,
                            img_format="png",
                        )
                        scale += 1
                    df.loc[index, "Compressed Size"] = (
                        f"{compressed_file_object.stat().st_size:,}"
                    )
                    df.loc[index, "Compressed Date"] = str(
                        date_format(compressed_file_object.stat().st_mtime)
                    )

        # Statement 6: Sorts the updated record and resets its index.
        df = df.sort_values(by=["File Path", "File Name"])
        df.reset_index()
        df.to_csv(csv_object, index=False)

    return wrapper


@compression_record
@file_checker
def file_generator(original_file_path):
    compressed_file_path = " (Compressed).ipynb".join(
        original_file_path.split(".ipynb")
    )
    compress(original_file_path, compressed_file_path, img_width=800, img_format="png")
    return compressed_file_path.split("/")[-1]


alterations_dict = {}

courses_list = [
    "Deep Learning with PyTorch for Medical Image Analysis",
    "Modern Computer Vision PyTorch, TensorFlow 2 Keras & OpenCV 4",
    "PyTorch for Deep Learning and Computer Vision",
]

csv_object = Path("modification_record.csv")

dir_notebook = ["./", "/Notebooks/"]

file_generator()
