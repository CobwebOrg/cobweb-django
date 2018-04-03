Feature: Logging in and out

  @done
  Scenario: Login links are visible
    Given: User is not logged in
     When: User visits any page
     Then: The text "Log in" links to login page

  @done
  Scenario: Login with username and password
    Given: User is not logged in
     When: User visits login page
      And: User enters username and password
     Then: User is logged in

  @done
  Scenario: Failed login with username and password

  @july
  Scenario: Password reset

  @defer
  Scenario: Login with OAuth
