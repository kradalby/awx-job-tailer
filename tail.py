#!/usr/bin/env python3

import requests
import sys
import os
import argparse
import configparser


def get_job_events_url(base_url, job_id, page=1):
    return '{}/jobs/{}/job_events/?page={}'.format(base_url, job_id, page)


def has_next_page(job_event):
    return 'next' in job_event.keys() and job_event['next']


def get_results(job_event):
    if 'results' in job_event.keys():
        return job_event['results']
    return []


def get_job_status(job_event):
    results = get_results(job_event)

    if results:
        return results[-1]['summary_fields']['job']['status']
    return ''


def get_last_line_id(job_event, old_id):
    results = get_results(job_event)

    if results:
        return results[-1]['id']
    return old_id


def get_stdout_lines(job_event, last_line_id):
    return [
        line['stdout'] for line in get_results(job_event)
        if line['id'] > last_line_id
    ]


def loop(session, base_url, job_event, job_id):
    status = get_job_status(job_event)
    last_line_id = 0
    lines = get_stdout_lines(job_event, last_line_id)
    page = 1
    while True:
        for line in lines:
            yield line
        if has_next_page(job_event):
            page = page + 1
        last_line_id = get_last_line_id(job_event, last_line_id)
        url = get_job_events_url(base_url, job_id, page)
        je = session.get(url, auth=session.auth)
        job_event = je.json()

        lines = get_stdout_lines(job_event, last_line_id)
        status = get_job_status(job_event)


if __name__ == '__main__':
    HOME_DIR = os.path.expanduser('~')
    TOWER_CONFIG = os.path.join(HOME_DIR, '.tower_cli.cfg')
    address = ''
    username = ''
    password = ''

    if os.path.isfile(TOWER_CONFIG):
        config = configparser.ConfigParser()
        config.read(TOWER_CONFIG)
        address = config['general']['host']
        username = config['general']['username']
        password = config['general']['password']

    parser = argparse.ArgumentParser()
    parser.add_argument('job', type=int, help='The job id to follow')
    parser.add_argument('-a', '--address', help='AWX/Tower address')
    parser.add_argument('-u', '--username', help='AWX/Tower username')
    parser.add_argument('-p', '--password', help='AWX/Tower password')
    parser.add_argument(
        '-i',
        '--insecure',
        action='store_true',
        help='Use HTTP instead of HTTPS')
    args = parser.parse_args()

    # Override config with commandline parameters
    if args.address:
        address = args.address

    if args.username:
        username = args.username

    if args.password:
        password = args.password

    # Check that necessary information is given

    for param in ['address', 'username', 'password']:
        if not eval(param):
            sys.exit(
                'Could not find tower_cli config nor argument for setting {}'.
                format(param))

    schema = 'https' if not args.insecure else 'http'
    address = '{}://{}/api/v2'.format(schema, address)

    try:
        s = requests.Session()
        s.auth = (username, password)
        job_event = s.get(get_job_events_url(address, args.job, 1)).json()

        for line in loop(s, address, job_event, sys.argv[1]):
            print(line)
    except KeyboardInterrupt:
        sys.exit(0)
