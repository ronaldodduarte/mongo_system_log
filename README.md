The idea behind this package is possibility to you use some client or something like the Metabase for collect and analyse logs of your application.  
Its return **mongodb_id** or **None** on exception case.

Its need two environments variables:  
* MONGO_DB  
* MONGO_URL      

Its works with three collections:  
* error  
* info  
* critical

Arguments:
* msg - Required
    * The message to log;
* payload - Default is None
    * If need to log a payload that make a some request;
* result - Default is None
    * If need to log a request result;
* log_console - boolean default is True
    * Enable or disable log console view;
* log_detail - boolean default is True
    * If disabled show only mongo_id and message.

Sample:
~~~python
from mongo_system_log import *
log = LogThis(get_module_name())
log.info('info message', payload='payload', result='result', log_console=False, log_detail=False)
log.error('error message', payload='payload', result='result')
log.critical('critical message', payload='payload', result='result')
~~~
get_module_name()  
* This function gets module and file name that called it. Must be called on instantiate the LogThis class.  
The arguments **payload** and **result** has default value None.

The document fields are:  
* Ip
* HostName
* App - File name that was executed;
* ModuleCalled - Module name where methods was called;
* Date -  Date Time on format 2010-12-12 11:41:42,612;
* Severity -  INFO, ERROR or CRITICAL;
* Message - The message that want be logged;
* Payload - A dict that used to call a request for example;
* Result - A request result.

### New method:
**custom**

Arguments:
* payload - Required
    * A dict that will be sent to MongoDb;
* collection - required
    * The collection that will receive the payload;
* msg_console - Default is string empty
    * The message that will be displayed on the console. It will not be sent to MongoDb;
* log_console - boolean default is True
    * Enable or disable log console view;
* log_detail - boolean default is True
    * If disabled show only mongo_id and message.


I suggest that You use the Metabase:  
https://www.metabase.com/

It is amazing to analyze logs.