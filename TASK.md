# 1 write a program which will be able to get currency exchange  rate from 
# https://openexchangerates.org/(to get access to this API you should get an API key firstly)


  * a. Write two implementations - on urllib and requests
  * b. Log every request to a log file.If file dose not exists - create it.If it exists already - append to the file.
  * c.Write custom exceptions to handle all network errors.Try to write it as much  as possible.
  * d.Store currency exchange rate in DB.Use custom ORM from prevision module.
  * e. Add tests;
  * Add file with dependencies.


# 2 Write a scrapper to solve the same issue as in previous task but from this page
  # https://bank.gov.ua/control/uk/curmetal/detail/currency?period=daily
  
  * a. Use the most convenient for you scrapper tool;
  * b. Use logging to write all requests;
  * c. Write custom exceptions to handle all network and scrapper errors;
  * d. Store scrapping result in DB.Use custom ORM from prevision module;
  * e. Add tests. Use mocks or vcr cassettes;
  * Add file with dependencies.
