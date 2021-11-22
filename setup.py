from setuptools import setup, find_packages


install_requires = [
    "hbp-validation-framework",
    "spur",
    "kg-core",
    "argh",
    "watchdog",
    "pygit",
    "pygithub"
]

setup(
    name='check-model',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/fbonnier/check_model.git',
    license="CeCILL",
    author='Florent Bonnier',
    author_email='florent.bonnier@cnrs.fr',
    description='EBRAINS Validation script generator',
    # Requirements
    install_requires=install_requires,
)
