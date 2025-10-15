# Django Polls Application

A poll application built with Django for Software Engineering course.

[![Build Status](https://travis-ci.org/YOUR_USERNAME/swe1-app.svg?branch=main)](https://travis-ci.org/YOUR_USERNAME/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/YOUR_USERNAME/swe1-app/badge.svg?branch=main)](https://coveralls.io/github/YOUR_USERNAME/swe1-app?branch=main)

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username in the badge URLs above.

## Technologies
- Django 5.2.6
- Python 3.11
- SQLite
- Travis CI
- AWS Elastic Beanstalk
- Coverage.py
- Black (code formatting)
- Flake8 (linting)

## Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Run the development server
python3 manage.py runserver
```

## Testing
```bash
# Run tests
python manage.py test

# Check code formatting
black --check .

# Run linter
flake8 .

# Run coverage
coverage run --source='.' manage.py test
coverage report
```

## CI/CD Pipeline
This project uses Travis CI for continuous integration and deployment:
- Code formatting check with Black
- Linting with Flake8
- Test coverage with Coverage.py
- Automatic deployment to AWS Elastic Beanstalk on successful tests
