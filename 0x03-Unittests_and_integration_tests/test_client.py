#!/usr/bin/env python3
"""
client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        client = GithubOrgClient("test_org")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")

    @patch('client.get_json')
    @patch(
        'client.GithubOrgClient._public_repos_url', new_callable=PropertyMock
    )
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Unit test for GithubOrgClient.public_repos
        """
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/test_org/repos"
        )
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        client = GithubOrgClient("test_org")

        result = client.public_repos()

        expected_result = ["repo1", "repo2", "repo3"]

        self.assertEqual(result, expected_result)

        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test_org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test the has_license method
        """
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(
    [
        {
            "org_payload": org_payload,
            "repos_payload": repos_payload,
            "expected_repos": expected_repos,
            "apache2_repos": apache2_repos,
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient class using fixtures
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up patching for requests.get
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Configure side_effect to return appropriate payloads
        def side_effect(url, *args, **kwargs):
            if url.endswith("/repos"):
                return MockResponse(cls.repos_payload, 200)
            return MockResponse(cls.org_payload, 200)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop patching
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test GithubOrgClient.public_repos integration
        """
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test GithubOrgClient.public_repos with license filter
        """
        # Update the mock to return filtered repos
        self.mock_get.side_effect = lambda url, *args, **kwargs: MockResponse(
            self.apache2_repos if "apache-2.0" in url else self.repos_payload,
            200
        )

        client = GithubOrgClient("test_org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


class MockResponse:
    """
    Mock Response object for simulating requests
    """

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


if __name__ == '__main__':
    unittest.main()
