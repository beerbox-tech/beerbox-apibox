"""
created by: thibault defeyter
created at: 2022/02/04
licene: MIT

unit testing of apibox boxes domain
"""


import pytest

from apibox.domain.boxes import BoxAlreadyExist
from apibox.domain.boxes import BoxDoesNotExist
from apibox.domain.boxes import InMemoryBoxRepository
from tests.factories import DomainBoxFactory


def test_repository_add_box():
    """test adding a box to the in memory repository"""
    box = DomainBoxFactory.create()
    repository = InMemoryBoxRepository()
    repository.add_box(box)
    assert repository.storage == {box.public_id: box}


def test_repository_add_box__already_exist():
    """test adding a box to the in memory repository"""
    box = DomainBoxFactory.create()
    repository = InMemoryBoxRepository(storage={box.public_id: box})
    with pytest.raises(BoxAlreadyExist):
        repository.add_box(box)


def test_repository_get_boxes__empty():
    """test getting nothing from in memory repository"""
    repository = InMemoryBoxRepository()
    assert not repository.get_boxes()


def test_repository_get_boxes__full():
    """test fetching boxes from in memory repository"""
    box = DomainBoxFactory.create()
    repository = InMemoryBoxRepository(storage={box.public_id: box})
    assert repository.get_boxes() == [box]


def test_repository_get_box__does_not_exist():
    """test getting nothing from in memory repository"""
    box = DomainBoxFactory.create()
    repository = InMemoryBoxRepository(storage={box.public_id: box})
    with pytest.raises(BoxDoesNotExist):
        repository.get_box(public_id="does-not-exist")


def test_repository_get_box__exists():
    """test getting nothing from in memory repository"""
    box = DomainBoxFactory.create()
    repository = InMemoryBoxRepository(storage={box.public_id: box})
    assert repository.get_box(public_id=box.public_id) == box
