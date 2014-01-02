from setuptools import setup
import os

PROJECT_ROOT = "."

setup(name='aksite',
      version='1.0',
      description='aksite',
      author='Sam Persson',
      author_email='samiljan@gmail.com',
      url='http://www.altekamerere.org',
	  install_requires=open('%s/requirements.txt' % os.environ.get('OPENSHIFT_REPO_DIR', PROJECT_ROOT)).readlines(),
     )
