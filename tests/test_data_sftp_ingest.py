import pytest
from unittest.mock import patch, MagicMock
from data-processing-pipeline.data_sftp_ingest import sftp_ingest

def test_download_from_sftp_success():
    with patch("paramiko.Transport") as mock_transport:
        mock_sftp = MagicMock()
        mock_transport.return_value.connect.return_value = True
        mock_transport.return_value.open_session.return_value = True
        mock_sftp.get = MagicMock()
        
        # Patch SFTPClient from_transport
        with patch("paramiko.SFTPClient.from_transport", return_value=mock_sftp):
            sftp_ingest(
                sftp_host="fake_host",
                sftp_port=22,
                sftp_user="fake_user",
                sftp_password="fake_pass",
                remote_path="/remote/file_test.csv",
                local_path="local__test_file.csv"
            )
            mock_sftp.get.assert_called_once_with("/remote/file.csv", "local_file.csv")

def test_download_from_sftp_exception():
    with patch("paramiko.Transport", side_effect=Exception("Connection error")):
        with pytest.raises(Exception) as exc_info:
            sftp_ingest(
                sftp_host="fake_host",
                sftp_port=22,
                sftp_user="fake_user",
                sftp_password="fake_pass",
                remote_path="/remote/file.csv",
                local_path="local_test_file.csv"
            )
        assert "Connection error" in str(exc_info.value)