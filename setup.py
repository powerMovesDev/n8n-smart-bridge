# setup.py

from setuptools import setup, find_packages

setup(
    name='n8n_smart_bridge',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any dependencies here
    ],
    author='Power Moves Development LLC',
    author_email='info@powermoves.io',
    description='A Python library to interact with n8n',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/n8n_library',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
