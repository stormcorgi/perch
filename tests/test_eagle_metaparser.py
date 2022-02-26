from app.eagle_metaparser import get_actress_name_id, get_all_tags, get_file_metadata, get_all_file_metadatas
from tests.conftest import sample_lib


def test_get_actress_name_id():
    """parse master metadata.json, get {actress name: actressid}"""
    actresses = get_actress_name_id(sample_lib)
    assert actresses["human"] == "L03BJZ6UJU790"
    assert len(actresses) == 5


def test_get_all_tags():
    """parse master metadata.json, get tag[]"""
    tags = get_all_tags(sample_lib)
    assert tags[0] == "animal"
    assert len(tags) == 15


def test_get_file_metadata():
    """parse file's metadata.json, get """
    fileid = "L03BG2NLB8U1I"
    meta = get_file_metadata(
        f"{sample_lib}/images/{fileid}.info")
    assert meta[fileid]["filename"] == "kLpTMbSKGi4"
    assert meta[fileid]["actressid"][0] == "L03BHPEH9SNKO"
    assert meta[fileid]["tags"][0] == "cycle"
    assert meta[fileid]["tags"][1] == "road"


def test_get_all_file_metadatas():
    """parse master metadata.json, get tag[]"""
    metadatas = get_all_file_metadatas(sample_lib)
    assert metadatas[0]["L03BG2NLNXQOK"]["filename"] == "1vv6rPwy-kk"
    assert metadatas[0]["L03BG2NLNXQOK"]["actressid"][0] == "L03BHPEH9SNKO"
    assert metadatas[0]["L03BG2NLNXQOK"]["tags"][0] == "night"
