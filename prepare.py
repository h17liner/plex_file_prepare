# -*- coding: utf-8 -*-
import argparse
import sys, os
import bencode
from tracker import rutracker
from urlparse import urlparse


parser = argparse.ArgumentParser(description='Torrent processing.')
parser.add_argument('--torrent_file', type=str)

args = parser.parse_args()

if not args.torrent_file or not args.torrent_path:
    print "Cannot work without torrentfile.  Exit"
    sys.exit(1)

with open(args.torrent_file, 'rb') as fh:
    torrent_data = fh.read()

torrent = bencode.bdecode(torrent_data)

filename, file_extension = os.path.splitext(
    torrent.get('info').get('name')
)

parsed_uri = urlparse(torrent.get('comment'))
domain = '{uri.netloc}'.format(uri=parsed_uri)


if domain == 'rutracker.org':
    tracker = rutracker.RutrackerPage(page_url=torrent.get('comment'))

title = '%s %s%s' %(tracker.title(lang='en'), tracker.year(), file_extension)
print title
