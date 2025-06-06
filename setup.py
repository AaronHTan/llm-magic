from setuptools import setup, find_packages

setup(
    name="llm-magic",
    version="0.1.0",
    description="Custom Jupyter magic for LLM integration",
    author="AI Developer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ipython>=8.0.0",
        "jupyter>=1.0.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "pyyaml>=6.0",
        "rich>=12.0.0",
        "anthropic>=0.3.0",
        "openai>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)