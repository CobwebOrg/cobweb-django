@fr7-13
Feature: Logging in and out

  @done @wip
  @fr6-1
  Scenario: Login links are visible
    Given: User is not logged in
     When: User visits any page
     Then: The text "Log in" links to login page

  @done
  @fr7-13-1
  Scenario: Login with username and password
    Given: User is not logged in
     When: User visits login page
      And: User enters username and password
     Then: User is logged in

  @done
  @fr7-13-1
  Scenario: Failed login with username and password

  @july
  @fr7-13-2
  Scenario: Password reset

  @defer
  Scenario: Login with OAuth

  @done
  @fr6-1
  Scenario: Logout link is visible
    Given: User is logged in
     When: User visits any page
     Then: The text "Log Out" links to logout url

  @done
  Scenario: Logout
    Given: User is logged in
     When: User visits logout url
     Then: User is logged out
