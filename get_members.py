import argparse
import sys

import requests


def get_auth(client_id, client_secret):
    r = requests.get(
        'https://graph.facebook.com/oauth/access_token',
        params=dict(
            client_id=client_id,
            client_secret=client_secret,
            grant_type='client_credentials'))
    r.raise_for_status()
    return r.json()['access_token']


def get_members(access_token, group_id):
    r = requests.get(
        'https://graph.facebook.com/v2.11/{}/members'.format(group_id),
        params=dict(access_token=access_token))
    r.raise_for_status()
    members = r.json().get('data')
    next_url = r.json().get('next')
    while next_url:
        r = requests.get(next_url)
        r.raise_for_status()
        members += r.json().get('data')
        next_url = r.json().get('next')
    return members


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Get list of members of group')
    parser.add_argument('--client-id',
                        required=True,
                        help='This is typically the App ID.')
    parser.add_argument('--client-secret',
                        required=True,
                        help='This is typically the App Secret.')
    parser.add_argument('--group-id',
                        required=True,
                        help='$GROUP_ID in https://www.facebook.com/groups/$GROUP_ID/')

    return parser.parse_args(argv)


def print_csv(members):
    for member in members:
        print '{name},{id}'.format(**member)


def main(argv=None):
    argv = argv or sys.argv
    args = vars(parse_args(argv[1:]))
    access_token = get_auth(args['client_id'], args['client_secret'])
    members = get_members(access_token, args['group_id'])
    print_csv(members)


if __name__ == '__main__':
    main(sys.argv)
