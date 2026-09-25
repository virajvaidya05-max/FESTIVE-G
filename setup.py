"""
Setup configuration for FESTIVE G package.

Run:
    pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="festive-g",
    version="1.0.0",
    description="Send personalized festival greetings with a beautiful web interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/festive-g",
    license="MIT",
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Package discovery
    packages=find_packages(),
    py_modules=["app"],
    
    # Package data (templates, static files)
    package_data={
        "": [
            "templates/*.html",
            "static/*.css",
            "static/images/*",
        ]
    },
    
    # Include template and static files in distribution
    include_package_data=True,
    
    # Runtime dependencies (none required - uses stdlib only)
    install_requires=[],
    
    # Optional dependencies for development
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "pylint>=2.0",
            "mypy>=0.9",
            "flake8>=4.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    
    # Entry point (optional - can run python app.py directly)
    entry_points={
        "console_scripts": [
            "festive-g=app:main",
        ],
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia",
    ],
    
    # Keywords for search
    keywords=[
        "festival",
        "greeting",
        "web",
        "http",
        "celebrations",
        "email",
        "diwali",
        "holi",
    ],
    
    # Project URLs
    project_urls={
        "Documentation": "https://github.com/yourusername/festive-g",
        "Source": "https://github.com/yourusername/festive-g",
        "Bug Reports": "https://github.com/yourusername/festive-g/issues",
    },
    
    # Zip safety
    zip_safe=False,
)
