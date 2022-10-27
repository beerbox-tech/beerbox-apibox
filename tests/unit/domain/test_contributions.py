"""
created by: thibault defeyter
created at: 2022/10/28
licene: MIT

unit testing of beerbox contributions domain
"""
from datetime import datetime

import pytest

from beerbox.domain.contributions import Contribution
from beerbox.domain.contributions import ContributionAlreadyExist
from beerbox.domain.contributions import ContributionDoesNotExist
from beerbox.domain.contributions import InMemoryContributionRepository


@pytest.fixture(name="contribution", scope="session")
def fixture_contribution():
    """expose a host fixture"""
    return Contribution(
        amount=10,
        created_at=datetime(2020, 1, 1),
        modified_at=datetime(2020, 1, 1),
        public_id="id",
        username="user",
    )


def test_repository_add_contribution(contribution):
    """test adding a contribution to the in memory repository"""
    repository = InMemoryContributionRepository()
    repository.add_contribution(contribution)
    assert repository.storage == {contribution.public_id: contribution}


def test_repository_add_contribution__already_exist(contribution):
    """test adding a contribution to the in memory repository"""
    repository = InMemoryContributionRepository(storage={contribution.public_id: contribution})
    with pytest.raises(ContributionAlreadyExist):
        repository.add_contribution(contribution)


def test_repository_get_contributions__empty():
    """test getting nothing from in memory repository"""
    repository = InMemoryContributionRepository()
    assert not repository.get_contributions()


def test_repository_get_contributions__full(contribution):
    """test fetching contributions from in memory repository"""
    repository = InMemoryContributionRepository(storage={contribution.public_id: contribution})
    assert repository.get_contributions() == [contribution]


def test_repository_get_contributions__full_not_matching(contribution):
    """test fetching contributions from in memory repository"""
    repository = InMemoryContributionRepository(storage={contribution.public_id: contribution})
    assert repository.get_contributions(username="does-not-exist") == []


def test_repository_get_contribution__does_not_exist(contribution):
    """test getting nothing from in memory repository"""
    repository = InMemoryContributionRepository(storage={contribution.public_id: contribution})
    with pytest.raises(ContributionDoesNotExist):
        repository.get_contribution(public_id="does-not-exist")


def test_repository_get_contribution__exists(contribution):
    """test getting nothing from in memory repository"""
    repository = InMemoryContributionRepository(storage={contribution.public_id: contribution})
    assert repository.get_contribution(public_id=contribution.public_id) == contribution
