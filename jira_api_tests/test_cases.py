import json
import yaml
from jira_api_implementation.implementation import JiraImplementation


class IssueTest:

    def __init__(self):
        self.jira_implementation = JiraImplementation()

    def create_issue(self, issue_json=None):
        issues = self.jira_implementation.query(r'project=AD&maxResults=1000')
        beginning_issue_count = json.loads(issues.content.decode('utf-8'))['total']
        new_issue_json = self.jira_implementation.issue.create_issue()
        new_issue_key = json.loads(new_issue_json.content.decode('utf-8'))['key']
        issues = self.jira_implementation.query(r'project=AD&maxResults=1000')
        ending_issue_count = json.loads(issues.content.decode('utf-8'))['total']
        if ending_issue_count > beginning_issue_count:
            return new_issue_key

        # New Issue NOT detected
        return None

    def update_story_points(self, story_points, issue_id):
        starting_issue_json = self.jira_implementation.issue.get_issue(issue_id)
        starting_story_points = json.loads(starting_issue_json.content.decode('utf-8'))['fields']['customfield_10026']
        if starting_story_points == story_points:
            # Return story points value if no update needed
            return story_points

        observed_issue_json = self.jira_implementation.issue.set_story_points(story_points, issue_id)
        return observed_issue_json


class SprintTest:
    def __init__(self):
        self.jira_implementation = JiraImplementation()

    def create_sprint(self, sprint_json=None):
        return self.jira_implementation.sprint.create_sprint(sprint_json)

    def update_sprint_name(self, sprint_id, sprint_name):
        starting_name = None
        sprint_json = json.loads(self.jira_implementation.sprint.get_sprint(sprint_id).content.decode('utf-8'))
        if 'name' in sprint_json:
            starting_name = sprint_json['name']

        if starting_name == sprint_name:
            return sprint_id

        return self.jira_implementation.sprint.set_name(sprint_id, sprint_name)

    def update_sprint_start(self, sprint_id, start_time_date):
        beginning_start_date = None
        sprint_json = json.loads(self.jira_implementation.sprint.get_sprint(sprint_id).content.decode('utf-8'))
        if 'startDate' in sprint_json:
            beginning_start_date = sprint_json['startDate']

        if beginning_start_date == start_time_date:
            return sprint_id
        return self.jira_implementation.sprint.set_start_date(sprint_id, start_time_date)

    def update_sprint_end(self, sprint_id, end_time_date):
        return self.jira_implementation.sprint.set_end_date(sprint_id, end_time_date)

    def update_sprint_goal(self, sprint_id, goal):
        return self.jira_implementation.sprint.set_goal(sprint_id, goal)

    def update_sprint_state(self, sprint_id, sprint_state):
        return self.jira_implementation.sprint.set_state(sprint_id, sprint_state)


def issue_test_case():
    issue_test = IssueTest()
    issue_key = issue_test.create_issue()
    updated_issue = None

    story_point_values = [5, 1, 0, 'A', -1, 3.1415926535, 10000, 10, 30]
    story_point_results = []
    story_point_matches = []
    for story_point_value in story_point_values:
        story_point_results.append(issue_test.update_story_points(story_point_value, issue_key))
        updated_issue = issue_test.jira_implementation.issue.get_issue(issue_key)
        observed_story_points = json.loads(updated_issue.content.decode('utf-8'))['fields']['customfield_10026']
        story_point_matches.append([story_point_value, observed_story_points])

    with open(r'story_point_matches.yaml', 'w') as file:
        yaml.dump(story_point_matches, file, explicit_start=True)
        file.close()


def sprint_test_case():
    sprint_test = SprintTest()
    # Add A Sprint
    sprint_create_response = sprint_test.create_sprint()
    sprint_id = str(json.loads(sprint_create_response.content.decode('utf-8'))['id'])
    # Change Sprint Name
    name_result = sprint_test.update_sprint_name(sprint_id, 'New TEST Sprint via API')
    # Change Sprint Start Date
    start_date_result = sprint_test.update_sprint_start(sprint_id, '2020-01-01T00:00:00.000+0000')
    # Set Sprint End Date Before Start Date
    end_date_result = sprint_test.update_sprint_end(sprint_id, '2019-01-15T00:00:00.000+0000')
    assert end_date_result.status_code > 399
    # Set Sprint End Date After Start Date
    end_date_result = sprint_test.update_sprint_end(sprint_id, '2020-01-15T00:00:00.000+0000')
    assert end_date_result.status_code == 200
    # Set Sprint Active
    active_result = sprint_test.update_sprint_state(sprint_id, 'active')
    # Close A Sprint
    closed_result = sprint_test.update_sprint_state(sprint_id, 'closed')
    # Attempt to reopen a closed sprint
    reopen_result = sprint_test.update_sprint_state(sprint_id, 'active')
    assert reopen_result.status_code > 399


sprint_test_case()


