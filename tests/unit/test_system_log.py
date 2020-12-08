from unittest import TestCase
from unittest.mock import *
from mongo_system_log.system_log import LogThis, get_module_name
from datetime import datetime
from pymongo import MongoClient
import mongomock
from sys import argv


class MongoConnectionHelper:

    @mongomock.patch(servers=(('server.test.com', 27017),))
    def __init__(self):
        self.client = MongoClient('server.test.com')
        self.db = self.client['test']
        self.error_collection = self.db['error']
        self.info_collection = self.db['info']


class LogThisTestCase(TestCase):

    @patch('mongo_system_log.system_log.LogThis.get_host_ip')
    @patch('mongo_system_log.system_log.LogThis.get_hostname')
    def setUp(self, mock_hostname, mock_ip):
        mock_hostname.return_value = 'HostNameTest'
        mock_ip.return_value = '127.0.0.1'
        self.mongo_cli = MongoConnectionHelper()
        self.log = LogThis(get_module_name())
        self.date = datetime.now()

    @patch('mongo_system_log.system_log.ConnectMongo')
    @patch('mongo_system_log.system_log.logging.error')
    def test_error_method_must_call_logging_error(self, mock_logging_error, mock_mongodb_connection):
        self.log.error('error test')
        mock_mongodb_connection.return_value = self.mongo_cli
        mock_logging_error.assert_called_with(f"Message:error test, Module:test_system_log, App:{argv[0]}")

    @patch('mongo_system_log.system_log.ConnectMongo')
    @patch('mongo_system_log.system_log.datetime')
    @patch('pymongo.collection.Collection.insert_one')
    def test_error_method_must_call_insert_one_method(self, mock_insert_db, mock_datetime, mock_mongodb_connection):
        mock_mongodb_connection.return_value = self.mongo_cli
        mock_datetime.now.return_value = self.date
        self.log.error('error test')
        expected = {
            'Date': self.date,
            'Severity': 'ERROR', 'HostName': 'HostNameTest', 'MsgError': 'error test', 'Ip': '127.0.0.1',
            'ModuleCalled': 'test_system_log',
            'App': argv[0]
        }
        mock_insert_db.assert_called_with(expected)

    @patch('mongo_system_log.system_log.ConnectMongo')
    @patch('mongo_system_log.system_log.datetime')
    @patch('mongo_system_log.system_log.logging.error')
    @patch('pymongo.collection.Collection.insert_one')
    def test_error_method_when_insert_one_method_make_an_exception_should_log_it_on_console(
            self,
            mock_insert_db,
            mock_logging_error,
            mock_datetime,
            mock_mongodb_connection
    ):
        msg = 'error test'
        expected = {
            'Date': self.date,
            'Severity': 'ERROR', 'HostName': 'HostNameTest', 'MsgError': 'error test', 'Ip': '127.0.0.1',
            'ModuleCalled': 'test_system_log',
            'App': argv[0]
        }
        mock_mongodb_connection.return_value = self.mongo_cli
        mock_datetime.now.return_value = self.date
        mock_insert_db.side_effect = Exception('Connection error')
        self.log.error(msg)
        mock_logging_error.assert_called_with(f'Fail to send log for MongoDb - Connection error, Message:{expected}')

    @patch('mongo_system_log.system_log.ConnectMongo')
    @patch('mongo_system_log.system_log.logging.info')
    def test_info_method_must_call_logging_info(self, mock_logging_info, mock_mongodb_connection):
        self.log.info('info test')
        mock_mongodb_connection.return_value = self.mongo_cli
        mock_logging_info.assert_called_with(f"Message:info test, Module:test_system_log, App:{argv[0]}, "
                                             f"Payload:None, Result:None")

    @patch('mongo_system_log.system_log.ConnectMongo')
    @patch('mongo_system_log.system_log.datetime')
    @patch('pymongo.collection.Collection.insert_one')
    def test_info_method_must_call_insert_one_method(self, mock_insert_db, mock_datetime, mock_mongodb_connection):
        mock_datetime.now.return_value = self.date
        mock_mongodb_connection.return_value = self.mongo_cli
        self.log.info('info test')
        expected = {
            'Date': self.date,
            'Severity': 'INFO', 'MsgInfo': 'info test', 'Payload': None, 'Result': None,
            'Ip': '127.0.0.1', 'HostName': 'HostNameTest',
            'ModuleCalled': 'test_system_log',
            'App': argv[0]
        }
        mock_insert_db.assert_called_with(expected)

    @patch('mongo_system_log.system_log.ConnectMongo')
    @patch('mongo_system_log.system_log.datetime')
    @patch('mongo_system_log.system_log.logging.error')
    @patch('pymongo.collection.Collection.insert_one')
    def test_info_method_when_insert_one_method_make_an_exception_should_log_it_on_console(
            self,
            mock_insert_db,
            mock_logging_error,
            mock_datetime,
            mock_mongodb_connection
    ):
        msg = 'info test'
        expected = {
            'Date': self.date,
            'Severity': 'ERROR', 'MsgInfo': 'info test', 'Payload': None, 'Result': None,
            'Ip': '127.0.0.1', 'HostName': 'HostNameTest',
            'ModuleCalled': 'test_system_log',
            'App': argv[0]
        }
        mock_mongodb_connection.return_value = self.mongo_cli
        mock_datetime.now.return_value = self.date
        mock_insert_db.side_effect = Exception('Connection error')
        self.log.info(msg)
        mock_logging_error.assert_called_with(f'Fail to send log for MongoDb - Connection error, Message:{expected}')

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
