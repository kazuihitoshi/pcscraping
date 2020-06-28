#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from oauth2client import client
from googleapiclient import sample_tools

def open(option=None):
  if option is None :
      argv = []
  else:
      argv = option
  service, flags = sample_tools.init(
      argv, 'blogger', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/blogger')
  try:
      return (service.posts())

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize')
    return (None)

def update(posts,postId, title, body,brogId='774130430689114410'):
    body = {
    "kind": "blogger#post",
    "title": title,
    "content":body
    }
    posts.update(blogId=brogId, postId=postId, body=body).execute()
    return()

def insert(posts, title, body,brogId='774130430689114410',isDraft=False):
    body = {
    "kind": "blogger#post",
    "title": title,
    "content":body
    }
    posts.insert(blogId=brogId, body=body,isDraft=isDraft).execute()
    return()

def main(argv):
    b = open()
    #update(posts=b,postId='6313931809273408540',title='titleです',body='記事です')
    insert(posts=b,title='titleですよ',body='記事です',isDraft=True)

if __name__ == '__main__':
  main(sys.argv)
