from setuptools import setup

setup(
    name='TbaneKart',
    version='1.0.0',
    install_requires=[
        'utm==0.4.2',
        'gevent==1.3a2',
        'flask==0.12.2',
        'requests==2.18.4',
        'python-dateutil==2.7.0',
        'flask-cors==3.0.3'
    ]
)

print('')
print('Remember to copy/rename init.example.js to init.js, and fill out the information in the variables.')
print('')
