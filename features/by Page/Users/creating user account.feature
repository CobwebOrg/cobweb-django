Feature: registering new user accounts

  Scenario: "Sign Up" link appears when not logged in
    Given I'm not logged in
     When I visit any page
     Then the text "Sign Up" links to "/users/new"

  Scenario: "Sign Up" link does not appear after login
    Given I am logged in
     When I visit any page
     Then the text "Sign Up" does not appear as a link

  Scenario: registering with email and password
    Given I'm not logged in
     When I click the "Sign Up" link
      And I enter my email and password in the registration form
      And I click submit
     Then A user account is created
      And I am automatically logged in as the created user
      And I am taken to the edit page for my profile

  Scenario: confirming registration via email

  Scenario: registering with invalid information
