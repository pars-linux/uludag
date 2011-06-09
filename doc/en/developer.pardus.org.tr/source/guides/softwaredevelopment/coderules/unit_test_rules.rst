.. _unit-test-rules:

**Last Modified Date:** |today|

:Author: Beyza Ermiş

:Version: 0.1

Unit Test
~~~~~~~~~
A unit test is code that exercises a specific portion of your codebase in a particular context. Typically, each unit test sends a specific input to a method and verifies that the method returns the expected value, or takes the expected action. Unit tests prove that the code you are testing does in fact do what you expect it to do.
 
The Force.com platform requires that at least 75% of the Apex Code in an org be executed via unit tests in order to deploy the code to production. You shouldn’t consider 75% code coverage to be an end-goal though. Instead, you should strive to increase the state coverage of your unit tests. Code has many more possible states than it has lines of code. For example, the following method has 4,294,967,296 different states:

  *double getFraction(Integer a){ return 1/a;}*

Clearly, you wouldn’t want to test all of the different states for this program. Instead, you should probably test a few different inputs for this method, even if it means that you will have achieved 100% code coverage several times over.
Three different states that you might consider testing are a "positive" input, a "negative" input and a "0" input. Testing with a positive input, and with a negative input will behave as expected. Testing with a "0" input however will yield a surprise "System.MathException". This is just one example of why it makes sense to focus on testing the different states of your code instead of focusing on just the 75% code coverage requirement. 

You can see the cheatsheet: http://developer.pardus.org.tr/guides/softwaredevelopment/coderules/PardusUnitTestCheatSheet.pdf


The Value of Unit Tests
-----------------------
- One of the most valuable benefits of unit tests is that they give you confidence that your code works as you expect it to work. Unit tests give you the confidence to do long-term development because with unit tests in place, you know that your foundation code is dependable. Unit tests give you the confidence to refactor your code to make it cleaner and more efficient.

- Unit tests also save you time because unit tests help prevent regressions from being introduced and released. Once a bug is found, you can write a unit test for it, you can fix the bug, and the bug can never make it to production again because the unit tests will catch it in the future.

- Another advantage is that unit tests provide excellent implicit documentation because they show exactly how the code is designed to be used.  


Unit Test Structure
-------------------
Let’s take a look at how unit tests are best structured. All unit tests should follow the same basic structure.

A unit test should:
    - Set up all conditions for testing.
    - Call the method (or Trigger) being tested.
    - Verify that the results are correct.
    - Clean up modified records. 

Set Up All Conditions for Testing
---------------------------------
Typically, methods perform some sort of operation upon data. So in order to test your methods, you’ll need to set up the data required by the method. This might be **as simple as** declaring a few variables, or **as complex as** creating a number of records in the Force.com database. For example, if you have a trigger like this one that updates an Opportunity’s parent Account after the Opportunity is inserted::

 *trigger updateParentAccountWithOpportunityName on Opportunity (after insert) {*

      *// Create a Map from Account Ids to Opportunities.*

      *Map<Id, Opportunity> accountIdOpportunityMap = new Map<Id, Opportunity>();*

      for(Opportunity o&nbsp;: Trigger.new){

          *accountIdOpportunityMap.put(o.AccountId, o);*

      }

      *// Create a list of Accounts to Update.*

      *List<Account> accounts = new List<Account>();*

      for(Account a&nbsp;: [SELECT Id, Most_Recently_Created_Opportunity_Name__c 

          *FROM Account*

          *WHERE Id IN&nbsp;:accountIdOpportunityMap.keySet()]){*

          *a.Most_Recently_Created_Opportunity_Name__c = ((Opportunity) accountIdOpportunityMap.get(a.Id)).Name;*

          *accounts.add(a);*
      }

      *update accounts;*
  }

Then, your setup code could look something like this:
 
 *Account a = new Account(Name='My Account');*

 *insert a;*

 *Opportunity o = new Opportunity(AccountId=a.Id, Name='My Opportunity', StageName='Prospecting', CloseDate=Date.today());*

Your unit tests should always create their own test data to execute against. That way, you can be confident that your tests aren’t dependent upon the state of a particular environment and will be repeatable even if they are executed in a different environment from which they were written.  

Call the method (or Trigger) being tested
-----------------------------------------
Once you have set up the appropriate input data, you still need to execute your code. If you are testing a method, then you will call the method directly. In this case, we’re testing a Trigger, so we’ll need to perform the action that causes the trigger to execute. 
In our sample, that means that we will need to insert the Opportunity: 

 *insert o;*

Verify the results are correct
------------------------------
Verifying that your code works as you expect it to work is the most important part of unit testing. Unit tests that do not verify the results of the code aren’t true unit tests. A good way to tell if unit tests are properly verifying results is to look for liberal use of the *assert()* methods.

Clean up (is Easy!)
-------------------
Cleaning up after unit tests is easy, because there’s nothing to do! Actions performed on records inside of a unit test are not committed to the database. This means that we can insert, delete, and modify records without having to write any code that will clean up our changes. 


Where to put tests?
-------------------
It makes sense to put unit tests for your classes in a separate class file as well. The most important reason for this is that by separating your class implementation and your unit tests, you will automatically be prevented from testing private methods and private properties. You shouldn’t test private methods and private properties because doing so will cause your unit tests to become a barrier to refactoring. With your classes and unit tests separated in to different files, you will always have the option to **change the internal implementation of your classes** should the need arise. If you ever do find yourself compelled to test a private or protected method, this is probably a strong indication that the method should be refactored in to its own stand-alone class. 


What to Test
------------
Broadly speaking, you should test your custom business logic. How thoroughly you test that business logic will probably vary between situations. On one end of the spectrum, you might choose to implement just a few tests that only cover the code paths that you believe are most likely to contain a bug. On the other end of the spectrum, you might choose to implement a large suite of unit tests that are incredibly thorough and test a wide variety of scenarios. Wherever a given project falls on that spectrum, you should be sure to write unit tests that verify your code behaves as expected in **normal** scenarios as well as in more **unexpected** scenarios, like boundary conditions or error conditions.

Testing Unexpected Conditions
-----------------------------
There are many scenarios that your code shouldn’t encounter. However, you can’t trust that clients of your code will always do the right thing, so you have to make sure that the code will still handle these unexpected scenarios appropriately.  

Bad Input Values
----------------
One potentially unexpected condition that the code might encounter is an unexpected value, like null, being passed to the push() method. You have a few implementation options for handling this scenario. Your code could ignore the null value, it could insert a special placeholder value, or it could not allow null values to be pushed on to the Stack at all.

Boundary Conditions
-------------------
Boundary conditions are another common source of bugs. Let’s verify that our StringStack implementation handles the overflow and underflow boundary conditions.
EX: The Apex documentation indicates that a List can only contain 1,000 records. If a 1,001th object were to be added to our List-based Stack implementation, a System exception would be thrown.


Tips for writing great unit tests
---------------------------------
- Make each test orthogonal (i.e., independent) to all the others:
  Any given behaviour should be specified in one and only one test. Otherwise if you later change that behaviour, you’ll have to change multiple tests. The corollaries of this rule include:

    - Don’t make unnecessary assertions:
      Which specific behaviour are you testing? It’s counterproductive to Assert() anything that’s also asserted by another test: it just increases the frequency of pointless failures without improving unit test coverage one bit. This also applies to unnecessary Verify() calls – if it isn’t the core behaviour under test, then stop making observations about it! Sometimes, TDD folks express this by saying “have only one logical assertion per test”.
      Remember, unit tests are a design specification of how a certain behaviour should work, not a list of observations of everything the code happens to do.
    - Test only one code unit at a time:
      Your architecture must support testing units (i.e., classes or very small groups of classes) independently, not all chained together. Otherwise, you have lots of overlap between tests, so changes to one unit can cascade outwards and cause failures everywhere.
      If you can’t do this, then your architecture is limiting your work’s quality – consider using Inversion of Control.
    - Mock out all external services and state:
      Otherwise, behaviour in those external services overlaps multiple tests, and state data means that different unit tests can influence each other’s outcome.
      You’ve definitely taken a wrong turn if you have to run your tests in a specific order, or if they only work when your database or network connection is active.
      (By the way, sometimes your architecture might mean your code touches static variables during unit tests. Avoid this if you can, but if you can’t, at least make sure each test resets the relevant statics to a known state before it runs.)
    - Avoid unnecessary preconditions:
      Avoid having common setup code that runs at the beginning of lots of unrelated tests. Otherwise, it’s unclear what assumptions each test relies on, and indicates that you’re not testing just a single unit.
      An exception: Sometimes I find it useful to have a common setup method shared by a very small number of unit tests (a handful at the most) but only if all those tests require all of those preconditions. This is related to the context-specification unit testing pattern, but still risks getting unmaintainable if you try to reuse the same setup code for a wide range of tests.

- Don’t unit-test configuration settings:

    By definition, your configuration settings aren’t part of any unit of code (that’s why you extracted the setting out of your unit’s code). Even if you could write a unit test that inspects your configuration, it merely forces you to specify the same configuration in an additional redundant location. Congratulations: it proves that you can copy and paste!

- Name your unit tests clearly and consistently:

    If you’re testing how ProductController’s Purchase action behaves when stock is zero, then maybe have a test fixture class called PurchasingTests with a unit test called ProductPurchaseAction_IfStockIsZero_RendersOutOfStockView(). This name describes the subject (ProductController’s Purchase action), the scenario (stock is zero), and the result (renders “out of stock” view). I don’t know whether there’s an existing name for this naming pattern, though I know others follow it. How about S/S/R? 
    Avoid non-descriptive unit tests names such as Purchase() or OutOfStock(). Maintenance is hard if you don’t know what you’re trying to maintain.


Pytest
------
We-don't-need-no-stinking-API unit test suite, is an alternative, more Pythonic way of writing your tests. The best part is, the overhead for creating unit tests is close to zero!
Two rules:
1. Prefix the names of your test functions/methods with *test_* and the names of your test classes with Test
2. Save your test code in files that start with *test_*

That's about it in terms of API complexity. If you just run py.test in the directory that contains your tests, the tool will search the current directory and its subdirectories for files that start with *test_*, then it will automagically invoke all the test functions/methods it finds in those files. There is no need to inherit your test class from a framework-specific class, as is the case with unittest. 

To run the tests in test_sort.py, simply invoke:

# py.test test_*.py


Test organization
-----------------
The only requirement for a test file to be recognized as such by py.test is for the filename to start with *test_* (and even this can be customized), it is very easy to organize your tests in hierarchies and test suites by creating a directory tree and placing/grouping your test files in the appropriate directories. Then you can just run py.test with no arguments and let it find and execute all the test files for you. A carefully chosen naming scheme would certainly help you in this scenario.

A feature of py.test which is a pleasant change from unittest is that the test execution order is guaranteed to be the same for each test run, and it is simply the order in which the test function/methods appear in a given test file. No alphanumerical sorting order to worry about. 

Assertion syntax
----------------
There is no special assertion syntax in py.test. You can use the standard Python assert statements, and they will (again, magically) be interpreted by py.test so that more helpful error messages can be printed out. This is in marked contrast with unittest's custom and somewhat clunky assertEqual/assertTrue/etc. mechanism. 

    *def test_custom_sort(self):*

        *def int_compare(x, y):*

            *x = int(x)*

            *y = int(y)*

            *return x - y*

        *self.alist.sort(int_compare)*

        *assert self.alist == [1, 2, 3, 4, 5]*


        *b = ["1", "10", "2", "20", "100"]*

        *b.sort()*

        *assert b == ['1', '10', '100', '2', '20']*

        *b.sort(int_compare)*

        *assert b == ['1', '2', '10', '20', '100']*

Dealing with exceptions
-----------------------
The test_sort.py module contains an example of how exceptions can be handled with py.test:

*def test_sort_exception(self):*

    *import py.test*

    *py.test.raises(NameError, "self.alist.sort(int_compare)")*

    *py.test.raises(ValueError, self.alist.remove, 6)*

We needed to import py.test in my test code, in order to be able to use the raises() function it provides. This function takes the expected exception type as the first parameter. The other parameters are either

 - a string specifying the function or method call that is supposed to raise the exception, or
 - the actual callable, followed by its arguments

The more general form for the raises() function is:

*py.test.raises(Exception, "func(*args, **kwargs)")*
*py.test.raises(Exception, func, *args, **kwargs)*
