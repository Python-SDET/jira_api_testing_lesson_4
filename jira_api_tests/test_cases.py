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
        return self.jira_implementation.sprint.create_sprint()

    def update_sprint_name(self, sprint_id, sprint_name):
        return self.jira_implementation.sprint.set_name(sprint_id, sprint_name)

    def update_sprint_start(self, start_time_date):
        raise NotImplementedError()

    def update_sprint_end(self, end_time_date):
        raise NotImplementedError()


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
    # sprint_key = sprint_test.create_sprint()
    # Change Sprint Name
    name_result = sprint_test.update_sprint_name('1', 'Sprint 12-6-19-14')
    print(name_result)
    # Change Sprint End Date
    # Change Sprint Start Date
    # Set Sprint Active
    # Close A Sprint
    # Open Another Sprint
    # Attempt to have overlapping sprints
    # Put sprints in a workable state


sprint_test_case()


