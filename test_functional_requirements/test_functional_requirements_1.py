"""
Tests for Cobweb Project functional requirements, section 1.

The Cobweb platform SHALL support features necessary to enable meaningful
collaborative collection development activities for web archives.

Based on version 2018-03-01_tests
"""

import pytest


# 1.1   The platform SHALL support necessary curatorial functions.


class TestFunctionalRequirements_1_1_1:
    """
    The platform SHALL support creation and maintenance of Projects established
    to encompass collaborative collecting in thematically-coherent areas.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_1_1_2:
    """
    The platform SHALL support Nomination of Seeds in the context of Projects.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_1_1_3:
    """
    The platform SHALL support claiming of Nominated Seeds by archiving
    Organizations in the context of Projects.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_1_1_4:
    """
    The platform SHALL support assertion of Claims of Seeds intended to be
    Crawled by Organizations in the context of Projects.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_1_1_5:
    """
    The platform SHALL support reporting of Holdings documenting Seeds
    actually harvested by Organizations and curated in Collections in the
    context of Projects.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_1_1_6:
    """
    The platform SHALL support high-level discovery of web archive Projects
    and Collections and finer-grained discovery of Seeds.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_1_2:
    """
    The platform SHALL support necessary administrative functions.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_1_2_1:
    """
    The platform SHALL support registering new and maintaining existing
    individual Agent user accounts.
    """

    def test_create_user(self, selenium):
        raise NotImplementedError


class TestFunctionalRequirements_1_2_2:
    """
    The platform SHALL support establishing new and maintaining existing
    Organizational accounts, to which Agents may be affiliated.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError
