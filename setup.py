from setuptools import setup
import os

PROJECT_ROOT = "."

import locale
#os.environ["LANG"] = "en_US.UTF-8"
print("locale:", locale.getpreferredencoding())

print("setup.py:", __name__)

requirements = [l.strip()
                for l in open('%s/requirements.txt' % os.environ.get('OPENSHIFT_REPO_DIR', PROJECT_ROOT)).readlines()
                if l.strip() and not l.startswith("#")]

print([r[3:] for r in requirements if r.startswith("-e ")])
print([r.split("#egg=")[1] if r.startswith("-e ") else r for r in requirements])

setup(name='aksite',
      version='1.0',
      description='aksite',
      author='Sam Persson',
      author_email='samiljan@gmail.com',
      url='http://www.altekamerere.org',
      dependency_links=[r[2:] for r in requirements if r.startswith("-e ")],
      install_requires=[r.split("#egg=")[1] if r.startswith("-e ") else r for r in requirements],
      )
