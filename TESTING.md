# Test Results

The Manual Testing document can be found here : [ Manual Test Results](/assets/testing/manual-testing.numbers).

## Test Strategy

The test strategy consisted of a combination of manual and automated tests.

- Parts of the appliction rely on CRUD operations to an external DB, and manual test cases were created to ensure isolate those tests that require internet access (Otherwise, a test could fail due to internet connectivity or some server error at the DB site although its application logic was correct). Partially it was started to mock the DB using `django-pytest` and `pytest_factoryboy` , but in the interest of time it was chosen to follow a manual test strategy here.
- The main parts of automated testing focussed on python unit testing with the pytest framework. Most of the functions were isolated from Django in separate files, in order to ensure atomic unit testing of pure application logic following a principle of **design for testability**. The Django functions then simply import the tested functions using pythons `import` statement.
- The modules for JS were tested only manually and via syntax validators

## Table of Contents

- [Test Strategy](#test-strategy)
- [Table of Contents](#table-of-contents)
- [Manual Tests](#manual-tests)
  - [Tests of Accessibility](#tests-of-accessibility)
    - [Results A11y Color Test](#results-a11y-color-test)
    - [Results WebAIM Accesibility Test](#results-webaim-accesibility-test)
    - [Results Chrome Lighthouse](#results-chrome-lighthouse)
  - [Tests for Compatibility](#tests-for-compatibility)
  - [Results W3C HTML Validation](#results-w3c-html-validation)
  - [Results Jshint Javascript Validation](#results-jshint-javascript-validation)
  - [Results Flake8 Python Syntax Validation](#results-flake8-python-syntax-validation)
  - [Results of Authentication Tests](#results-of-authentication-tests)
- [Functionality Tests](#functionality-tests)
  - [Results of User Profile Functionality Tests](#results-of-user-profile-functionality-tests)
  - [Results of Comments + Ratings Functionality Tests](#results-of-comments--ratings-functionality-tests)
  - [Results of Checkout Functionality Tests](#results-of-checkout-functionality-tests)
  - [Results of Products Functionality Tests](#results-of-products-functionality-tests)
  - [Results of Testing the deployed version](#results-of-testing-the-deployed-version)
  - [Results of Marketing Functionality Tests](#results-of-marketing-functionality-tests)
  - [Results of Accessibility Tests](#results-of-accessibility-tests)
  - [Results of Syntax Validation Tests](#results-of-syntax-validation-tests)
  - [Results of Browser Compatibility Tests](#results-of-browser-compatibility-tests)
  - [Issues Found During Manual Testing](#issues-found-during-manual-testing)
- [Automated Tests](#automated-tests)
  - [Results of pytest automated testing](#results-of-pytest-automated-testing)
  - [Coverage Report](#coverage-report)
  - [Running the Tests on Github Actions](#running-the-tests-on-github-actions)

---

## Manual Tests

### Tests of Accessibility

#### Results A11y Color Test

#### Results WebAIM Accesibility Test

#### Results Chrome Lighthouse

### Tests for Compatibility

### Results W3C HTML Validation

### Results Jshint Javascript Validation

### Results Flake8 Python Syntax Validation

### Results of Authentication Tests

## Functionality Tests

### Results of User Profile Functionality Tests

### Results of Comments + Ratings Functionality Tests

### Results of Checkout Functionality Tests

### Results of Products Functionality Tests

### Results of Testing the deployed version

### Results of Marketing Functionality Tests

### Results of Accessibility Tests

### Results of Syntax Validation Tests

### Results of Browser Compatibility Tests

### Issues Found During Manual Testing

---

## Automated Tests

### Results of pytest automated testing

### Coverage Report

### Running the Tests on Github Actions
