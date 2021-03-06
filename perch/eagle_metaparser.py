"""os,json for parse metadata.json"""
import json
import os
from flask import current_app


def parse_actress_name_id():
    """returns {actressname: eagleid}, or return None when failed parse"""
    with current_app.app_context():
        meta_path = current_app.config['LIB_PATH'] + "/metadata.json"
        actress_name_id = {}
        # file exists?
        if not os.path.exists(meta_path):
            return None

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


def parse_all_tags():
    """returns ["tag name itself"], or return None when failed parse"""
    meta_path = current_app.config['LIB_PATH'] + "/metadata.json"
    # file exists?
    if not os.path.exists(meta_path):
        return None
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


def parse_file_metadata(dirpath):
    """returns {fileid : filename}, or return None when failed parse"""
    path = dirpath + "/metadata.json"
    # file exists?
    if not os.path.exists(path):
        return None
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


def parse_all_file_metadatas():
    """ scan every images folder and get each metadata """
    file_metadatas = []
    path = f"{current_app.config['LIB_PATH']}/images"
    dirs = os.listdir(path=path)
    for tdir in dirs:
        targetpath = os.path.join(path, tdir)
        if os.path.isdir(targetpath):
            try:
                file_metadatas.append(parse_file_metadata(targetpath))
            except json.decoder.JSONDecodeError:
                pass
            except FileNotFoundError:
                pass
    return file_metadatas
