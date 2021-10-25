import setuptools
from distutils.util import convert_path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

main_ns = {}
ver_path = convert_path('src/dyscord/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setuptools.setup(
    name="dyscord",
    version=main_ns['__version__'],
    author="John Murray",
    author_email="jmurrayufo@gmail.com",
    description="A simple implementation of the discord API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isbe-house/dyscord",
    project_urls={
        "Bug Tracker": "https://github.com/isbe-house/dyscord/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    license='GPLv3',
    platforms=['any'],
    install_requires=[
        'cachetools>=4.2.4',
        'colour>=0.1.5',
        'emoji>=1.5.0',
        'httpx>=0.19.0',
        'nest_asyncio>=1.5.1',
        'orjson>=3.6.3',
        'requests>=2.26.0',
        'websockets>=10.0',
        'validators>=0.18.2',
    ],
)
