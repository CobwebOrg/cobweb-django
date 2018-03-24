Feature: registering new user accounts

  Scenario: "sign up" link appears when not logged in
    Given I'm not logged in
     When I visit any page
     Then the text "sign up" links to "/users/new"

  Scenario: "sign up link" does not appear after login
    Given I am logged in
     When I visit any page
     Then a "sign up" link does not appear above the navbar

  Scenario: registering with email and password
    Given I'm not logged in
     When I click the "sign up" link
      And I enter my email and password in the registration form
      And I click submit
     Then A user account is created
      And I am automatically logged in as the created user
      And I am taken to the edit page for my profile

  Scenario: confirming registration via email

  Scenario: registering with invalid information
