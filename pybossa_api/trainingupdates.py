import requests
import json
import os
import csv
from utils import get_ids, get_projectIDs


PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def generateCSV(user_ids, filename='user', write=True):
    """
    Input: user_ids dictionary (user ids: task values), filename
    Output: csv file with name, email, and number of tasks completed
    """
    emails = {}
    for user in user_ids:
        r = requests.get('https://pe.goodlylabs.org'
                         '/api/user/{}?api_key={}&limit=100'
                         .format(user, PYBOSSA_API_KEY), headers=headers)
        user_info = json.loads(r.text)
        if len(user_info) != 3:
            emails[user] = [user_info['fullname'],
                            user_info['email_addr'], user_ids[user]]
    if write:
        with open('trainingupdates_output/{}.csv'.format(filename), 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["name", "email", "tasks"])
            for i in emails:
                writer.writerow([emails[i][0], emails[i][1], emails[i][2]])
    return emails


if __name__ == '__main__':
    # Write the project names you want to retrieve task data on
    # Right now, these are the training tasks
    project_names = ['Covid_SourceRelevancev1', 'Covid_Semantics1.0',
                     "Covid_Reasoningv1", "Covid_Probabilityv1",
                     "Covid_Languagev1.1", "Covid_Holisiticv1.2",
                     "Covid_Form1.0", "Covid_Evidencev1",
                     "Covid_ArgumentRelevancev1.2"]
    # Call project_ids to retrieve the project IDs of each project
    project_ids = get_projectIDs(project_names)
    for name in project_ids:
        # Call get_ids to retrieve a list of user IDs and how many tasks
        # they've completed for a given project
        # Here, we specify the months we want to retrieve tasks from
        user_ids = get_ids([project_ids[name]], months=['2020-09', '2020-10'])
        # Finally, we generate the CSV for each project, giving us the name, 
        # email, and number of tasks each person has done for the given months
        generateCSV(user_ids, name)
