"""load eagle_metaparser, tests.conftest for static path"""
from flask import current_app
from perch.eagle_metaparser import parse_actress_name_id, parse_all_tags
from perch.eagle_metaparser import parse_file_metadata, parse_all_file_metadatas


def test_parse_actress_name_id(app):
    """parse master metadata.json, parse {actress name: actressid}"""
    with app.app_context():
        actresses = parse_actress_name_id()
        assert actresses["human"] == "L03BJZ6UJU790"
        assert len(actresses) == 5


def test_parse_all_tags(app):
    """parse master metadata.json, parse tag[]"""
    with app.app_context():
        tags = parse_all_tags()
        assert tags[0] == "animal"
        assert len(tags) == 15


def test_parse_file_metadata(app):
    """parse file's metadata.json, parse """
    with app.app_context():
        lib_path = current_app.config["LIB_PATH"]
        fileid = "L03BG2NLB8U1I"
        meta = parse_file_metadata(
            f"{lib_path}/images/{fileid}.info")
        assert meta[fileid]["filename"] == "kLpTMbSKGi4"
        assert meta[fileid]["actressid"][0] == "L03BHPEH9SNKO"
        assert meta[fileid]["tags"][0] == "cycle"
        assert meta[fileid]["tags"][1] == "road"


def test_parse_all_file_metadatas(app):
    """parse master metadata.json, parse tag[]"""
    with app.app_context():
        fileid = "L03BG2NLNXQOK"
        metadatas = parse_all_file_metadatas()
        for metadata in metadatas:
            if fileid in metadata:
                assert metadata[fileid]["filename"] == "1vv6rPwy-kk"
                assert metadata[fileid]["actressid"][0] == "L03BHPEH9SNKO"
                assert metadata[fileid]["tags"][0] == "night"
