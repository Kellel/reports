from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

from report import __version__

setup(name='report',
      version=__version__,
      description='Generate reports from txt files',
      author="Kellen Fox",
      author_email='kellen@cablespeed.com',
      packages=['report', 'report.parsers'],
      install_requires=reqs,
      scripts=['scripts/report-daemon',
               'scripts/report-cli']
)
