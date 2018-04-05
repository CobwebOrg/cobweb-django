Feature: project permissions

  Scenario: Anonymous users don't get "add project" link.
    Given I'm not logged in
     When I visit url /projects/
     Then the text "add project" does not appear as a link

  Scenario: Anonymous users can't add projects.
    Given I'm not logged in
     When I visit url /projects/new
     Then taken to login page
      And I get an error message telling me I need to log in
  #
  # Scenario:
  #   Given I'm a logged in user
  #    When I visit /projects/
  #    Then an "add project" link does appear
