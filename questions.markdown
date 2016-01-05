* Are agency contact name, email, and phone redundent with the info in the related agency? Is the name for the agency the contact for all programs within that agency? 
* Can avgApplicationTime, currentEmployeesRequired,  annualRevenue, age be converted from strings to ranges of two integers?
  * If so can we have humans manually migrate some of this information?  Probably only afew days of data entry.
  * If so how soon can we have people do that? I could have something that people could use in a week or two easily.
* Should all of the dropdowns and multiselects be converted from strings to foreign keys?
* Agencies have sparse data on emails but each opp. has an agnecy email, should we fix this?
* To what extent is the industry list exhaustive and complete? Does it need changing? Could it be representedin a better way? 
* What does average application time mean? What unit does PR want to use (hopefully all days)? Does a range work? Does this need to be searchable? If not, then it can be a string. Do we need to encompass more information that a range does? 
* Questions related to notifications
  * is each opportunity updated when it passes the deadline? what does deadline refer to specifically (when program expires as written in policy or end of application window)
  * do some opportunities have recurring application windows? How are those currently noted? 
  * are there recurring opportunities? 
  * how often are opportunities edited? should we notify folks that it has been updated? 


