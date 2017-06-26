=======
sftp2s3
=======
Copy a file from an SFTP server to an S3 bucket
-----------------------------------------------

::

    python sftp2s3.py mysftpserver.com:/path/to/file.png my-s3-bucketname
    python3 sftp2s3.py mysftpserver.com:/path/to/file2.png my-s3-bucketname

Installation
------------

::

    git clone https://github.com/phatpiglet/sftp2s3.git

Dependencies
------------

- boto3 `config help`_
- pysftp troubleshooting_

Both dependencies can be installed with pip. However, installation can be tricky, especially if your system is a bit old.

Boto3 also needs to be configured with:

- credentials for a programmatic IAM user
  with access to S3 and SES
- a default region, that matches the
  region of your S3 bucket

.. _config help: http://boto3.readthedocs.io/en/latest/guide/quickstart.html
.. _troubleshooting: https://stackoverflow.com/questions/22073516/failed-to-install-python-cryptography-package-with-pip-and-setup-py
