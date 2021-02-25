from unittest import TestCase
from unittest.mock import *
from mongo_system_log.system_log import LogThis, get_module_name
from datetime import datetime
from pymongo import MongoClient
import mongomock


class MongoConnectionHelper:

    @mongomock.patch(servers=(('server.test.com', 27017),))
    def __init__(self):
        self.client = MongoClient('server.test.com')
        self.db = self.client['test']


class LogThisTestCase(TestCase):

    @patch('mongo_system_log.mongodb_connector.connect')
    @patch('mongo_system_log.system_log.LogThis.get_host_ip')
    @patch('mongo_system_log.system_log.LogThis.get_hostname')
    def setUp(self, mock_hostname, mock_ip, mock_mongo_connect):
        mock_hostname.return_value = 'HostNameTest'
        mock_ip.return_value = '127.0.0.1'
        self.mongo_cli = MongoConnectionHelper()
        self.log = LogThis(get_module_name())
        self.date = datetime.now()
        mock_mongo_connect.return_value = self.mongo_cli

    @patch('mongo_system_log.system_log.socket')
    @patch('mongo_system_log.system_log.logging.error')
    def test_get_host_ip_method_when_make_an_exception_should_return_specific_text(
            self,
            mock_logging_error,
            mock_socket,
    ):
        mock_socket.side_effect = Exception('socket error')
        mock_logging_error.return_value = None
        expected = 'N/A'
        host = LogThis(get_module_name()).get_host_ip()
        self.assertEqual(expected, host)

    @patch('mongo_system_log.system_log.gethostname')
    @patch('mongo_system_log.system_log.logging.error')
    def test_get_hostname_method_when_make_an_exception_should_return_specific_text(
            self,
            mock_logging_error,
            mock_socket,
    ):
        mock_socket.side_effect = Exception('socket error')
        mock_logging_error.return_value = None
        expected = 'N/A'
        host = LogThis(get_module_name()).get_hostname()
        self.assertEqual(expected, host)

    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_info_method_must_call_send_mongo_method(self, mock_send_mongo):
        mock_send_mongo.return_value = None
        LogThis(get_module_name()).info('msg_info')
        mock_send_mongo.assert_called_with('info', msg='msg_info', payload=None, result=None)

    @patch('mongo_system_log.system_log.logging.info')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_info_method_when_send_mongo_method_return_None_should_not_call_logging_info(
            self,
            mock_send_mongo,
            mock_log_info
    ):
        mock_send_mongo.return_value = None
        LogThis(get_module_name()).info('msg_info')
        mock_log_info.assert_not_called()

    @patch('mongo_system_log.system_log.logging.info')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_info_method_when_send_mongo_method_return_id_mongo_should_call_logging_info(
            self,
            mock_send_mongo,
            mock_log_info
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).info('msg_info')
        mock_log_info.assert_called_with(f'log_id:id_mongo, Message:msg_info, Module:{get_module_name()[0]}, '
                                         f'App:{get_module_name()[1]}, Payload:None, Result:None')

    @patch('mongo_system_log.system_log.logging.info')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_info_method_when_send_mongo_method_return_id_mongo_and_log_console_is_False_should_not_call_logging_info(
            self,
            mock_send_mongo,
            mock_log_info
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).info('msg_info', log_console=False)
        mock_log_info.assert_not_called()

    @patch('mongo_system_log.system_log.logging.info')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_info_method_when_send_mongo_method_return_id_mongo_and_log_details_is_False_should_call_logging_info(
            self,
            mock_send_mongo,
            mock_log_info
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).info('msg_info', log_detail=False)
        mock_log_info.assert_called_with('log_id:id_mongo, Message:msg_info')

    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_error_method_must_call_send_mongo_method(self, mock_send_mongo):
        mock_send_mongo.return_value = None
        LogThis(get_module_name()).error('msg_error')
        mock_send_mongo.assert_called_with('error', msg='msg_error', payload=None, result=None)

    @patch('mongo_system_log.system_log.logging.error')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_error_method_when_send_mongo_method_return_None_should_not_call_logging_error(
            self,
            mock_send_mongo,
            mock_log_error
    ):
        mock_send_mongo.return_value = None
        LogThis(get_module_name()).error('msg_error')
        mock_log_error.assert_not_called()

    @patch('mongo_system_log.system_log.logging.error')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_error_method_when_send_mongo_method_return_id_mongo_should_call_logging_error(
            self,
            mock_send_mongo,
            mock_log_error
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).error('msg_error')
        mock_log_error.assert_called_with(f'log_id:id_mongo, Message:msg_error, Module:{get_module_name()[0]}, '
                                          f'App:{get_module_name()[1]}, Payload:None, Result:None')

    @patch('mongo_system_log.system_log.logging.error')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_error_method_when_send_mongo_method_return_id_mongo_and_log_console_is_False_should_not_call_logging_error(
            self,
            mock_send_mongo,
            mock_log_error
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).error('msg_error', log_console=False)
        mock_log_error.assert_not_called()

    @patch('mongo_system_log.system_log.logging.error')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_error_method_when_send_mongo_method_return_id_mongo_and_log_details_is_False_should_call_logging_error(
            self,
            mock_send_mongo,
            mock_log_error
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).error('msg_error', log_detail=False)
        mock_log_error.assert_called_with('log_id:id_mongo, Message:msg_error')

#
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_critical_method_must_call_send_mongo_method(self, mock_send_mongo):
        mock_send_mongo.return_value = None
        LogThis(get_module_name()).critical('msg_critical')
        mock_send_mongo.assert_called_with('critical', msg='msg_critical', payload=None, result=None)

    @patch('mongo_system_log.system_log.logging.critical')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_critical_method_when_send_mongo_method_return_None_should_not_call_logging_critical(
            self,
            mock_send_mongo,
            mock_log_critical
    ):
        mock_send_mongo.return_value = None
        LogThis(get_module_name()).critical('msg_critical')
        mock_log_critical.assert_not_called()

    @patch('mongo_system_log.system_log.logging.critical')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_critical_method_when_send_mongo_method_return_id_mongo_should_call_logging_critical(
            self,
            mock_send_mongo,
            mock_log_critical
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).critical('msg_critical')
        mock_log_critical.assert_called_with(f'log_id:id_mongo, Message:msg_critical, Module:{get_module_name()[0]}, '
                                             f'App:{get_module_name()[1]}, Payload:None, Result:None')

    @patch('mongo_system_log.system_log.logging.critical')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_critical_method_when_send_mongo_method_return_id_and_log_console_is_False_should_not_call_logging_critical(
            self,
            mock_send_mongo,
            mock_log_critical
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).critical('msg_critical', log_console=False)
        mock_log_critical.assert_not_called()

    @patch('mongo_system_log.system_log.logging.critical')
    @patch('mongo_system_log.system_log.LogThis._send_mongo')
    def test_critical_method_when_send_mongo_method_return_id_and_log_details_is_False_should_call_logging_critical(
            self,
            mock_send_mongo,
            mock_log_critical
    ):
        mock_send_mongo.return_value = 'id_mongo'
        LogThis(get_module_name()).critical('msg_critical', log_detail=False)
        mock_log_critical.assert_called_with('log_id:id_mongo, Message:msg_critical')

    @patch('mongo_system_log.system_log.datetime')
    @patch('mongo_system_log.system_log.ConnectMongo')
    @patch('pymongo.collection.Collection.insert_one')
    def test_send_mongo_should_call_insert_one_method(
            self,
            mock_insert_one,
            mock_mongodb_connection,
            mock_datetime
    ):
        mock_datetime.now.return_value = self.date
        mock_mongodb_connection.return_value = self.mongo_cli
        self.log._send_mongo('info', 'test_send_mongo', None, None)
        mock_insert_one.assert_called()

    @patch('mongo_system_log.system_log.logging.critical')
    @patch('mongo_system_log.system_log.datetime')
    @patch('mongo_system_log.system_log.ConnectMongo')
    def test_send_mongo_when_receive_an_exception_should_call_logging_critical_and_return_None(
            self,
            mock_mongodb_connection,
            mock_datetime,
            mock_log_critical
    ):
        mock_datetime.now.return_value = self.date
        mock_mongodb_connection.side_effect = Exception('an exception occurred')
        result = self.log._send_mongo('info', 'test_send_mongo', None, None)
        mock_log_critical.assert_called()
        self.assertIsNone(result)


