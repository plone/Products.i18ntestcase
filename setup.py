from setuptools import setup, find_packages
import sys, os

version = '1.2'

setup(name='Products.i18ntestcase',
      version=version,
      description="Products.i18ntestcase makes it easier to use "
                  "QueueCatalog in your Plone site.",
      long_description="""\
      """,
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
      ],
      keywords='Plone i18n testcase',
      author='Hanno Schlichting',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/collective/Products.i18ntestcase/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
)
