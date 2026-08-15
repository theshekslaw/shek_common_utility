from shek_common_utility import (
    AsyncHTTPClient,
    BaseServiceSettings,
    __version__,
    configure_logging,
    get_logger,
)
from shek_common_utility.brain_client import BrainClient
from shek_common_utility.model_engine_client import ModelEngineClient


def test_version_exposed() -> None:
    assert __version__ == "0.1.0"


def test_settings_defaults() -> None:
    class MySettings(BaseServiceSettings):
        pass

    settings = MySettings()
    assert settings.service_name == "unnamed-service"
    assert settings.log_level == "INFO"
    assert settings.log_json is True


def test_configure_logging_smoke() -> None:
    configure_logging(service="test-service", level="DEBUG", json=False)
    logger = get_logger("smoke")
    logger.info("hello", key="value")


def test_client_construction() -> None:
    client = AsyncHTTPClient(base_url="http://localhost:8000", auth_token="t")
    assert client is not None

    me = ModelEngineClient(base_url="http://localhost:8000")
    assert me is not None

    br = BrainClient(base_url="http://localhost:8001")
    assert br is not None
