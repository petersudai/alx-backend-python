#!/usr/bin/env python3
"""
client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for GithubOrgClient class
    """
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected__response, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        """
        mock_get_json.return_value = expected_response

        client = GithubOrgClient(org_name)

        self.assertEqual(client.org(), expected_response)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that GithubOrgClient.__public_repos_url returns correct URL
        """
        mock_org.return_value = {
                "repos_url" : "https://api.github.com/orgs/test_org/repos"
                }

        client = GithubOrgClient("test_org")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")


if __name__ == '__main__':
    unittest.main()
