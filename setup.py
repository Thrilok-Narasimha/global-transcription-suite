from setuptools import setup, find_packages

setup(
    name="translate_scribe",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional GUI-based transcription and translation app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/translate_scribe",
    packages=find_packages(),
    install_requires=[
        "speechrecognition",
        "googletrans==4.0.0rc1",
        "pycountry"
    ],
    python_requires=">=3.7",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "translate-scribe=translate_scribe.main:run",  # if you want a CLI
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
