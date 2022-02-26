"""os,json for parse metadata.json"""
import json
import os


def get_actress_name_id():
    """returns {actressname: eagleid}"""
    actress_name_id = {}

    with open(
        './static/eagle_library/metadata.json',
        'r',
        encoding='utf-8'
    ) as file:
        json_meta = json.load(file)
        folders = json_meta["folders"]
        for folder in folders:
            # print(folder["name"])
            childrens = folder["children"]
            for child in childrens:
                # print("  --> name : " + child["name"])
                # print("  --> id : " + child["id"])
                actress_name_id[child["name"]] = child["id"]
        # print(actress_name_id)
    return actress_name_id


def get_all_tags():
    """returns ["tag name itself"]"""
    taglist = []
    with open(
        './static/eagle_library/metadata.json',
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


def get_all_file_metadatas():
    """ scan every images folder and get each metadata """
    file_metadatas = []
    path = "./static/eagle_library/images"
    dirs = os.listdir(path=path)
    for tdir in dirs:
        if os.path.isdir(os.path.join(path, tdir)):
            try:
                targetpath = "./static/eagle_library/images/" + tdir
                file_metadatas.append(get_file_metadata(targetpath))
            except json.decoder.JSONDecodeError:
                pass
            except FileNotFoundError:
                pass
    return file_metadatas


if __name__ == "__main__":
    print(
        get_file_metadata("./static/eagle_library/images/KYDUNFM9D6PEC.info")
    )
    # print(get_all_tags())
    # print(get_all_file_metadatas())
