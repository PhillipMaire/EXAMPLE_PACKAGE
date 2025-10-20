
from setuptools import setup, find_packages
pakage_name = 'snippetropolis'
setup(
    name=pakage_name,
    version='0.1.0',
    packages=find_packages(),
    package_data={
        pakage_name: ['../data/*'],
    },
    # Other metadata here...
)



# ____ ____ ____ ____ ____ ____
# DEBUGGING 

# https://stackoverflow.com/questions/42609943/what-is-the-use-case-for-pip-install-e

# once you have a setup.py file in root directory you can use this command to install package that automatically updates as you use it. this allows you to directly debug the code using hte debugger!!!!


# pip install -e 


# ____ ____ ____ ____ ____ ____
