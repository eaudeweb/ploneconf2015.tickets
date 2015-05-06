from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='ploneconf2015.tickets',
      version=version,
      description="Tickets for Plone Conference 2015",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='tickets ploneconf 2015',
      author='Alin Voinea',
      author_email='alin@eaudeweb.ro',
      url='https://github.com/eaudeweb/ploneconf2015.tickets',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ploneconf2015'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'phpserialize',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
