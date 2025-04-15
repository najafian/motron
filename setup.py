from setuptools import setup, find_packages

setup(
    name="motron",
    version="0.1.2",
    packages=find_packages(where="src/main"),
    package_dir={"": "src/main"},
    install_requires=[
        "flask==2.3.2",
        "apscheduler==3.9.1",
        "pydantic<2.0",
        "PyYAML>=6.0.1",
        "Werkzeug~=3.1.3"
    ],
    include_package_data=True,
    zip_safe=False,
)
