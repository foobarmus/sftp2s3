# Utility for Copying Files from an SFTP Server to an S3 Bucket
#
# Copyright 2017 Jonas McCallum.
#
# Open source, MIT license
# http://www.opensource.org/licenses/mit-license.php
"""
Main controller
Author: Jonas McCallum
https://github.com/phatpiglet/sftp2s3
"""
import os, argparse, getpass

import pysftp, boto3


class FileTransfer(object):
    """file transfer controller"""

    def __init__(self, args):
        """parse the command line arguments"""
        host, file_path = args.source.split(':')
        filename = os.path.split(file_path)[-1]
        self.host = host
        self.file_path = file_path
        self.filename = filename
        self.bucket = args.dest
        self.args = args

    def sftp_get(self):
        """download source file to local"""
        credentials = _get_sftp_creds()
        with pysftp.Connection(self.host, **credentials) as sftp:
            sftp.get(self.file_path)

    def s3_put(self):
        """copy from local to s3 bucket"""
        filename = self.filename
        s3 = boto3.resource('s3')
        with open(filename, 'rb') as f:
            s3.Bucket(self.bucket).put_object(Key=filename, Body=f)

    def cleanup(self):
        """delete local copy of file"""
        os.remove(self.filename)

    def notify(self):
        """send email notification of upload"""


def _get_sftp_creds():
    """prompt for username and password"""
    return {'username': input('SFTP User: '),
            'password': getpass.getpass()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="host:/path/filename.etc")
    parser.add_argument("dest", help="your-s3-bucketname")
    args = parser.parse_args()
    try:
        transfer = FileTransfer(args)
        transfer.sftp_get()
        transfer.s3_put()
        transfer.notify()
    finally:
        try:
            transfer.cleanup()
        except NameError:
            print('Nothing to clean up.')
