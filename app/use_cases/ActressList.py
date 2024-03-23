from app.domain.Folder import Folder
from app.repository.IFolderRepo import IFolderRepo


def actress_list_use_case(repo: IFolderRepo) -> list[Folder]:
    return repo.list()
