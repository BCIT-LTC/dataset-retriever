from django.test import TestCase
from unittest.mock import patch, MagicMock
from task_functions.tasks import execute_sequential_tasks

class ExecuteSequentialTasksTest(TestCase):

    @patch('task_functions.tasks.renew_token.s')
    @patch('task_functions.tasks.fetch_datahub_data_task.s')
    @patch('task_functions.tasks.filter_objects_task.s')
    @patch('task_functions.tasks.process_datasets_task.s')
    @patch('task_functions.tasks.download_and_extract_files_task.s')
    @patch('task_functions.tasks.chain')
    def test_execute_sequential_tasks(self, mock_renew, mock_fetch, mock_filter, mock_process, mock_download, mock_chain):
        # Arrange
        arg = 20
        mock_renew.return_value = "access_token"
        mock_fetch.return_value = {'Objects': [{'Full': {'Name': 'Role Details', 'ExtractsLink': 'http://example.com'}}]}
        mock_filter.return_value = [{'Full': {'Name': 'Role Details', 'ExtractsLink': 'http://example.com'}}]
        mock_process.return_value = [{'Name': 'RoleDetails', 'ExtractsLink': 'http://example.com'}]
        mock_download.return_value = None
        mock_chain.return_value = None

        # Act
        execute_sequential_tasks(arg)
        
        # Assert
        mock_renew.assert_called_once_with(arg)
        mock_fetch.assert_called_once()
        mock_filter.assert_called_once_with(['Role Details', 'Users', 'Organizational Units', 'Enrollments and Withdrawals'], 'Full')
        mock_process.assert_called_once_with(mock_filter.return_value, 'Full')
        mock_download.assert_called_once_with(mock_process.return_value)
        mock_chain.assert_called_once_with(
            mock_renew.return_value,
            mock_fetch.return_value,
            mock_filter.return_value,
            mock_process.return_value,
            mock_download.return_value
        )
        mock_chain().apply_async.assert_called_once_with(link_error=MagicMock())