#!/usr/bin/env python
# coding=utf-8

import os
import requests
from time import sleep

USER_ID = os.environ.get('user_id')

def get_comments(access_token='', owner_id='', post_id='', comment_id=''):
    return requests.get('https://api.vk.com/method/wall.getComments', params={'access_token': access_token,
                                                                            'owner_id': '-%s'%owner_id,
                                                                            'post_id': post_id,
                                                                            'count': 100,
                                                                            'extended': 0,
                                                                            'need_likes': 0,
                                                                            'comment_id': comment_id,
                                                                            'v': 5.101
                                                                            })

def check_comments(postlink, access_token, group_id, post_id, comment_id=''):
    sleep(0.5)
    r1 = get_comments(access_token, group_id, post_id, comment_id)
    comments = r1.json()['response']['items']
    for comment in comments:
        if not 'deleted' in comment and USER_ID == comment['from_id']:
            print('write link')
            write_link(postlink%(group_id,post_id))
        #если ктото ответил на коммент читаем ветку ответов
        if 'thread' in comment and comment['thread']['count'] > 0:
            check_comments(postlink, access_token, group_id, post_id, comment['id'])


def write_link(link):
    links = []
    if not link in links:
        links.append(link)
        with open('links.txt', 'a') as file:
            file.write(link + '\n')

def main():
    #https://vkhost.github.io/
    access_token = os.environ.get('access_token')

    group_id = os.environ.get('group_id')
    gr = requests.get('https://api.vk.com/method/groups.getById', params={'access_token': access_token,
                                                                          'group_ids':group_id,
                                                                          'v': 5.101})
    postlink = 'https://vk.com/'+gr.json()['response'][0]['screen_name']+'?w=wall-%s_%s'
    date_x = 1559397075
    r = requests.get('https://api.vk.com/method/wall.get', params={'access_token': access_token,
                                                                   'owner_id': '-%s'%group_id,
                                                                   'count':100,
                                                                   'offset':0,
                                                                   'extended':'0',
                                                                   'v': 5.101})
    posts = r.json()['response']['items']
    for post in posts:
        print(post['id'])
        check_comments(postlink, access_token, group_id, post['id'])


if __name__ == '__main__':
	main()