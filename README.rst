=======
sftp2s3
=======
Utility for Copying Files from an SFTP Server to an S3 Bucket

Usage
-----
Once you have extracted the utility, installed the dependencies, and
configured Boto3, navigate to the sftp2s3 directory, and do something
like this:

::

    python sftp2s3.py mysftpserver.com:/path/to/file.png my-s3-bucketname
    python3 sftp2s3.py mysftpserver.com:/path/to/file2.png my-s3-bucketname

Dependencies
------------

- boto3 `config help`_
- pysftp `troubleshooting guide`_

.. _config help: http://boto3.readthedocs.io/en/latest/guide/quickstart.html
.. _troubleshooting guide: https://stackoverflow.com/questions/22073516/failed-to-install-python-cryptography-package-with-pip-and-setup-py

Both dependencies can be installed with pip. You may need to upgrade your
pip installation first. Further tips and tricks can be found in the
troubleshooting guide.

Boto3 Config
------------
Boto3 requires:

- credentials for a IAM user with full access to S3 and SES
- a default region, that matches the region of your S3 bucket

Email Config
------------
To switch on email notifications:

- copy notification_email_sample.txt to notification_email.txt
- modify notification_email.txt to meet your requirements

Note that if your AWS account still has SES in sandbox mode (the default)
you can only use validated email addresses. Also note that SES is only
available in 3 regions.
