import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-discord-jmurrayufo",
    version="0.0.1",
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
)
