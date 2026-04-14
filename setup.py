import setuptools

setuptools.setup(
    packages=setuptools.find_packages(include=["genai_code_test"]),
    install_requires=[
        'coverage==7.8.2',
        'gitpython',
        'numpy',
        'pandas',
        'pytest==9.0.3',
    ]
)