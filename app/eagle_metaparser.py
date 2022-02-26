"""os,json for parse metadata.json"""
import json
import os


def get_actress_name_id(lib_path="./static/eagle_library"):
    """returns {actressname: eagleid}"""
    meta_path = lib_path + "/metadata.json"
    actress_name_id = {}

    with open(
        meta_path,
        'r',
        encoding='utf-8'
    ) as file:
        json_meta = json.load(file)
        # TODO adopt another folder structure. current: category - actress
        folders = json_meta["folders"]
        for folder in folders:
            childrens = folder["children"]
            for child in childrens:
                actress_name_id[child["name"]] = child["id"]
    return actress_name_id


def get_all_tags(lib_path="./static/eagle_library"):
    """returns ["tag name itself"]"""
    meta_path = lib_path + "/metadata.json"
    taglist = []
    with open(
        meta_path,
        'r',
        encoding='utf-8'
    ) as file:
        json_meta = json.load(file)
        tags_groups = json_meta["tagsGroups"]
        for tag_group in tags_groups:
            taglist += tag_group["tags"]
    return taglist


def get_file_metadata(dirpath):
    """returns {fileid : filename}"""
    path = dirpath + "/metadata.json"
    with open(path, 'r', encoding='utf-8') as file:
        json_meta = json.load(file)
        metadata = {
            json_meta["id"]: {
                "filename": json_meta["name"],
                "actressid": json_meta["folders"],
                "tags": json_meta["tags"]
            }
        }
    return metadata


def get_all_file_metadatas(lib_path="./static/eagle_library"):
    """ scan every images folder and get each metadata """
    file_metadatas = []
    path = f"{lib_path}/images"
    dirs = os.listdir(path=path)
    for tdir in dirs:
        targetpath = os.path.join(path, tdir)
        if os.path.isdir(targetpath):
            try:
                file_metadatas.append(get_file_metadata(targetpath))
            except json.decoder.JSONDecodeError:
                pass
            except FileNotFoundError:
                pass
    return file_metadatas


if __name__ == "__main__":
    pass
    # print(get_all_tags())
    # print(get_all_file_metadatas()
