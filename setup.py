from setuptools import setup, find_packages

setup(
    name="motron",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",  # Flask will still be a dependency, but DI will be custom
        # Add other necessary dependencies like scheduling libraries, etc.
    ],
    description="Motron - A Python-based framework mimicking Spring Boot.",
    author="Saeid",
    author_email="your.email@example.com",
)
