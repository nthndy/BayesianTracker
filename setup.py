from setuptools import setup
# from setuptools.command.install import install

def get_install_required():
    with open("./requirements.txt", "r") as reqs:
        requirements = reqs.readlines()
    return [r.rstrip() for r in requirements]

def get_version():
    with open("./btrack/VERSION.txt" ,"r") as ver:
        version = ver.readline()
    return version.rstrip()

setup(name='btrack',
      version=get_version(),
      description='BayesianTracker is a simple Python/C++ based framework for multi-object tracking',
      author='Alan R. Lowe',
      author_email='a.lowe@ucl.ac.uk',
      url='https://github.com/quantumjot/BayesianTracker',
      packages=setuptools.find_packages(),
      package_data={'btrack': ['libs/libtracker*', 'VERSION.txt']},
      include_package_data=True,
      install_requires=get_install_required(),
      license='LICENSE.md')
