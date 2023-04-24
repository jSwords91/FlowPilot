from setuptools import setup, find_packages

setup(
    name="FlowPilot",
    version="0.1.9",
    description="A library for managing data processing workflows",
    author="Josh Swords",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
