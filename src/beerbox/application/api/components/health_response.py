"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox api health response
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

from beerbox import config
from beerbox.application.api.components.base import APIComponent
from beerbox.application.health import Check
from beerbox.application.health import Status


class CheckComponent(APIComponent):
    """API component representing a healtch check"""

    name: str
    time: datetime
    status: Status
    observed_value: str
    observed_unit: str

    @classmethod
    def from_check(cls, check: Check) -> CheckComponent:
        """create an api component from a health check"""
        return cls(**asdict(check))


class HealthResponse(APIComponent):
    """API component representing a healt check response"""

    status: Status
    checks: list[CheckComponent]
    version: str
    service: str

    @classmethod
    def from_checks(cls, checks: list[Check]) -> HealthResponse:
        """transform a list of application checks into a healtch check response"""
        version = config.VERSION
        service = config.SERVICE
        return cls(
            status=Status.all(check.status for check in checks),
            checks=[CheckComponent.from_check(check) for check in checks],
            version=version,
            service=service,
        )
