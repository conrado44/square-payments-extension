from setuptools import setup, find_packages

setup(
    name="square-payments-extension",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "squareup>=42.0.0",
    ],
    entry_points={
        "goose.extensions": [
            "square_payments = square_payments_extension:SquarePaymentsExtension",
        ],
    }
)