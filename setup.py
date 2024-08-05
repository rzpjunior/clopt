from setuptools import setup, find_packages

setup(
    name='clopt',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'flask',
        'dash',
        'pandas',
        'pydo',
        'python-dotenv',
        'plotly'
    ],
    entry_points={
        'console_scripts': [
            'clopt=app:main',
        ],
    },
)
