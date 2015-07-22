from distutils.core import setup

setup(name='reports',
      version='1.0',
      description='Generate reports from txt files',
      author="Kellen Fox",
      author_email='kellen@cablespeed.com',
      packages=['report'],
      scripts=['scripts/report-daemon']
)
