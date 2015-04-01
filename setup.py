import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'VERSION.txt')) as f:
    VERSION = f.read().strip()

setup(name='lexical',
      version=VERSION,
      description='Simple Lexical Analyser',
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Guto Maia',
      author_email='guto@guto.net',
      url='',
      keywords='web',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='lexical',
      install_requires=[],
      )
