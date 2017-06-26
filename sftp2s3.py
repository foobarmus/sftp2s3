# sftp2s3
# copy files from an sftp server to an amazon s3 bucket
# author: Jonas McCallum

import os, argparse, getpass

import pysftp, boto3

def get_args():
    """parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="host:/path/filename.etc")
    parser.add_argument("dest", help="your-s3-bucketname")
    args = parser.parse_args()
    host, file_path = args.source.split(':')
    filename = os.path.split(file_path)[-1]
    bucket = args.dest
    return args.source, host, file_path, filename, bucket

def get_sftp_creds():
    """prompt for username and password"""
    return {'username': input('SFTP User: '),
            'password': getpass.getpass()}

def sftp_get(host, file_path):
    """download source file to local"""
    credentials = get_sftp_creds()
    with pysftp.Connection(host, **credentials) as sftp:
        sftp.get(file_path)

def s3_put(filename, bucket):
    """copy from local to s3 bucket"""
    s3 = boto3.resource('s3')
    with open(filename, 'rb') as f:
        s3.Bucket(bucket).put_object(Key=filename, Body=f)

def cleanup(filename):
    """delete local copy of file"""
    os.remove(filename)

def notify(source, dest):
    """send email notification of upload"""

if __name__ == '__main__':
    try:
        source, host, file_path, filename, bucket = get_args()
        sftp_get(host, file_path)
        s3_put(filename, bucket)
        notify(source, bucket)
    except Exception as e:
        print(e)
    finally:
        cleanup(filename)
