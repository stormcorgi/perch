"""os,json for parse metadata.json"""
import json
import os
import logging
from flask import current_app


def parse_actress_name_id():
    """returns {actressname: eagleid}, or return None when failed parse"""
    with current_app.app_context():
        meta_path = current_app.config['LIB_PATH'] + "/metadata.json"
        logging.debug(
            "  [DEBUG][parse_actress_name_id] meta_path = %s", meta_path)
        actress_name_id = {}
        # file exists?
        if not os.path.exists(meta_path):
            return None

        logging.debug("  [DEBUG][file open]")
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


def parse_all_tags(lib_path=None):
    """returns ["tag name itself"], or return None when failed parse"""
    if lib_path is None:
        with current_app.app_context():
            lib_path = current_app.config['LIB_PATH_VIDEO']
    meta_path = lib_path + "/metadata.json"
    if not os.path.exists(meta_path):
        return None
    with open(meta_path, 'r', encoding='utf-8') as file:
        json_meta = json.load(file)
        tags_groups = json_meta.get("tagsGroups", [])
        taglist = []
        for tag_group in tags_groups:
            taglist += tag_group.get("tags", [])
    return taglist


def parse_file_metadata(dirpath):
    """returns {fileid:{filename:, ext:, size:, mtime:, tags:}}, or return None"""
    path = dirpath + "/metadata.json"
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as file:
            json_meta = json.load(file)
    except (json.decoder.JSONDecodeError, OSError):
        return None
    return {
        json_meta["id"]: {
            "filename": json_meta.get("name", ""),
            "ext": json_meta.get("ext", ""),
            "size": json_meta.get("size", 0),
            "mtime": json_meta.get("mtime", 0),
            "tags": json_meta.get("tags", []),
        }
    }


def parse_all_file_metadatas(lib_path=None):
    """scan images/ under lib_path, return list of {fileid: {filename, ext, ...}}.
    When lib_path is omitted, use current app's video LIB_PATH (backward compat)."""
    if lib_path is None:
        with current_app.app_context():
            lib_path = current_app.config['LIB_PATH_VIDEO']
    path = f"{lib_path}/images"
    if not os.path.isdir(path):
        return []
    file_metadatas = []
    for tdir in os.listdir(path=path):
        targetpath = os.path.join(path, tdir)
        if os.path.isdir(targetpath):
            try:
                meta = parse_file_metadata(targetpath)
                if meta is not None:
                    file_metadatas.append(meta)
            except (json.decoder.JSONDecodeError, FileNotFoundError, OSError):
                pass
    return file_metadatas
