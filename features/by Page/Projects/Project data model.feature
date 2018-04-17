@fr5-7
Feature: project data model

  Scenario Outline: project data model
    Given: there is a project
     Then: project has field <field> of type <type>

      Examples:
      | field               | type                          |
      | title               | str                           |
      | description         | str                           |
      | administrators      | ManyToManyField(User)         |
      | nomination_policy   | enum                          |
      | nominator_orgs      | ManyToManyField(Organization) |
      | nominators          | ManyToManyField(User)         |
      | nominator_blacklist | ManyToManyField               |
      | status              | enum                          |
      # | impact_factor       | int??? | # <- computed
      # | resources           | ManyToManyField(Resource, through nominations) | # <- computed
      | tags                | ManyToManyField(Tag)          |
      # | subject_headings | ManyToManyField(SubjectHeading)  |
