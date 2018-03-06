"""
Tests for Cobweb Project functional requirements, section 1.

The platform SHALL maintain state information about its functional entities
(see Figure 1).
"""

import pytest


class TestFunctionalRequirements_5_1:
    """
    The complete version history for all state information SHALL be maintained,
    including date and timestamps of value changes and the Agent making the
    change.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_1_1:
    """
    Timestamps SHALL be maintained with timezone information, either UTC or the
    local timezone.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_2:
    """
    The textual elements of all entities SHALL accept Unicode/ISO/IEC 10646
    characters (Unicode, 2017).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


@pytest.mark.xfail
def no_test(self):
    raise NotImplementedError

class TestFunctionalRequirements_5_3:
    """
    All entities (except notes) MAY be associated with one or more descriptive notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_3_1:
    """
    Each note SHALL be defined in terms of its author, date and timestamp (with timezone granularity), scope of visibility, and text, and OPTIONALLY a reference to a previous note to which the current one is a response.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_3_1_1:
    """
    Visibility scope SHALL be one of: Public, Organizational scope (restricted to Organizational affiliates), or Project scope (restricted to Project associates).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_4:
    """
    A Project SHALL be defined in terms of its title, narrative description, administrator(s), Nomination policy, status, and impact factor, and MAY be defined in terms of Resources, Tags, Subject Headings, and notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_4_1:
    """
    Nomination policy SHALL be one of: Public, Organizational affiliation (restricted to Institutional affiliates), or Restricted (to named whitelisted individuals).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_4_2:
    """
    Project status SHALL be one of: Active (open for Nomination, the default), Deprecated (recommended for no further Nomination), Inactive (closed to Nomination), or Deleted.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_4_3:
    """
    Project impact factor SHALL be the counts, by number and percentage, of Nominated Resources that are Claimed or Held.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_4_4:
    """
    Project Subject Headings SHOULD support FAST (Faceted Application of Subject Terminology) (OCLC, 2017).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5:
    """
    A Resource SHALL be defined in terms of its normalized URL and status on the live web, and MAY be defined in terms of its title, narrative description, language, Tags, Subject Headings, and referencing Nominations, Claims, and Holdings, and notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5_1:
    """
    Resources SHALL be unique across the Cobweb system.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5_1_1:
    """
    A given Resource, with normalized URL globally unique within Cobweb, MAY be Nominated, Claimed, or Held relative to multiple Projects.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5_2:
    """
    The normalized form of the URL SHALL conform to the syntax defined in Section § 6 of RFC 3986 (Berners-Lee et al., 2005).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5_3:
    """
    Resource status SHALL be one of: Active (dereferencable and retrievable directly from its URL), Redirected (dereferencable and retrievable from a redirected URL), Inactive (not dereferencable), or Unknown.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5_3_1:
    """
    Status SHOULD be determined by periodically scheduled link checking.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5_4:
    """
    Resource Subject Headings SHOULD support FAST (Faceted Application of Subject Terminology) (OCLC, 2017).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_5_5:
    """
    Language SHALL be selected from ISO 369-defined languages.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6:
    """
    A Nomination SHALL be defined in terms of its underlying Project, Seed Resource, status, endorsement counter, and impact factor, and MAY be defined in terms of its narrative description (providing the justification for the Nomination), Tags, Subject Headings, and notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6_1:
    """
    Nominations SHALL be unique within the context of their underlying Projects.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6_1_1:
    """
    A given Resource, with Seed URL globally unique within Cobweb, MAY be associated with Nominations relative to multiple Projects.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6_1_2:
    """
    A given Nomination, with underlying Resource globally unique within Cobweb, SHALL be associated with a single Project.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6_2:
    """
    Nomination status SHALL be one of: Active (open for Claiming, the default), Deprecated (recommended for no further Claiming), Inactive (closed to Claiming), or Deleted.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6_3:
    """
    The endorsement counter SHALL maintain a counter of the number of times that the Nomination has been endorsed (similar to Twitter or Facebook’s “like” feature) by users other than the Nomination’s creator.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6_3_1:
    """
    A given non-creating user SHALL only be able to endorse a given Nomination once.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_6_4:
    """
    Nomination impact factor SHALL be the number of Claims, endorsements, Claiming Organizations, Holdings, and Holding Organizations.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_7:
    """
    A Claim SHALL be defined in terms of its underlying Project, Resource, Nomination, curating Organization, status, impact factor, and MAY be defined in terms of its notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_7_1:
    """
    Claims SHALL be unique within the context of their underlying Projects and Claiming Organizations.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_7_1_1:
    """
    A given Nomination SHALL be Claimed by a given Organization at most one time in the context of a particular Project.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_7_2:
    """
    Claim status SHALL be one of: Active (open for Holding, the default), Deprecated (recommended for no further Holding), Inactive (closed to Holding), or Deleted.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_7_3:
    """
    Claim impact factor SHALL be a Boolean flag indicating whether or not the Claiming Organization actual Holds the underlying Resource.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_8:
    """
    A Holding SHALL be defined in terms of its underlying Project, Resource, curating Organization, and status, and MAY be defined in terms of an underlying Claim,  Collection, and notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_8_1:
    """
    Holdings SHALL be unique within the context of their underlying Projects and Holding Organizations.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_8_2:
    """
    Holding status SHALL be one of: Active (under curatorial stewardship by the Holding Organization, the default) or Deleted.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_9:
    """
    A Collection SHALL be defined in terms of its title, narrative description, curating Organization, underlying Holdings, status, and terms of use, and MAY be defined in terms of landing page URL, catalog record/finding aid/discovery portal/etc. URL(s), Tags, Subject Headings, and notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_9_1:
    """
    Collection status SHALL be one of: Active, Inactive, Unknown (default), or Deleted.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_9_2:
    """
    Terms of use SHALL include use modality, and MAY include contact name and email (RECOMMENDED if modality is Restricted) and formatted attribution statement.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_9_2_1:
    """
    Use modality SHALL be one of: Anonymous, Public (but requiring prior authentication), or Restricted (to authenticated individuals).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_9_3:
    """
    Collection Subject Headings SHOULD support FAST (Faceted Application of Subject Terminology) (OCLC, 2017).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_10:
    """
    An Organization SHALL be defined in terms of its full legal name, administrator(s), and Cobweb impact factor, and MAY be defined in terms of its common short name, nickname, or acronym, description of curatorial or stewardship mission and collecting policy, mailing address, telephone number (qualified with country code), URL, email address, contact Agent(s), parent Organization, and notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_10_1:
    """
    Organizational impact factor SHALL be the number of Projects, Nominations, Claimed Nominations (as an absolute count and percentage of total Nominations), and Held Claims (as an absolute count and percentage of total Nominations and Claims).
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_11:
    """
    An Agent SHALL be defined in terms of his or her name and impact factor, and MAY be defined in terms of his or her Organizational affiliation, professional title, personal URL, email address, and notes.
    """

    @pytest.mark.xfail
    def no_test(self):
        raise NotImplementedError


class TestFunctionalRequirements_5_11_1:
    """
    Agent impact factor SHALL be the number of Nominations (absolutely and as a percentage of total Nominations), Claimed Nominations (as an absolute count and percentage of total Nominations Nominated by the Agent), and Held Claims (as an absolute count and percentage of total Claims of Nominations Nominated by the Agent).
    """
