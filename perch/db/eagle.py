"""os,json for parse metadata.json"""
import datetime
import json
import logging
import os

from flask import current_app


def parse_actress_name_id():
    """returns {actressname: eagleid}, or return None when failed parse"""
    with current_app.app_context():
        meta_path = current_app.config["LIB_PATH"] + "/metadata.json"
        logging.debug("  [DEBUG][parse_actress_name_id] meta_path = %s", meta_path)
        actress_name_id = {}
        # file exists?
        if not os.path.exists(meta_path):
            return None

        logging.debug("  [DEBUG][file open]")
        with open(meta_path, "r", encoding="utf-8") as file:
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
    meta_path = current_app.config["LIB_PATH"] + "/metadata.json"
    # file exists?
    if not os.path.exists(meta_path):
        return None
    taglist = []

    logging.debug("  [DEBUG][file open]")
    with open(meta_path, "r", encoding="utf-8") as file:
        json_meta = json.load(file)
        tags_groups = json_meta["tagsGroups"]
        for tag_group in tags_groups:
            taglist += tag_group["tags"]
    return taglist


def parse_file_metadata(dirpath):
    """returns {fileid:{filename: ,actressid: , tags: }}, or return None when failed parse"""
    path = dirpath + "/metadata.json"
    # file exists?
    if not os.path.exists(path):
        logging.warning("  [WARNING][parse] File not found on %s", path)
        return None

    logging.debug("  [DEBUG][file open]")
    with open(path, "r", encoding="utf-8") as file:
        logging.debug("  [DEBUG][parse] File found on %s", path)
        json_meta = json.load(file)
        star = 0
        try:
            star = json_meta["star"]
        except KeyError:
            pass
        metadata = {
            json_meta["id"]: {
                "filename": json_meta["name"],
                "actressid": json_meta["folders"],
                "tags": json_meta["tags"],
                "star": star,
            }
        }
        logging.debug("  [DEBUG][parse_file_metadata] parsed metadata : %s", metadata)
    return metadata


def parse_all_file_metadatas():
    """scan every images folder and get each metadata [{fileid:{filename:- ,actressid:- ,tags: }}, ...]"""
    file_metadatas = []
    path = f"{current_app.config['LIB_PATH']}/images"
    dirs = os.listdir(path=path)
    for tdir in dirs:
        targetpath = os.path.join(path, tdir)
        if os.path.isdir(targetpath):
            try:
                meta = parse_file_metadata(targetpath)
                if meta is not None:
                    file_metadatas.append(meta)
            except json.decoder.JSONDecodeError:
                pass
            except FileNotFoundError:
                pass
    return file_metadatas


# update file star data. if star is not exist in metadata.json file, add new line.
def update_file_star(file_id, star):
    """update file star data. if star is not exist in metadata.json file, add new line.
    return True when success, False when failed"""
    # get now with unix epoch time
    now = datetime.datetime.now()
    epoch_now = int(now.timestamp()) * 1000

    # update images metadata.json
    path = f"{current_app.config['LIB_PATH']}/images/{file_id}.info/metadata.json"
    with open(path, "r", encoding="utf-8") as file:
        json_meta = json.load(file)
        json_meta["star"] = star
        json_meta["lastModified"] = epoch_now
    if json_meta["star"] is None:
        return False
    with open(path, "w", encoding="utf-8") as file:
        json.dump(json_meta, file)

    # update latest modified file
    mtime_path = f"{current_app.config['LIB_PATH']}/mtime.json"
    with open(mtime_path, "r", encoding="utf-8") as file:
        json_mtimes = json.load(file)
        json_mtimes[file_id] = epoch_now
    with open(mtime_path, "w", encoding="utf-8") as file:
        json.dump(json_mtimes, file)

    return True
