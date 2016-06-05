from __future__ import with_statement
from fabric.api import *
from fabric.contrib.files import exists
from fabric.operations import local as lrun, run
from fabric.context_managers import env
from pprint import pprint
import os
import pdb
import sys

cms = 'magento'
cms_version = "1.9.2.4"
file_ext = "zip"
cms_download_filename = "%s-%s.%s" % (cms,cms_version,file_ext)
cms_download_url = "https://github.com/OpenMage/magento-mirror/archive/1.9.2.4.zip"
sample_data_url = "https://github.com/Vinai/compressed-magento-sample-data/raw/master/compressed-magento-sample-data-1.9.1.0.tgz"
sample_data_filename = "%s-%s.%s" % (cms,"sample","tgz")

root_dir = "/vagrant/htdocs"
download_path = "%s/%s" % ("/tmp",cms)

@task
def localhost():
    env.run = lrun
    env.hosts = ['localhost']
    env.use_sudo = True
    env.password = 'vagrant'

@task
def execute(*args, **kwargs):
    if env.use_sudo:
        sudo(*args, **kwargs)
    else:
        run(*args, **kwargs)

@task
def init():
    execute("mkdir -p %s" % (download_path))
    with cd(download_path):
        if not exists(cms_download_filename):
            execute("wget %s -O %s" % (cms_download_url, cms_download_filename))
            execute("unzip %s" % (cms_download_filename))
        if not exists(sample_data_filename):
            execute("wget %s -O %s" % (sample_data_url,sample_data_filename))
            execute("tar -xvf %s" % (sample_data_filename))        
        execute("rsync -av ./%s/ %s/" % ('magento-mirror-1.9.2.4',root_dir))       
        execute("rsync -av ./%s/ %s/" % ('magento-sample-data-1.9.1.0',root_dir))       
        execute("find . -type d -name '*%s*' -exec rm -rf {} \;" % (cms))
        execute("chmod -R 777 %s" % (root_dir))