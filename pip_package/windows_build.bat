pip install .
python setup.py sdist bdist_wheel
python -m twine upload --skip-existing dist/*