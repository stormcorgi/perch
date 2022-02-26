"""load eagle_metaparser, tests.conftest for static path"""
from app.eagle_metaparser import get_actress_name_id, get_all_tags
from app.eagle_metaparser import get_file_metadata, get_all_file_metadatas
from tests.conftest import SAMPLE_LIB


def test_get_actress_name_id():
    """parse master metadata.json, get {actress name: actressid}"""
    actresses = get_actress_name_id(SAMPLE_LIB)
    assert actresses["human"] == "L03BJZ6UJU790"
    assert len(actresses) == 5


def test_get_all_tags():
    """parse master metadata.json, get tag[]"""
    tags = get_all_tags(SAMPLE_LIB)
    assert tags[0] == "animal"
    assert len(tags) == 15


def test_get_file_metadata():
    """parse file's metadata.json, get """
    fileid = "L03BG2NLB8U1I"
    meta = get_file_metadata(
        f"{SAMPLE_LIB}/images/{fileid}.info")
    assert meta[fileid]["filename"] == "kLpTMbSKGi4"
    assert meta[fileid]["actressid"][0] == "L03BHPEH9SNKO"
    assert meta[fileid]["tags"][0] == "cycle"
    assert meta[fileid]["tags"][1] == "road"


def test_get_all_file_metadatas():
    """parse master metadata.json, get tag[]"""
    fileid = "L03BG2NLNXQOK"
    metadatas = get_all_file_metadatas(SAMPLE_LIB)
    for metadata in metadatas:
        if fileid in metadata:
            assert metadata[fileid]["filename"] == "1vv6rPwy-kk"
            assert metadata[fileid]["actressid"][0] == "L03BHPEH9SNKO"
            assert metadata[fileid]["tags"][0] == "night"
