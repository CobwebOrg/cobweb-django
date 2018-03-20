Feature: creating projects

  Scenario:
    Given I'm not logged in
     When I visit "{projects/}"
     Then an "add project" link does not appear

  Scenario:
    Given I'm not logged in
     When I visit "{projects/new}"
     Then I get redirected to a the login page
      And I get an error message telling me I need to log in

  Scenario:
    Given I'm a logged in user
     When I visit "{projects/}"
     Then an "add project" link does appear
