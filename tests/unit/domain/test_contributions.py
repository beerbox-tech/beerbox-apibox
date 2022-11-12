"""
created by: thibault defeyter
created at: 2022/11/01
licene: MIT

unit testing of apibox contributions domain
"""

import pytest

from apibox.domain.contributions import ContributionDoesNotExist
from apibox.domain.contributions import ContributionUserDoesNotExist
from apibox.domain.contributions import InMemoryContributionRepository
from tests.factories import DomainContributionFactory
from tests.factories import DomainUserFactory


def test_repository_add_contribution():
    """test adding a contribution to the in memory repository"""
    user = DomainUserFactory.create(public_id="user-public-id")
    contribution = DomainContributionFactory.create(user_id="user-public-id")
    repository = InMemoryContributionRepository(users=[user])
    repository.add_contribution(contribution)
    assert repository.storage == [contribution]


def test_repository_add_contribution__already_exist():
    """test adding a contribution to the in memory repository"""
    user = DomainUserFactory.create(public_id="user-public-id")
    contribution = DomainContributionFactory.create(user_id="user-public-id")
    repository = InMemoryContributionRepository(users=[user], storage=[contribution])
    repository.add_contribution(contribution)
    assert repository.storage == [contribution, contribution]


def test_repository_add_contribution__failure():
    """test adding a contribution to the in memory repository"""
    contribution = DomainContributionFactory.create()
    repository = InMemoryContributionRepository()
    with pytest.raises(ContributionUserDoesNotExist):
        repository.add_contribution(contribution)
    assert repository.storage == []


def test_repository_get_contributions__empty():
    """test getting nothing from in memory repository"""
    repository = InMemoryContributionRepository()
    assert not repository.get_contributions()


def test_repository_get_contributions():
    """test fetching contributions from in memory repository"""
    contribution = DomainContributionFactory.create()
    repository = InMemoryContributionRepository(storage=[contribution])
    assert repository.get_contributions() == [contribution]


def test_repository_get_contribution__does_not_exist():
    """test getting nothing from in memory repository"""
    contribution = DomainContributionFactory.create()
    repository = InMemoryContributionRepository(storage=[contribution])
    with pytest.raises(ContributionDoesNotExist):
        repository.get_contribution(public_id="does-not-exist")


def test_repository_get_contribution__exists():
    """test getting nothing from in memory repository"""
    contribution = DomainContributionFactory.create()
    repository = InMemoryContributionRepository(storage=[contribution])
    assert repository.get_contribution(public_id=contribution.public_id) == contribution
