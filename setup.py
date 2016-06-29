import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.markdown')) as f:
    README = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wealthmap',
    version='0.1',
    packages=find_packages(exclude=['sample_project']),
    include_package_data=True,
    license='MIT License',  # example license
    description='The next generation of econ dev resource matching.',
    long_description=README,
    zip_safe=False,  # This may not be necessary, per http://bit.ly/1UzPCs1
    url='https://github.com/codeforamerica/wealthmap/issues',
    author='Mikela Clemmons, Mark Rossetti',
    author_email='support@codeforamerica.org',
    install_requires=[
        'django-localflavor>=1.2',
        'django-formtools>=1.0',
        'django-bootstrap-form>=3.2,<4.0',
        'djangorestframework>=3.3.3,<3.4',
        'django-cors-headers==1.1.0',
        'django-admin-sortable2==0.6.4',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        # TODO: Update with reference to econ dev or business
    ],
)
