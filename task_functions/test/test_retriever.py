from django.test import TestCase
from unittest.mock import patch, MagicMock
from task_functions.tasks import (
    fetch_datahub_data_task,
    filter_objects_task,
    process_datasets_task,
    download_and_extract_files_task,
    execute_sequential_tasks
)

class RetrieverTestCase(TestCase):

    @patch('task_functions.tasks.cache.get', return_value='mock_access_token')
    @patch('task_functions.tasks.fetch_datahub_data_task.apply_async', return_value=MagicMock())
    @patch('task_functions.tasks.filter_objects_task.apply_async', return_value=MagicMock())
    @patch('task_functions.tasks.process_datasets_task.apply_async', return_value=MagicMock())
    @patch('task_functions.tasks.download_and_extract_files_task.apply_async', return_value=MagicMock())
    @patch('redis.StrictRedis')
    def test_execute_sequential_tasks_success(self, mock_redis, mock_download_and_extract_files, mock_process_datasets, mock_filter_objects, mock_fetch_datahub_data, mock_cache_get):
        # Mock the Redis connection
        mock_redis.return_value = MagicMock()

        # Mock the return values
        mock_fetch_datahub_data.return_value = MagicMock()
        mock_filter_objects.return_value = MagicMock()
        mock_process_datasets.return_value = MagicMock()
        mock_download_and_extract_files.return_value = MagicMock()

        # Call the task
        result = execute_sequential_tasks('some_argument')

        # Assertions
        self.assertIsNone(result)
        mock_fetch_datahub_data.assert_called_once()
        mock_filter_objects.assert_called_once()
        mock_process_datasets.assert_called_once()
        mock_download_and_extract_files.assert_called_once()
        mock_cache_get.assert_called_once()
        mock_redis.assert_called_once()

    @patch('task_functions.tasks.cache.get', return_value='mock_access_token')
    @patch('redis.StrictRedis')
    def test_execute_sequential_tasks_connection_error(self, mock_redis, mock_cache_get):
        # Mock the Redis connection to raise a connection error
        mock_redis.return_value = MagicMock()
        mock_redis.side_effect = Exception("Connection refused")

        # Call the task
        result = execute_sequential_tasks('some_argument')

        # Assertions
        self.assertIsNone(result)
        mock_redis.assert_called_once()

    @patch('task_functions.tasks.cache.get', return_value='mock_access_token')
    @patch('task_functions.tasks.fetch_datahub_data_task.apply_async', return_value=MagicMock())
    @patch('redis.StrictRedis')
    def test_execute_sequential_tasks_fetch_datahub_data_failure(self, mock_redis, mock_fetch_datahub_data, mock_cache_get):
        # Mock the Redis connection
        mock_redis.return_value = MagicMock()

        # Mock the return values
        mock_fetch_datahub_data.return_value = None

        # Call the task
        result = execute_sequential_tasks('some_argument')

        # Assertions
        self.assertIsNone(result)
        mock_fetch_datahub_data.assert_called_once()
        mock_cache_get.assert_called_once()
        mock_redis.assert_called_once()