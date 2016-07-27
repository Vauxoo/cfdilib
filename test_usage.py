# coding: utf-8
"""script: test_usage.py
This is a helper for maitainance and to set some environment prints
and differentiate between CI and Local test run.
"""
from __future__ import print_function
import cfdilib
from cfdilib.tools import tools
import os
from botocore.exceptions import ProfileNotFound, NoCredentialsError


print('*'*50)
print(cfdilib.__version__)
print(os.environ.get('TRAVIS'))
print(type(os.environ.get('TRAVIS')))
print('*'*50)

cfdiv32 = 'http://www.sat.gob.mx/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt'  # noqa

if not os.environ.get('TRAVIS') == 'true':
    '''Here basically you need to have a profile called "dev" to use boto3
    This is a helper this is why it is not too much elaborated.

    RTFD: http://boto.cloudhackers.com/en/latest/boto_config_tut.html
    '''
    try:
        tools.send_s3_xsd(cfdiv32)
    except ProfileNotFound:
        print ('Create a proper amazon profile called with write permisions '
               ' on %s "dev"' % tools.domain)
    except NoCredentialsError:
        print ('Create a proper amazon credentials '
               ' on %s "dev" profile' % tools.domain)
