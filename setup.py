from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'celery',
    'pyinotify',
    'redis',
    'setuptools',
    ]

tests_require = [
    'coverage',
    'nose',
    ]

setup(name='watchman',
      version=version,
      description=(
          "Watch directories for new files and send tasks to a queue "
          "for futher asynchronous processing."),
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python'],
      keywords=[],
      author='Carsten Byrman',
      author_email='carsten.byrman@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['watchman'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
              'notify = watchman.notify:main',
          ]},
      )
