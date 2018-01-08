from setuptools import setup, find_packages


setup(
    name='dxe-fb',
    version='1.0',
    description='get list of members of facebook group',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
    ],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'get_members = get_members:main',
        ]
    }
)
