@fr5-7
Feature: claim data model

  Scenario Outline: claim data model
    Given: there is a claim
     Then: claim has field <field> of type <type>

      Examples:
      | field         | type         |
      | project       | Project      | # <- Computed nomination.project
      | resource      | Resource     | # <- Computed nomination.resource
      | nomination    | Nomination   |
      | organization  | Organization |
      | status        | str          |
      | impact_factor | bool         |  # <- Computed
      # | scope |
      # | notes |

  Scenario: claim project computed from nomination
    Given: there is a claim
     Then: claim.project is equal to  claim.nomination.project

  Scenario: claim resource computed from nomination
    Given: there is a claim
     Then: claim.resource is equal to  claim.nomination.resource

  Scenario: claim impact factor computed from holdings
    Given: there is an organization
      And: organization has made a claim
      And: organization has a collection
     When: claim's resource <is_or_is_not> held in collection
     Then: claim's impact factor is equal to <impact_factor>

      Examples:
      | is_or_is_not | impact_factor |
      | is           | true          |
      | is not       | false         |
