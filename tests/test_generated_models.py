"""Tests for client-side validation in the generated NiFi API models.

These exercise the swagger templates and spec augmentations that produce
``nipyapi.nifi.models`` rather than any maintained nipyapi function, so
they construct and deserialize models directly without touching NiFi.
"""

import pytest

import nipyapi
from nipyapi.nifi import ApiClient
from nipyapi.nifi.models import (
    AffectedComponentEntity,
    ParameterGroupConfigurationEntity,
    ParameterProviderEntity,
)


# Shape of a Parameter Provider entity as returned by a fetch request.
# On the first fetch of a new group NiFi stages each parameter with a null
# sensitivity and a null synchronized flag; later fetches return the
# sensitivity that was applied.
FIRST_FETCH_PROVIDER = {
    "id": "00000000-0000-0000-0000-000000000001",
    "revision": {"version": 1},
    "component": {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Example Parameter Provider",
        "type": "org.example.ExampleParameterProvider",
        "parameterGroupConfigurations": [
            {
                "groupName": "example.secrets",
                "parameterContextName": "example.secrets",
                "parameterSensitivities": {"API_KEY": None},
                "synchronized": None,
            }
        ],
    },
}

LATER_FETCH_PROVIDER = {
    "id": "00000000-0000-0000-0000-000000000001",
    "revision": {"version": 2},
    "component": {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Example Parameter Provider",
        "type": "org.example.ExampleParameterProvider",
        "parameterGroupConfigurations": [
            {
                "groupName": "example.secrets",
                "parameterContextName": "example.secrets",
                "parameterSensitivities": {
                    "API_KEY": "SENSITIVE",
                    "API_HOST": "NON_SENSITIVE",
                },
                "synchronized": True,
            }
        ],
    },
}


def test_parameter_sensitivities_keyed_by_parameter_name():
    # Keys are parameter names; only the values are constrained by the enum
    group = ParameterGroupConfigurationEntity(
        group_name="example.secrets",
        parameter_sensitivities={"API_KEY": "SENSITIVE", "API_HOST": "NON_SENSITIVE"},
    )
    assert group.parameter_sensitivities == {
        "API_KEY": "SENSITIVE",
        "API_HOST": "NON_SENSITIVE",
    }


def test_parameter_sensitivities_allows_unset_value():
    # A first fetch stages parameters with no sensitivity chosen yet
    group = ParameterGroupConfigurationEntity(
        group_name="example.secrets",
        parameter_sensitivities={"API_KEY": None},
    )
    assert group.parameter_sensitivities == {"API_KEY": None}


def test_parameter_sensitivities_rejects_invalid_value():
    with pytest.raises(ValueError):
        ParameterGroupConfigurationEntity(
            group_name="example.secrets",
            parameter_sensitivities={"API_KEY": "SECRET"},
        )


@pytest.mark.parametrize("payload", [FIRST_FETCH_PROVIDER, LATER_FETCH_PROVIDER])
def test_deserialize_parameter_provider_fetch_response(payload):
    entity = ApiClient().deserialize_model(payload, ParameterProviderEntity)
    groups = entity.component.parameter_group_configurations
    assert len(groups) == 1
    assert groups[0].group_name == "example.secrets"
    assert set(groups[0].parameter_sensitivities) >= {"API_KEY"}


def test_affected_component_accepts_stateless_group():
    # NiFi returns STATELESS_GROUP for components in stateless process groups;
    # AffectedComponentDTO allows it but the upstream entity enum omits it
    entity = AffectedComponentEntity(reference_type="STATELESS_GROUP")
    assert entity.reference_type == "STATELESS_GROUP"


def test_client_side_validation_can_be_disabled(monkeypatch):
    monkeypatch.setattr(
        nipyapi.config.nifi_config, "client_side_validation", False
    )
    group = ParameterGroupConfigurationEntity(
        group_name="example.secrets",
        parameter_sensitivities={"API_KEY": "SECRET"},
    )
    assert group.parameter_sensitivities == {"API_KEY": "SECRET"}
    entity = AffectedComponentEntity(reference_type="NOT_A_TYPE")
    assert entity.reference_type == "NOT_A_TYPE"


def test_client_side_validation_enabled_by_default():
    assert getattr(nipyapi.config.nifi_config, "client_side_validation", None) is True
    with pytest.raises(ValueError):
        AffectedComponentEntity(reference_type="NOT_A_TYPE")


@pytest.mark.parametrize("client", [nipyapi.nifi, nipyapi.registry])
def test_enum_validation_scalar_and_container(client, monkeypatch):
    """The shared template guard covers both clients and list enums."""
    configuration = client.Configuration()
    assert configuration.client_side_validation is True
    with pytest.raises(ValueError):
        client.Stateful(scopes=['UNRECOGNIZED'])
    with pytest.raises(ValueError):
        client.DynamicProperty(expression_language_scope='UNRECOGNIZED')
    monkeypatch.setattr(configuration, 'client_side_validation', False)
    assert client.Stateful(scopes=['UNRECOGNIZED']).scopes == ['UNRECOGNIZED']
    assert client.DynamicProperty(expression_language_scope='UNRECOGNIZED').expression_language_scope == 'UNRECOGNIZED'


@pytest.mark.parametrize("client", [nipyapi.nifi, nipyapi.registry])
@pytest.mark.parametrize("status", [200, 500])
def test_rest_preserves_response_diagnostics(client, status, monkeypatch, caplog):
    """Both generated clients preserve response bodies in DEBUG logs and API errors."""
    import logging
    import urllib3
    transport = client.rest.RESTClientObject()
    monkeypatch.setattr(transport.pool_manager, 'request', lambda *args, **kwargs:
                        urllib3.response.HTTPResponse(
                            status=status, reason='test reason', body=b'test response details',
                            headers={'X-Request-Id': 'response-test'}))
    with caplog.at_level(logging.DEBUG):
        if status == 200:
            response = transport.GET('https://localhost.invalid/test')
            assert response.status == 200
            assert response.data == 'test response details'
        else:
            with pytest.raises(client.rest.ApiException) as failed:
                transport.GET('https://localhost.invalid/test')
            assert failed.value.status == status
            assert failed.value.reason == 'test reason'
            assert failed.value.body == 'test response details'
            assert failed.value.headers['X-Request-Id'] == 'response-test'
    assert 'response body: test response details' in caplog.text
