import json
import os


def get_actress_name_id():  # returns {actressname : eagleid}
    actress_name_id = {}

    with open('./static/eagle_library/metadata.json', 'r') as f:
        json_meta = json.load(f)
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


def get_all_tags():  # returns ["tag name itself"]
    taglist = []
    with open('./static/eagle_library/metadata.json', 'r') as f:
        json_meta = json.load(f)
        tagsGroups = json_meta["tagsGroups"]
        for tg in tagsGroups:
            taglist += tg["tags"]
    return taglist


# returns {fileid : filename}
def get_file_metadata(dirpath):
    p = dirpath + "/metadata.json"
    with open(p, 'r') as f:
        json_meta = json.load(f)
        metadata = {
            json_meta["id"]: {
                "filename": json_meta["name"],
                "actressid": json_meta["folders"],
                "tags": json_meta["tags"]
            }
        }
    return metadata


def get_all_file_metadatas():
    file_metadatas = []
    p = "./static/eagle_library/images"
    dirs = os.listdir(path=p)
    for d in dirs:
        if os.path.isdir(os.path.join(p, d)):
            try:
                targetpath = "./static/eagle_library/images/" + d
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
