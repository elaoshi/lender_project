Feature: Lender
    A site where you can update a lender.

    Scenario: Update the lender
        Given I get a lender

        When I update it

        Then I should see the change