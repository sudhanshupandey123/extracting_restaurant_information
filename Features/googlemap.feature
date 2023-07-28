Feature: Google Map

  Scenario: Google Map Search
    Given He Open Google Map
    When He Search For "restaurant"
    When He Found The List
    When He Save Top "10" All The Details
    Then He Make CSV File Of Those


