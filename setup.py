import setuptools
from distutils.util import convert_path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

main_ns = {}
ver_path = convert_path('src/simple_discord/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setuptools.setup(
    name="simple-discord-jmurrayufo",
    version=main_ns['__version__'],
    author="John Murray",
    author_email="jmurrayufo@gmail.com",
    description="A simple implementation of the discord API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmurrayufo/simple-discord",
    project_urls={
        "Bug Tracker": "https://github.com/jmurrayufo/simple-discord/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    license='GPLv3',
    platforms=['any'],
)
