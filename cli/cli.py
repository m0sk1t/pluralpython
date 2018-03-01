import sys
import configparser
import urllib.parse
import urllib.request
from branch import validate_branch, BranchValidationException


def post_request(url, post_data):
    request_data = urllib.parse.urlencode(post_data)
    request_data = request_data.encode('ascii')
    request = urllib.request.Request(url, request_data)
    return urllib.request.urlopen(request)


def reset():
    """
    Resets a chart tree
    :return: None
    """
    with post_request(endpoint + '/api/orgchart/new', {}) as response:
        print(response.read())


def add(branches):
    """
    Adds a new branch to chart tree
    :param branches: list of branches to add
    :return: None
    """
    for branch in branches:
        try:
            boss_id, employees = validate_branch(branch)
            with post_request(endpoint + '/api/orgchart/add', {
                'boss_id': boss_id,
                'employees': employees
            }) as response:
                print(response.read())
        except BranchValidationException as error:
            print('BranchValidationException: {0}'.format(error))


def drop(boss_id):
    """
    Drops a branch from chart tree by boss_id
    :param boss_id:
    :return: None
    """
    with urllib.request.urlopen(endpoint + '/api/orgchart/{0}'.format(boss_id)) as response:
        print(response.read())


def main():
    print('Illegal action')


endpoint = ''
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    port = config['server']['port'] or config['default']['port']
    host = config['server']['host'] or config['default']['host']
    endpoint = 'http://{0}:{1}'.format(host, port)
    action = sys.argv[1:2]
    data = sys.argv[2:]
    if 'add' in action:
        add(data)
    elif 'drop' in action:
        drop(data[0])
    elif 'reset' in action:
        reset()
    else:
        main()
