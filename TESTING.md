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
- [Functionality Tests / User Stories Test](#functionality-tests--user-stories-test)
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

## Functionality Tests / User Stories Test

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

There were several issues found during Manual Testing that required refactoring of the code to make it pass the test.

<table style="width:90%">
    <tr>
        <th style="text-align:center;width:10%"> Test Case</th>
        <th style="width:35%"> Description </th>
        <th style="width:60%"> Errors Found  </th>
    </tr>
    <tr>
      <td style="text-align:center"> TC_19 </td>
      <td> Validate that all pages pass W3C HTML Validation Tool (Landing Page)   </td>
      <td> 
         <ul>
            <li> In the first round, the HTML validator noted a stray div HTML element at the end of the landing page, and raised an error. </li>
            <li> After removing the stray div, the test passed </li>
         </ul>
     </td>
    </tr>
    <tr>
      <td style="text-align:center"> TC_19 </td>
      <td> Validate that all pages pass W3C HTML Validation Tool (Product Detail Page)   </td>
      <td> 
         <ul>
            <li> In the first round, the HTML validator noted:  a div inside a label element,  an unclosed div elemen end of a form element but but no opening element of a form, a duplicate 'class attribute' and an unclosed paragraph </li>
            <li> After adjusting the HTML code, the test passed </li>
         </ul>
     </td>
    </tr>
    <tr>
      <td style="text-align:center"> TC_19 </td>
      <td> Validate that all pages pass W3C HTML Validation Tool  (Shopping Bag Page)    </td>
      <td> 
         <ul>
            <li> In the first round, the HTML validator noted: a quote in an attribute name , and unclosed body tag and an unclosed div </li>
            <li> After adjusting the HTML code, the test passed </li>
         </ul>
    </td>
    </tr>
    <tr>
      <td style="text-align:center"> TC_19 </td>
      <td> Validate that all pages pass W3C HTML Validation Tool  (Checkout Page)    </td>
      <td> 
         <ul>
            <li> In the first round, the HTML validator noted: a quote in an attribute name , a stray end div, and that the value for a for label did not have a matching ID of a form control element </li>
            <li> After adjusting the HTML code, the test still failed with an error regarding the label of the country form field </li>
            <img src="./assets/testing/html-checkout-crispy-1.png"; alt="error message of HTML validator that was left unfixed - Argumentation: this part of the HTML was rendered by Tailwind-Crispyforms" > 
            <img src="./assets/testing/html-checkout-crispy-2.png"; alt="error message of HTML validator that was left unfixed - Argumentation: this part of the HTML was rendered by Tailwind-Crispyforms" > 
            <li> This part of the HTML is rendered by `Crispy-Tailwind` [Link](https://django-crispy-forms.github.io/crispy-tailwind/). It did not seem reasonable in terms of code readibility and maintainability to overwrite the behaviour of this package.</li>
            <li> Aside from this single error, the test passes. </li>
         </ul>
    </td>
    </tr>
     <tr>
      <td style="text-align:center"> TC_19 </td>
      <td> Validate that all pages pass W3C HTML Validation Tool  (Checkout Success Page)    </td>
      <td> 
         <ul>
            <li> In the first round, the HTML validator noted: an obsolete scope element in the td element which should only be used in the th element (table header).  </li>
            <li> After adjusting the HTML code, the test passed </li>
         </ul>
    </td>
    </tr>
     <tr>
      <td style="text-align:center"> TC_19 </td>
      <td> Validate that all pages pass W3C HTML Validation Tool  (Profile Page)    </td>
      <td> 
         <ul>
            <li> In the first round, the HTML validator noted: Element ul not allowed as child of element ul,End tag td seen, but there were open element, Unclosed element ul  , Quote ' in attribute name, Duplicate ID error,the value of the for attribute of the label element must be the ID of a non-hidden form control. </li>
            <li> After adjusting the HTML code, the test still failed with the same error as the Checkout Page complaining about the country form fields rendered by Crispy-Tailwind </li>
            <img src="./assets/testing/html-profile-crispy-1.png"; alt="error message of HTML validator that was left unfixed - Argumentation: this part of the HTML was rendered by Tailwind-Crispyforms" > 
            <img src="./assets/testing/html-profile-crispy-2.png"; alt="error message of HTML validator that was left unfixed - Argumentation: this part of the HTML was rendered by Tailwind-Crispyforms" > 
            <li> This part of the HTML is rendered by `Crispy-Tailwind` [Link](https://django-crispy-forms.github.io/crispy-tailwind/). It did not seem reasonable in terms of code readibility and maintainability to overwrite the behaviour of this package.</li>
            <li> Aside from this single error, the test passes. </li>
         </ul>
    </td>
    </tr>
    <tr>
      <td style="text-align:center"> TC_19 </td>
      <td> Validate that all pages pass W3C HTML Validation Tool  (Signup Page)    </td>
      <td> 
         <ul>
            <li> In the first round, the HTML validator noted an Error: Element ul not allowed as child of element small in this context. (Suppressing further errors from this subtree.).  </li>
             <img src="./assets/testing/html-signup-crispy-1.png"; alt="error message of HTML validator that was left unfixed - Argumentation: this part of the HTML was rendered by Tailwind-Crispyforms" > 
            <img src="./assets/testing/html-signup-crispy-2.png"; alt="error message of HTML validator that was left unfixed - Argumentation: this part of the HTML was rendered by Tailwind-Crispyforms" > 
            <li> This part of the HTML is rendered by `Crispy-Tailwind` [Link](https://django-crispy-forms.github.io/crispy-tailwind/). It did not seem reasonable in terms of code readibility and maintainability to overwrite the behaviour of this package.</li>
            <li> Aside from this single error, the test passes. </li>
         </ul>
    </td>
    </tr>
</table>

---

## Automated Tests

### Results of pytest automated testing

### Coverage Report

### Running the Tests on Github Actions
