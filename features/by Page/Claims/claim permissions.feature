Feature: Claim Permissions

  @may
  Scenario Outline: Anonymous doesn't see claim links
    Given I'm not logged in
      And there's a nomination
     When I visit detail page for object <object>
     Then there is no claim nomination link

      Examples:
      | object             |
      | nomination         |
      | nomination.project |

  @may
  Scenario: Anonymous users can't create or update claims
    Given I'm not logged in
      And there's a nomination
     When I visit claim_create page for nomination
     Then taken to login page
      And I get an error message telling me I need to log in

  @may
  Scenario: Users who don't administer collections can or can't add claims
    Given: there's a nomination
      And: user is logged in
      And: user is not administrator of any collections
     When: user tries to add a claim
     Then: we need go decide if user is allowed to make claims

  @may
  Scenario: Collection administrators can make claims on behalf of their collections
    Given: a nomination
      And: user is logged in
      And: user is administrator of one or more collections
     Then: user can create a claim of the nomination for any of their collections
