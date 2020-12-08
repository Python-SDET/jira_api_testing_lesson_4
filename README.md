"# jira_api_testing_lesson_4" 

Going thorough all the commits in the repository will help reveal the steps

1) Renamed test file to test_cases.py  
  a. Put code for issue test case in it's own function  
  b. Started off by writing an function stub for the sprint test case using comments as test step  
  c. Added calls to function stubs in implementation.py  
  d. Raise not implemented exception while putting in the function stubs  
  
2) implementation.py  
  a. Added function stubs for create_sprint, set_name, set_start_date, set_end_date, set_goal, set_state  
  b. Raise not implemented exception in each until the code for each of these is complete  
  c. Added call to function that returnsresults for a jql query string  
  
 3) jira_api.py  
  a. Added function for partial_sprint_update because it uses a post instead of a put like many other update transactions  
  b. Added function to return results for a jql query string  
  
  4) Once all the functions that are needed has been added to jira_api.py, start adding calls those needed functions in order to code 
  the function stubs in implementation.py and remove the not implemented exceptions are each one is completed.
  
  5) Once all the function stubs are completed in implementation.py and the calls in test_cases.py are confirmed to work, 
  the not implemented exception can be removed from there as well.



