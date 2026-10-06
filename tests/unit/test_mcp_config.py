from qa_mcp.config import PlaywrightMCPConfig


def test_mcp_config_is_target_scoped_and_non_secret() -> None:
    config = PlaywrightMCPConfig.from_env({"SHOPDEMO_BASE_URL": "http://localhost:3000/"})

    assert config.base_url == "http://localhost:3000"
    assert config.command == "npx"
    assert config.package.startswith("@playwright/mcp@")
