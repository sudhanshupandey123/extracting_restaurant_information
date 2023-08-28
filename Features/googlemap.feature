Feature: Google Map

  Scenario: Google Map Search
    Given He Open Google Map
    When He Search For "restaurant near marathahalli"
    When He Found The List
    When He Save Top "5" All The Details
    Then He Make CSV File Of Those

  Scenario Outline: Google Map Search with multiple values
    Given He Open Google Map
    When He Search For "<user_searched_for>"
    When He Found The List
    When He Save Top "<user_requirement_value>" All The Details
    Then He Make CSV File Of Those
    Examples:
      | user_searched_for            | user_requirement_value |
      | ressort near electronic city | 5                      |
      | oyo near tin factory         | 5                      |


