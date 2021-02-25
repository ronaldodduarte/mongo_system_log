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
log.info('error message', payload='payload', result='result', log_console=False, log_detail=False)
log.error('error message', payload='payload', result='result')
log.critical('error message', payload='payload', result='result')
~~~
get_module_name()  
* This function gets module and file name that called it. Must be called on instantiate the LogThis class.  
The arguments **payload** and **result** has default value None.
