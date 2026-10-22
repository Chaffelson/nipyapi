"""Tests for `nipyapi.parameters` package."""

from tests import conftest
import uuid
import pytest
from nipyapi import parameters
from nipyapi.nifi import ParameterContextEntity
from nipyapi.nifi.rest import ApiException


def test_list_all_parameter_providers(fix_param_provider):
    """Provider listing returns the created entities."""
    provider = fix_param_provider.generate()
    assert provider.id in {item.id for item in parameters.list_all_parameter_providers()}


def test_get_parameter_provider(fix_param_provider):
    """Provider lookup supports id/name/type and None/single/list results."""
    first = fix_param_provider.generate('_first')
    second = fix_param_provider.generate('_second')
    assert parameters.get_parameter_provider(first.id, 'id').id == first.id
    assert parameters.get_parameter_provider(first.component.name, greedy=False).id == first.id
    matches = parameters.get_parameter_provider(conftest.test_basename + '_param_provider')
    assert {item.id for item in matches} == {first.id, second.id}
    typed = parameters.get_parameter_provider('EnvironmentVariableParameterProvider', 'type')
    assert {first.id, second.id}.issubset({item.id for item in typed})
    assert parameters.get_parameter_provider('nipyapi_test_missing_provider') is None
    assert parameters.get_parameter_provider(str(uuid.uuid4()), 'id') is None


def test_list_all_parameter_provider_types():
    """Provider type discovery includes the stock environment provider."""
    types = parameters.list_all_parameter_provider_types()
    assert any(item.type.endswith('.EnvironmentVariableParameterProvider') for item in types)


def test_get_parameter_provider_type():
    """Provider type lookup follows the existing documented-type filter contract."""
    provider_type = parameters.get_parameter_provider_type('EnvironmentVariableParameterProvider')
    assert provider_type.type == 'org.apache.nifi.parameter.EnvironmentVariableParameterProvider'
    assert parameters.get_parameter_provider_type(provider_type.type, greedy=False) == provider_type
    assert parameters.get_parameter_provider_type('nipyapi_test_missing_type') is None
    assert len(parameters.get_parameter_provider_type('ParameterProvider')) > 1


def test_provider_stale_revision(fix_param_provider):
    """refresh exists because NiFi rejects a stale provider revision."""
    provider = fix_param_provider.generate()
    stale = parameters.get_parameter_provider(provider.id, 'id')
    parameters.update_parameter_provider(provider, {'include-environment-variables': 'HOME'})
    for operation in (
        lambda **kwargs: parameters.update_parameter_provider(
            stale, {'include-environment-variables': 'HOME'}, **kwargs),
        lambda **kwargs: parameters.fetch_parameter_provider(stale, **kwargs),
    ):
        with pytest.raises(ApiException) as rejected:
            operation(refresh=False)
        assert rejected.value.status in (400, 409)
        assert 'up-to-date' in rejected.value.body
        assert operation().id == provider.id

def test_update_parameter_provider(fix_param_provider):
    """Provider updates refresh stale revisions and validate property keys."""
    provider = fix_param_provider.generate()
    properties = {'parameter-group-name': conftest.test_parameter_context_name + '_changed'}
    updated = parameters.update_parameter_provider(provider, properties)
    assert updated.component.properties['parameter-group-name'] == properties['parameter-group-name']
    cleared = parameters.update_parameter_provider(provider, {'include-environment-variables': None})
    assert cleared.component.properties['include-environment-variables'] is None
    with pytest.raises(ValueError, match='property'):
        parameters.update_parameter_provider(provider, {'not-a-property': 'unused'})


def test_fetch_parameter_provider(fix_param_provider):
    """Fetch stages only the configured group and refreshes the provider revision."""
    provider = fix_param_provider.generate()
    fetched = parameters.fetch_parameter_provider(provider.id)
    assert fetched.id == provider.id
    group = fetched.component.parameter_group_configurations[0]
    assert group.group_name == provider.component.properties['parameter-group-name']
    assert set(group.parameter_sensitivities) == {'HOME'}
    assert parameters.fetch_parameter_provider(provider).id == provider.id


def test_apply_parameter_provider(fix_param_provider):
    """First apply assigns explicit sensitivities and returns a completed request."""
    provider = fix_param_provider.generate()
    fetched = parameters.fetch_parameter_provider(provider)
    group_name = provider.component.properties['parameter-group-name']
    request = parameters.apply_parameter_provider(provider, [group_name], fetch_result=fetched)
    assert request.complete and not request.failure_reason
    context = parameters.get_parameter_context(group_name, greedy=False)
    home = next(item.parameter for item in context.component.parameters if item.parameter.name == 'HOME')
    assert home.sensitive is True
    assert home.value in (None, '********')
    with pytest.raises(ApiException) as deleted:
        conftest.nipyapi.nifi.ParameterProvidersApi().get_parameter_provider_apply_parameters_request(
            provider.id, request.request_id
        )
    assert deleted.value.status == 404
    with pytest.raises(ValueError, match='missing'):
        parameters.apply_parameter_provider(provider, ['missing'])


def test_fetch_and_apply_parameter_provider(fix_param_provider):
    """Fetch and apply by ID supports repeat refresh and rejects empty requested groups."""
    provider = fix_param_provider.generate()
    request = parameters.fetch_and_apply_parameter_provider(provider.id, identifier_type='id')
    assert request.complete and not request.failure_reason
    repeated = parameters.fetch_and_apply_parameter_provider(provider)
    assert not repeated.referencing_components
    parameters.update_parameter_provider(provider, {'include-environment-variables': 'NIPYAPI_ABSENT_VARIABLE'})
    with pytest.raises(ValueError, match='empty|parameters'):
        parameters.fetch_and_apply_parameter_provider(provider)
    parameters.update_parameter_provider(provider, {'include-environment-variables': 'HOME'})
    # Overrides reach apply, so a mistyped name is rejected before anything is submitted.
    with pytest.raises(ValueError, match='Unknown parameters'):
        parameters.fetch_and_apply_parameter_provider(
            provider, sensitivities={'NIPYAPI_TYPO': 'SENSITIVE'})
    with pytest.raises(TypeError, match='synchronized'):
        parameters.fetch_and_apply_parameter_provider(provider, synchronized='yes')


def test_set_inherited_parameter_contexts(fix_context, fix_inherited_context_hierarchy):
    """Prepend controls actual inherited precedence; replace preserves locals."""
    hierarchy = fix_inherited_context_hierarchy
    first = fix_context.generate(conftest.test_parameter_context_name + '_first')
    parameters.upsert_parameter_to_context(
        first, parameters.prepare_parameter(hierarchy.child_param_name, 'first_value'))
    second = hierarchy.child_ctx
    target = hierarchy.parent_ctx
    request = parameters.set_inherited_parameter_contexts(target, [second], mode='replace')
    assert request.complete and not request.failure_reason
    with pytest.raises(ApiException) as deleted:
        conftest.nipyapi.nifi.ParameterContextsApi().get_parameter_context_update(
            target.id, request.request_id)
    assert deleted.value.status == 404
    parameters.set_inherited_parameter_contexts(target.id, [first, second], mode='prepend')
    repeated = parameters.set_inherited_parameter_contexts(target, [first], mode='prepend')
    live = conftest.nipyapi.nifi.ParameterContextsApi().get_parameter_context(
        target.id, include_inherited_parameters=True)
    assert [item.id for item in live.component.inherited_parameter_contexts] == [first.id, second.id]
    assert not repeated.referencing_components
    assert next(item.parameter.value for item in live.component.parameters
                if item.parameter.name == hierarchy.child_param_name) == 'first_value'
    parameters.set_inherited_parameter_contexts(target, [], mode='replace')
    live = parameters.get_parameter_context(target.id, 'id')
    assert not live.component.inherited_parameter_contexts
    assert [(item.parameter.name, item.parameter.value) for item in live.component.parameters] == [
        (hierarchy.parent_param_name, 'parent_value'),
    ]


def test_inheritance_uses_live_context(fix_inherited_context_hierarchy, fix_context):
    """A stale context entity cannot drop inheritance added after it was read."""
    hierarchy = fix_inherited_context_hierarchy
    target = hierarchy.parent_ctx
    stale = parameters.get_parameter_context(target.id, 'id')
    added = fix_context.generate(conftest.test_parameter_context_name + '_added')
    parameters.set_inherited_parameter_contexts(target, [added])
    later = fix_context.generate(conftest.test_parameter_context_name + '_later')
    parameters.set_inherited_parameter_contexts(stale, [later])
    live = parameters.get_parameter_context(target.id, 'id')
    assert [item.id for item in live.component.inherited_parameter_contexts] == [
        later.id, added.id, hierarchy.child_ctx.id]

def test_connect_uses_live_target(fix_context, fix_pg):
    """Stale context and process-group entities resolve to the current target."""
    source = fix_context.generate(conftest.test_parameter_context_name + '_live_source')
    parameters.upsert_parameter_to_context(source, parameters.prepare_parameter('KEY', 'value', sensitive=True))
    target = fix_context.generate(conftest.test_parameter_context_name + '_live_target')
    stale_target = parameters.get_parameter_context(target.id, 'id')
    group = fix_pg.generate()
    parameters.assign_context_to_process_group(group, target.id)
    other = fix_context.generate(conftest.test_parameter_context_name + '_live_other')
    parameters.set_inherited_parameter_contexts(target, [other])
    parameters.connect_parameter_provider_group(group, source.component.name, {'Alias': 'KEY'})
    parameters.connect_parameter_provider_group(stale_target, source.component.name, {'Alias': 'KEY'})
    live = parameters.get_parameter_context(target.id, 'id')
    assert [item.id for item in live.component.inherited_parameter_contexts] == [source.id, other.id]

def test_get_process_group_parameter_context(fix_pg, fix_context):
    """Bound-context discovery accepts entities and strings; unbound returns None."""
    group = fix_pg.generate()
    assert parameters.get_process_group_parameter_context(group) is None
    context = fix_context.generate()
    parameters.assign_context_to_process_group(group, context.id)
    assert parameters.get_process_group_parameter_context(group).id == context.id
    assert parameters.get_process_group_parameter_context(group.id).id == context.id


def test_connect_parameter_provider_group(fix_context, fix_pg):
    """Connect prepends the supplied context and creates a local sensitive alias."""
    source = fix_context.generate(conftest.test_parameter_context_name + '_source')
    parameters.upsert_parameter_to_context(
        source, parameters.prepare_parameter('API_KEY', 'fixture-secret-value', sensitive=True)
    )
    target = fix_context.generate(conftest.test_parameter_context_name + '_target')
    group = fix_pg.generate()
    parameters.assign_context_to_process_group(group, target.id)
    request = parameters.connect_parameter_provider_group(
        group, source.component.name, {'Local Secret': 'API_KEY'}
    )
    assert request.complete and not request.failure_reason
    live = parameters.get_parameter_context(target.id, 'id')
    assert live.component.inherited_parameter_contexts[0].id == source.id
    alias = next(item.parameter for item in live.component.parameters if item.parameter.name == 'Local Secret')
    assert alias.sensitive is True
    repeated = parameters.connect_parameter_provider_group(
        target.id, source.component.name, {'Local Secret': 'API_KEY'}
    )
    assert not repeated.referencing_components
    # An already-inherited source keeps its position unless a higher context shadows it.
    other = fix_context.generate(conftest.test_parameter_context_name + '_other')
    parameters.set_inherited_parameter_contexts(target, [other, source], mode='replace')
    parameters.connect_parameter_provider_group(target, source.component.name, {'Local Secret': 'API_KEY'})
    live = parameters.get_parameter_context(target.id, 'id')
    assert [item.id for item in live.component.inherited_parameter_contexts] == [other.id, source.id]
    parameters.upsert_parameter_to_context(
        other, parameters.prepare_parameter('API_KEY', 'shadow', sensitive=True))
    with pytest.raises(ValueError, match=r"shadow.*\['API_KEY'\]"):
        parameters.connect_parameter_provider_group(
            target, source.component.name, {'Local Secret': 'API_KEY'})
    with pytest.raises(ValueError, match='MISSING'):
        parameters.connect_parameter_provider_group(target, source.component.name, {'Local Secret': 'MISSING'})


def test_provider_sensitivity_precedence(fix_param_provider):
    """Explicit overrides beat staged choices, which beat the default."""
    provider = fix_param_provider.generate()
    fetched = parameters.fetch_parameter_provider(provider)
    group = fetched.component.parameter_group_configurations[0]
    group.parameter_sensitivities = {'HOME': 'NON_SENSITIVE'}
    parameters.apply_parameter_provider(
        provider, sensitivities={'HOME': 'SENSITIVE'}, fetch_result=fetched,
    )
    context = parameters.get_parameter_context(group.group_name, greedy=False)
    assert next(item.parameter for item in context.component.parameters
                if item.parameter.name == 'HOME').sensitive is True
    # A new default must not override the stored sensitivity on subsequent fetches.
    repeated = parameters.fetch_and_apply_parameter_provider(provider, sensitivity='NON_SENSITIVE')
    assert repeated.complete and not repeated.failure_reason
    context = parameters.get_parameter_context(group.group_name, greedy=False)
    assert next(item.parameter for item in context.component.parameters
                if item.parameter.name == 'HOME').sensitive is True


def test_apply_parameter_provider_request_failure(fix_param_provider, monkeypatch):
    """A completed failed apply raises NiFi's reason and deletes that request.

    NiFi marks a failed request complete with failure_reason; no reliable live
    trigger exists, so the request boundary is simulated. Cleanup policy itself
    is covered by tests/test_utils.py.
    """
    provider = fix_param_provider.generate()
    fetched = parameters.fetch_parameter_provider(provider)
    nifi = conftest.nipyapi.nifi
    deleted = []
    monkeypatch.setattr(nifi.ParameterProvidersApi, 'submit_apply_parameters',
                        lambda *args, **kwargs: nifi.ParameterProviderApplyParametersRequestEntity(
                            request=nifi.ParameterProviderApplyParametersRequestDTO(request_id='test-request')))
    monkeypatch.setattr(nifi.ParameterProvidersApi, 'get_parameter_provider_apply_parameters_request',
                        lambda *args: nifi.ParameterProviderApplyParametersRequestEntity(
                            request=nifi.ParameterProviderApplyParametersRequestDTO(
                                complete=True, failure_reason='provider request failed: source unavailable')))
    monkeypatch.setattr(nifi.ParameterProvidersApi, 'delete_apply_parameters_request',
                        lambda self, provider_id, request_id: deleted.append((provider_id, request_id)))
    with pytest.raises(ValueError, match='^provider request failed: source unavailable$'):
        parameters.apply_parameter_provider(provider, fetch_result=fetched)
    assert deleted == [(provider.id, 'test-request')]


def test_provider_fetch_failure_hint(fix_param_provider, monkeypatch, caplog):
    """Fetch preserves the REST error details and logs the additional scope hint."""
    import logging
    import urllib3
    provider = fix_param_provider.generate()
    original_request = urllib3.PoolManager.request
    def failed_fetch(pool, method, url, **kwargs):
        if method == 'POST' and url.endswith('/fetch-requests'):
            return urllib3.response.HTTPResponse(
                status=500, reason='Internal Server Error',
                body=b'Provider source unavailable', headers={'X-Request-Id': 'fetch-test'},
            )
        return original_request(pool, method, url, **kwargs)
    monkeypatch.setattr(urllib3.PoolManager, 'request', failed_fetch)
    with caplog.at_level(logging.DEBUG), pytest.raises(ApiException) as failed:
        parameters.fetch_parameter_provider(provider)
    assert failed.value.status == 500
    assert failed.value.reason == 'Internal Server Error'
    assert failed.value.body == 'Provider source unavailable'
    assert failed.value.headers['X-Request-Id'] == 'fetch-test'
    assert 'Provider source unavailable' in caplog.text
    assert 'scope' in caplog.text


def test_parameter_helpers_do_not_expose_secrets(fix_param_provider, fix_context, caplog):
    """Sensitive context values stay absent from returned models and DEBUG logs."""
    import logging
    target = fix_context.generate(conftest.test_parameter_context_name + '_secret_target')
    # This synthetic value originates in the provider, not a separate context.
    provider = fix_param_provider.generate(properties={
        'include-environment-variables': 'NIPYAPI_TEST_PROVIDER_SECRET',
    })
    caplog.clear()
    with caplog.at_level(logging.DEBUG):
        fetched = parameters.fetch_parameter_provider(provider)
        applied = parameters.apply_parameter_provider(provider, fetch_result=fetched)
        refreshed = parameters.fetch_and_apply_parameter_provider(provider)
        source = parameters.get_parameter_context(
            provider.component.properties['parameter-group-name'], greedy=False)
        assert {item.parameter.name for item in source.component.parameters} == {'NIPYAPI_TEST_PROVIDER_SECRET'}
        assert all(item.parameter.sensitive is True and item.parameter.value in (None, '********')
                   for item in source.component.parameters)
        inherited = parameters.set_inherited_parameter_contexts(target, [source])
        connected = parameters.connect_parameter_provider_group(
            target, source.component.name, {'Local Secret': 'NIPYAPI_TEST_PROVIDER_SECRET'}
        )
    for result in [fetched, applied, refreshed, source, inherited, connected]:
        assert 'fixture-secret-value' not in repr(result.to_dict())
    assert 'fixture-secret-value' not in caplog.text


@pytest.mark.parametrize('entrypoint', ['update', 'inherit'])
def test_context_request_failure_cleanup(fix_context, monkeypatch, entrypoint):
    """Both context APIs raise a completed request failure and delete the request.

    NiFi marks a failed request complete with failure_reason; no reliable live
    trigger exists, so the request boundary is simulated. Live success and
    deletion are covered by the real update tests.
    """
    context = fix_context.generate()
    nifi = conftest.nipyapi.nifi
    deleted = []

    def invoke():
        if entrypoint == 'update':
            return parameters.update_parameter_context(context)
        return parameters.set_inherited_parameter_contexts(context, [], mode='replace')
    monkeypatch.setattr(nifi.ParameterContextsApi, 'submit_parameter_context_update',
                        lambda *args, **kwargs: nifi.ParameterContextUpdateRequestEntity(
                            request=nifi.ParameterContextUpdateRequestDTO(request_id='context-request')))
    monkeypatch.setattr(nifi.ParameterContextsApi, 'get_parameter_context_update',
                        lambda *args: nifi.ParameterContextUpdateRequestEntity(
                            request=nifi.ParameterContextUpdateRequestDTO(
                                complete=True, failure_reason='context update failed')))
    monkeypatch.setattr(nifi.ParameterContextsApi, 'delete_update_request',
                        lambda self, context_id, request_id: deleted.append((context_id, request_id)))
    with pytest.raises(ValueError, match='^context update failed$'):
        invoke()
    assert deleted == [(context.id, 'context-request')]


@pytest.mark.parametrize('entrypoint', ['update', 'inherit'])
def test_context_inheritance_cycle_conflict(fix_context, entrypoint):
    """NiFi rejects a circular inheritance at submit; the 409 propagates unchanged."""
    first = fix_context.generate(conftest.test_parameter_context_name + '_cycle_a')
    second = fix_context.generate(conftest.test_parameter_context_name + '_cycle_b')
    parameters.set_inherited_parameter_contexts(second, [first])
    try:
        with pytest.raises(ApiException) as failed:
            if entrypoint == 'update':
                first.component.inherited_parameter_contexts = [
                    ParameterContextEntity(id=second.id, component=conftest.nipyapi.nifi
                                           .ParameterContextDTO(id=second.id))]
                parameters.update_parameter_context(first)
            else:
                parameters.set_inherited_parameter_contexts(first, [second])
        assert failed.value.status == 409
        assert 'Circular' in failed.value.body
    finally:
        parameters.set_inherited_parameter_contexts(second, [], mode='replace')


def test_parameter_helper_argument_validation(fix_param_provider, fix_context):
    """Invalid arguments are rejected before anything is submitted."""
    provider = fix_param_provider.generate()
    fetched = parameters.fetch_parameter_provider(provider)
    group = fetched.component.parameter_group_configurations[0].group_name
    with pytest.raises(TypeError, match='properties'):
        parameters.update_parameter_provider(provider, 'HOME')
    with pytest.raises(ValueError, match='sensitivity must'):
        parameters.apply_parameter_provider(provider, sensitivity='SECRET')
    with pytest.raises(TypeError, match='sensitivities must'):
        parameters.apply_parameter_provider(provider, sensitivities='HOME')
    with pytest.raises(ValueError, match='sensitivities must'):
        parameters.apply_parameter_provider(provider, sensitivities={'HOME': 'SECRET'})
    with pytest.raises(TypeError, match='group_names'):
        parameters.apply_parameter_provider(provider, [1], fetch_result=fetched)
    other = fix_param_provider.generate(suffix='_other')
    with pytest.raises(ValueError, match='fetch_result'):
        parameters.apply_parameter_provider(other, fetch_result=fetched)
    # A single group name is accepted as well as a list.
    assert parameters.apply_parameter_provider(provider, group, fetch_result=fetched).complete
    context = fix_context.generate()
    parameters.upsert_parameter_to_context(context, parameters.prepare_parameter('KEY', 'v', sensitive=True))
    with pytest.raises(ValueError, match='mode'):
        parameters.set_inherited_parameter_contexts(context, [], mode='append')
    with pytest.raises(TypeError, match='inherited'):
        parameters.set_inherited_parameter_contexts(context, context.id)
    with pytest.raises(ValueError, match='inherit itself'):
        parameters.set_inherited_parameter_contexts(context, [context])
    target = fix_context.generate(conftest.test_parameter_context_name + '_alias_target')
    with pytest.raises(ValueError, match='reference itself'):
        parameters.connect_parameter_provider_group(target, context.component.name, {'KEY': 'KEY'})


def test_inherited_references_unreadable():
    """An inherited context the user cannot read has no component; keep it by id."""
    hidden = conftest.nipyapi.nifi.ParameterContextReferenceEntity(id='hidden', component=None)
    context = ParameterContextEntity(
        id='target',
        component=conftest.nipyapi.nifi.ParameterContextDTO(
            id='target', inherited_parameter_contexts=[hidden]),
    )
    references = parameters._inherited_context_references(context, [], 'prepend', False, 'id')
    assert [(item.id, item.component.id) for item in references] == [('hidden', 'hidden')]


def test_connect_parameter_provider_group_target_guards(fix_context, fix_pg):
    """An unbound group and colliding context/group names must never pick a target."""
    group = fix_pg.generate()
    source = fix_context.generate(group.component.name)
    with pytest.raises(ValueError, match='bound'):
        parameters.connect_parameter_provider_group(group, source.component.name, {})
    with pytest.raises(ValueError, match='exactly one'):
        parameters.connect_parameter_provider_group(group.component.name, source.component.name, {})
    with pytest.raises(TypeError, match='mappings'):
        parameters.connect_parameter_provider_group(group, source.component.name, ['API_KEY'])


def test_connect_parameter_provider_group_overwrites_local(fix_context, monkeypatch):
    """Connecting replaces an existing sensitive literal and preserves other locals."""
    source = fix_context.generate(conftest.test_parameter_context_name + '_source')
    parameters.upsert_parameter_to_context(source, parameters.prepare_parameter('API_KEY', 'secret', sensitive=True))
    target = fix_context.generate(conftest.test_parameter_context_name + '_target')
    parameters.upsert_parameter_to_context(source, parameters.prepare_parameter('PLAIN', 'visible'))
    parameters.upsert_parameter_to_context(
        target, parameters.prepare_parameter('Alias', 'old', description='kept', sensitive=True))
    parameters.upsert_parameter_to_context(target, parameters.prepare_parameter('Untouched', 'keep'))
    # NiFi leaves a sensitive alias to a non-sensitive parameter unresolved.
    with pytest.raises(ValueError, match=r"not sensitive: \['PLAIN'\]"):
        parameters.connect_parameter_provider_group(target, source.component.name, {'New': 'PLAIN'})
    submitted = []
    api = conftest.nipyapi.nifi.ParameterContextsApi
    original_submit = api.submit_parameter_context_update
    def capture_submit(handle, context_id, body, **kwargs):
        submitted.append(body)
        return original_submit(handle, context_id=context_id, body=body, **kwargs)
    monkeypatch.setattr(api, 'submit_parameter_context_update', capture_submit)
    result = parameters.connect_parameter_provider_group(target, source.component.name, {'Alias': 'API_KEY'})
    assert result.complete and not result.failure_reason
    # The exact alias and inheritance travel in the same atomic request.
    assert len(submitted) == 1
    component = submitted[0].component
    assert [(item.parameter.name, item.parameter.value, item.parameter.sensitive)
            for item in component.parameters] == [('Alias', '#{API_KEY}', True)]
    assert [item.id for item in component.inherited_parameter_contexts] == [source.id]
    live = parameters.get_parameter_context(target.id, 'id')
    assert next(item.parameter.value for item in live.component.parameters
                if item.parameter.name == 'Untouched') == 'keep'
    assert next(item.parameter.description for item in live.component.parameters
                if item.parameter.name == 'Alias') == 'kept'
    with pytest.raises(ValueError, match='non-sensitive'):
        parameters.connect_parameter_provider_group(target, source.component.name, {'Untouched': 'API_KEY'})
    # Confirm the server restriction behind the helper's preflight rejection.
    live = parameters.get_parameter_context(target.id, 'id')
    with pytest.raises(ApiException) as conversion:
        original_submit(
            api(), context_id=live.id,
            body=ParameterContextEntity(
                id=live.id, revision=live.revision,
                component=conftest.nipyapi.nifi.ParameterContextDTO(
                    id=live.id, name=live.component.name,
                    parameters=[parameters.prepare_parameter('Untouched', '#{API_KEY}', sensitive=True)],
                ),
            ),
        )
    assert conversion.value.status in (400, 409)
    assert 'sensitive' in conversion.value.body.lower()


def test_apply_parameter_provider_group_selection(fix_param_provider, monkeypatch):
    """Select requested groups; keep staged choices unless explicitly overridden.

    The environment-variable provider yields one group, so the multi-group staging
    is simulated; the single-group live path is covered by the apply tests.
    """
    nifi = conftest.nipyapi.nifi
    provider = fix_param_provider.generate()
    fetched = parameters.fetch_parameter_provider(provider)
    fetched.component.parameter_group_configurations = [
        nifi.ParameterGroupConfigurationEntity(
            group_name='selected',
            parameter_sensitivities={'unset': None, 'staged': 'NON_SENSITIVE', 'override': 'NON_SENSITIVE'},
        ),
        nifi.ParameterGroupConfigurationEntity(
            group_name='kept', parameter_sensitivities={'p': 'SENSITIVE'}, synchronized=False),
        nifi.ParameterGroupConfigurationEntity(group_name='unrelated', parameter_sensitivities={'other': None}),
    ]
    submitted = []
    def submit(handle, provider_id, body):
        submitted.append(body)
        return nifi.ParameterProviderApplyParametersRequestEntity(
            request=nifi.ParameterProviderApplyParametersRequestDTO(request_id='selected-request'))
    monkeypatch.setattr(nifi.ParameterProvidersApi, 'submit_apply_parameters', submit)
    monkeypatch.setattr(nifi.ParameterProvidersApi, 'get_parameter_provider_apply_parameters_request',
                        lambda *args: nifi.ParameterProviderApplyParametersRequestEntity(
                            request=nifi.ParameterProviderApplyParametersRequestDTO(complete=True)))
    monkeypatch.setattr(nifi.ParameterProvidersApi, 'delete_apply_parameters_request', lambda *args: None)
    result = parameters.apply_parameter_provider(
        provider, ['selected', 'kept'], sensitivities={'override': 'SENSITIVE'}, fetch_result=fetched,
    )
    assert result.complete
    assert len(submitted) == 1
    groups = submitted[0].parameter_group_configurations
    assert [group.group_name for group in groups] == ['selected', 'kept']
    assert groups[0].group_name == groups[0].parameter_context_name == 'selected'
    assert groups[0].parameter_sensitivities == {
        'unset': 'SENSITIVE', 'staged': 'NON_SENSITIVE', 'override': 'SENSITIVE',
    }
    # NiFi skips unsynchronized groups on apply: unset defaults to True, staged False is kept.
    assert [group.synchronized for group in groups] == [True, False]
    assert fetched.component.parameter_group_configurations[0].parameter_sensitivities['unset'] is None
    parameters.apply_parameter_provider(
        provider, ['selected', 'kept'], synchronized=True, fetch_result=fetched)
    assert [group.synchronized for group in submitted[1].parameter_group_configurations] == [True, True]
    with pytest.raises(TypeError, match='synchronized'):
        parameters.apply_parameter_provider(provider, synchronized='yes', fetch_result=fetched)
    # Override keys are parameter names; one matching no selected parameter must not be ignored.
    with pytest.raises(ValueError, match=r"Unknown parameters.*\['other'\]"):
        parameters.apply_parameter_provider(
            provider, ['selected'], sensitivities={'other': 'SENSITIVE'}, fetch_result=fetched)
    assert len(submitted) == 2


def test_apply_parameter_provider_nothing_to_apply(fix_param_provider, caplog):
    """NiFi completes an apply of only unsynchronized groups without changing anything."""
    provider = fix_param_provider.generate()
    fetched = parameters.fetch_parameter_provider(provider)
    group = fetched.component.parameter_group_configurations[0].group_name
    with caplog.at_level('WARNING', logger='nipyapi.parameters'):
        result = parameters.apply_parameter_provider(
            provider, [group], synchronized=False, fetch_result=fetched)
    assert result.complete and not result.failure_reason
    assert 'nothing to apply' in caplog.text
    assert parameters.get_parameter_context(group, greedy=False) is None
    caplog.clear()
    with caplog.at_level('WARNING', logger='nipyapi.parameters'):
        parameters.apply_parameter_provider(provider, [group], fetch_result=fetched)
    assert 'nothing to apply' not in caplog.text
    assert parameters.get_parameter_context(group, greedy=False) is not None


def test_create_parameter_context(fix_context):
    c1 = fix_context.generate(name=conftest.test_parameter_context_name)
    assert isinstance(c1, ParameterContextEntity)
    with pytest.raises(AssertionError):
        _ = parameters.create_parameter_context(name={})
    with pytest.raises(AssertionError):
        _ = parameters.create_parameter_context(name=conftest.test_basename, description={})
    with pytest.raises(ApiException):
        # Attempt to generate duplicate Parameter Context
        _ = fix_context.generate(name=conftest.test_parameter_context_name)


def test_get_parameter_context(fix_context):
    # Regression tests are parametrized, skip inside function to work properly
    r1 = parameters.get_parameter_context('fake news', 'name')
    assert r1 is None
    c2 = parameters.get_parameter_context(
        identifier=str(uuid.uuid4()), identifier_type='id'
    )
    assert c2 is None
    c1 = fix_context.generate(name=conftest.test_basename + 'instance_1')
    r3 = parameters.get_parameter_context(c1.id, identifier_type='id')
    assert r3.component.name == conftest.test_basename + 'instance_1'
    c2 = fix_context.generate(name=conftest.test_basename + 'instance_2')
    r4 = parameters.get_parameter_context(
        conftest.test_basename + 'instance_2', identifier_type='name'
    )
    assert r4.id == c2.id


def test_list_all_parameter_contexts(fix_context):
    _ = fix_context.generate()
    r1 = parameters.list_all_parameter_contexts()
    assert isinstance(r1, list)
    for pc in r1:
        assert isinstance(pc, ParameterContextEntity)
    _ = fix_context.generate(name=conftest.test_basename + 'instance_1')
    r2 = [
        x for x in parameters.list_all_parameter_contexts()
        if conftest.test_basename in x.component.name
    ]
    assert isinstance(r2, list)
    assert len(r2) == 2
    for pc in r2:
        assert isinstance(pc, ParameterContextEntity)


def test_list_orphaned_contexts(fix_context):
    """Test listing parameter contexts not bound to any process groups."""
    # Create an unbound context (orphan)
    orphan = fix_context.generate(name=conftest.test_basename + '_orphan')
    assert orphan is not None

    # List orphaned contexts
    orphans = parameters.list_orphaned_contexts()
    assert isinstance(orphans, list)

    # Our newly created context should be in the orphaned list
    orphan_ids = [ctx.id for ctx in orphans]
    assert orphan.id in orphan_ids

    # All returned contexts should have no bound process groups
    for ctx in orphans:
        assert not ctx.component.bound_process_groups


def test_delete_parameter_context(fix_context):
    c1 = fix_context.generate()
    assert c1.revision is not None
    r1 = parameters.delete_parameter_context(c1)
    assert isinstance(r1, ParameterContextEntity)
    assert r1.revision is None
    with pytest.raises(ApiException):
        _ = parameters.delete_parameter_context(c1)

    # Test deletion by ID string
    c2 = fix_context.generate(name=conftest.test_parameter_context_name + '_id_delete')
    r2 = parameters.delete_parameter_context(c2.id)
    assert r2.id == c2.id

    # Test deletion by name string
    c3 = fix_context.generate(name=conftest.test_parameter_context_name + '_name_delete')
    r3 = parameters.delete_parameter_context(
        c3.component.name, identifier_type="name", greedy=False
    )
    assert r3.id == c3.id


def test_update_parameter_context(fix_context, monkeypatch):
    api = conftest.nipyapi.nifi.ParameterContextsApi
    original_delete = api.delete_update_request
    deleted = []

    def record_delete(handle, context_id, request_id, **kwargs):
        deleted.append((context_id, request_id))
        return original_delete(handle, context_id=context_id, request_id=request_id, **kwargs)

    # Pass-through spy: the real NiFi DELETE runs; only its IDs are recorded.
    monkeypatch.setattr(api, 'delete_update_request', record_delete)
    c1 = fix_context.generate()
    c1.component.parameters.append(
        parameters.prepare_parameter('Black', 'Lives', 'Matter', True)
    )
    r1 = parameters.update_parameter_context(
        c1
    )
    assert isinstance(r1, ParameterContextEntity)
    assert 1 == len([x for x in r1.component.parameters if 'Black' in x.parameter.name])
    assert len(deleted) == 1
    with pytest.raises(ApiException) as gone:
        api().get_parameter_context_update(*deleted[0])
    assert gone.value.status == 404
    r1.component.parameters = [
        parameters.prepare_parameter('Black', 'Votes', 'Matter', True)
    ]
    r2 = parameters.update_parameter_context(
        r1
    )
    assert isinstance(r2, ParameterContextEntity)
    assert r2.component.parameters[0].parameter.description == 'Matter'


def test_rename_parameter_context(fix_context):
    """Test renaming a parameter context without affecting parameters."""
    # Create context with a parameter
    c1 = fix_context.generate()
    c1.component.parameters.append(
        parameters.prepare_parameter('test_param', 'test_value')
    )
    c1 = parameters.update_parameter_context(c1)
    original_name = c1.component.name
    new_name = original_name + '_renamed'

    # Rename the context
    r1 = parameters.rename_parameter_context(c1, new_name)
    assert isinstance(r1, ParameterContextEntity)
    assert r1.component.name == new_name

    # Verify parameters are preserved
    assert len(r1.component.parameters) == 1
    assert r1.component.parameters[0].parameter.name == 'test_param'
    assert r1.component.parameters[0].parameter.value == 'test_value'


def test_delete_parameter_from_context(fix_context):
    c1 = fix_context.generate()
    c1.component.parameters.append(
        parameters.prepare_parameter('Black', 'Lives', 'Matter', True)
    )
    _ = parameters.update_parameter_context(
        c1
    )
    r1 = parameters.delete_parameter_from_context(c1, 'Black')
    assert r1.component.parameters == []


def test_upsert_parameter_to_context(fix_context):
    c1 = fix_context.generate()
    r1 = parameters.upsert_parameter_to_context(
        c1,
        parameters.prepare_parameter('Black', 'Lives', 'Matter', True)
    )
    assert r1.component.parameters[0].parameter.description == 'Matter'


def test_assign_context_to_process_group(fix_pg, fix_context):
    c1 = fix_context.generate()
    pg1 = fix_pg.generate()
    r1 = parameters.assign_context_to_process_group(pg1, c1.id)
    assert r1.component.parameter_context.id == c1.id

    # Test with pg as ID string
    c2 = fix_context.generate(name=conftest.test_parameter_context_name + '_assign_id')
    pg2 = fix_pg.generate(suffix='_assign_id')
    r2 = parameters.assign_context_to_process_group(pg2.id, c2.id)
    assert r2.component.parameter_context.id == c2.id


def test_remove_context_from_process_group(fix_pg, fix_context):
    c1 = fix_context.generate()
    pg1 = fix_pg.generate()
    r1 = parameters.assign_context_to_process_group(pg1, c1.id)
    assert r1.component.parameter_context.id == c1.id
    r2 = parameters.remove_context_from_process_group(pg1)
    assert r2.component.parameter_context is None


# =============================================================================
# Asset Management Tests
# =============================================================================


def test_upload_asset_from_bytes(fix_context):
    """Test uploading an asset from bytes - validates octet-stream handling."""

    c1 = fix_context.generate()

    # Create test file content (simple text, but sent as binary)
    test_content = b"This is test content for asset upload validation."
    test_filename = "test_asset.txt"

    # Upload the asset using file_bytes
    result = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=test_content,
        filename=test_filename
    )

    # Verify the result structure
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result
    assert "digest" in result
    assert result["name"] == test_filename
    # Digest should be a SHA-256 hash (64 hex chars)
    assert len(result["digest"]) == 64

    # Clean up - delete the asset
    parameters.delete_asset(context_id=c1.id, asset_id=result["id"])


def test_list_assets(fix_context):
    """Test listing assets in a parameter context."""

    c1 = fix_context.generate()

    # Initially should be empty
    assets = parameters.list_assets(c1.id)
    assert isinstance(assets, list)
    initial_count = len(assets)

    # Upload two assets
    asset1 = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"asset one content",
        filename="asset1.txt"
    )
    asset2 = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"asset two content",
        filename="asset2.txt"
    )

    # List should now have 2 more assets
    assets = parameters.list_assets(c1.id)
    assert len(assets) == initial_count + 2

    # Verify asset structure
    asset_names = [a["name"] for a in assets]
    assert "asset1.txt" in asset_names
    assert "asset2.txt" in asset_names

    for asset in assets:
        assert "id" in asset
        assert "name" in asset
        assert "digest" in asset
        assert "missing_content" in asset

    # Clean up
    parameters.delete_asset(context_id=c1.id, asset_id=asset1["id"])
    parameters.delete_asset(context_id=c1.id, asset_id=asset2["id"])


def test_delete_asset(fix_context):
    """Test deleting an asset from a parameter context."""

    c1 = fix_context.generate()

    # Upload an asset
    asset = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"content to delete",
        filename="to_delete.txt"
    )

    # Verify it exists
    assets_before = parameters.list_assets(c1.id)
    asset_ids_before = [a["id"] for a in assets_before]
    assert asset["id"] in asset_ids_before

    # Delete it
    result = parameters.delete_asset(context_id=c1.id, asset_id=asset["id"])
    assert isinstance(result, dict)
    assert result["id"] == asset["id"]
    assert result["name"] == "to_delete.txt"

    # Verify it's gone
    assets_after = parameters.list_assets(c1.id)
    asset_ids_after = [a["id"] for a in assets_after]
    assert asset["id"] not in asset_ids_after


def test_prepare_parameter_with_asset(fix_context):
    """Test preparing a parameter that references an asset."""

    c1 = fix_context.generate()

    # Upload an asset first
    asset = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"JDBC driver content simulation",
        filename="postgresql-42.7.6.jar"
    )

    # Prepare a parameter referencing the asset
    param = parameters.prepare_parameter_with_asset(
        name="PostgreSQL Driver",
        asset_id=asset["id"],
        asset_name=asset["name"],
        description="JDBC driver for PostgreSQL database connections"
    )

    # Verify the parameter structure
    assert param.parameter.name == "PostgreSQL Driver"
    assert param.parameter.description == "JDBC driver for PostgreSQL database connections"
    assert len(param.parameter.referenced_assets) == 1
    assert param.parameter.referenced_assets[0].id == asset["id"]
    assert param.parameter.referenced_assets[0].name == asset["name"]

    # Clean up
    parameters.delete_asset(context_id=c1.id, asset_id=asset["id"])


def test_prepare_parameter_with_multiple_assets(fix_context):
    """Test preparing a parameter that references multiple assets."""

    c1 = fix_context.generate()

    # Upload multiple assets
    asset1 = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"ActiveMQ client JAR",
        filename="activemq-client-5.18.0.jar"
    )
    asset2 = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"ActiveMQ broker JAR",
        filename="activemq-broker-5.18.0.jar"
    )

    # Prepare a parameter referencing multiple assets
    param = parameters.prepare_parameter_with_asset(
        name="JMS Client Libraries",
        assets=[asset1, asset2],
        description="ActiveMQ client JARs"
    )

    # Verify the parameter structure
    assert param.parameter.name == "JMS Client Libraries"
    assert param.parameter.description == "ActiveMQ client JARs"
    assert len(param.parameter.referenced_assets) == 2
    asset_ids = {a.id for a in param.parameter.referenced_assets}
    assert asset1["id"] in asset_ids
    assert asset2["id"] in asset_ids

    # Clean up
    parameters.delete_asset(context_id=c1.id, asset_id=asset1["id"])
    parameters.delete_asset(context_id=c1.id, asset_id=asset2["id"])


def test_prepare_parameter_with_asset_validation():
    """Test validation errors for prepare_parameter_with_asset."""

    # Cannot specify both single and multiple assets
    with pytest.raises(ValueError) as exc_info:
        parameters.prepare_parameter_with_asset(
            name="Test",
            asset_id="123",
            asset_name="test.jar",
            assets=[{"id": "456", "name": "other.jar"}]
        )
    assert "Cannot specify both" in str(exc_info.value)

    # Must specify at least one
    with pytest.raises(ValueError) as exc_info:
        parameters.prepare_parameter_with_asset(name="Test")
    assert "Must specify either" in str(exc_info.value)

    # Single asset requires both id and name
    with pytest.raises(ValueError) as exc_info:
        parameters.prepare_parameter_with_asset(name="Test", asset_id="123")
    assert "Both asset_id and asset_name are required" in str(exc_info.value)

    # Assets list must have valid dicts
    with pytest.raises(ValueError) as exc_info:
        parameters.prepare_parameter_with_asset(
            name="Test",
            assets=[{"id": "123"}]  # Missing 'name'
        )
    assert "must be a dict with 'id' and 'name' keys" in str(exc_info.value)

    # Assets cannot be empty list
    with pytest.raises(ValueError) as exc_info:
        parameters.prepare_parameter_with_asset(name="Test", assets=[])
    assert "non-empty list" in str(exc_info.value)


def test_upload_asset_and_link_to_parameter(fix_context):
    """Test full workflow: upload asset and link it to a parameter."""

    c1 = fix_context.generate()

    # Upload an asset
    asset = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"Driver binary content here",
        filename="mysql-connector-j-8.3.0.jar"
    )

    # Prepare parameter referencing the asset
    param = parameters.prepare_parameter_with_asset(
        name="MySQL Driver",
        asset_id=asset["id"],
        asset_name=asset["name"]
    )

    # Add parameter to context
    updated_context = parameters.upsert_parameter_to_context(c1, param)

    # Verify the parameter was added with asset reference
    param_names = [p.parameter.name for p in updated_context.component.parameters]
    assert "MySQL Driver" in param_names

    # Find the parameter and verify asset reference
    mysql_param = next(
        p for p in updated_context.component.parameters
        if p.parameter.name == "MySQL Driver"
    )
    assert mysql_param.parameter.referenced_assets is not None
    assert len(mysql_param.parameter.referenced_assets) == 1
    assert mysql_param.parameter.referenced_assets[0].id == asset["id"]

    # Clean up - delete parameter first, then asset
    parameters.delete_parameter_from_context(updated_context, "MySQL Driver")
    parameters.delete_asset(context_id=c1.id, asset_id=asset["id"])


def test_upload_asset_validation_errors():
    """Test that upload_asset raises appropriate validation errors."""
    # No file_path or file_bytes
    with pytest.raises(ValueError, match="Either file_path or file_bytes"):
        parameters.upload_asset(context_id="fake-id")

    # file_bytes without filename
    with pytest.raises(ValueError, match="filename is required"):
        parameters.upload_asset(context_id="fake-id", file_bytes=b"content")


# =============================================================================
# Parameter Context Hierarchy Tests
# =============================================================================


def test_get_parameter_context_hierarchy_simple(fix_context):
    """Test get_parameter_context_hierarchy with a single context."""

    ctx = fix_context.generate()

    # Add a parameter
    param = parameters.prepare_parameter(
        name="HierarchyTestParam",
        value="test_value",
        description="Test for hierarchy"
    )
    parameters.upsert_parameter_to_context(ctx, param)

    # Get hierarchy
    hierarchy = parameters.get_parameter_context_hierarchy(ctx.id)

    assert hierarchy["id"] == ctx.id
    assert hierarchy["name"] == ctx.component.name
    assert isinstance(hierarchy["parameters"], list)
    assert isinstance(hierarchy["inherited"], list)
    assert len(hierarchy["inherited"]) == 0  # No inherited contexts

    # Verify parameter is in the list
    param_names = [p["name"] for p in hierarchy["parameters"]]
    assert "HierarchyTestParam" in param_names

    # Verify parameter fields including description
    test_param = next(p for p in hierarchy["parameters"] if p["name"] == "HierarchyTestParam")
    assert test_param["value"] == "test_value"
    assert test_param["description"] == "Test for hierarchy"
    assert test_param["sensitive"] is False
    assert "has_asset" in test_param
    assert "asset_name" in test_param


def test_get_parameter_context_hierarchy_with_inheritance(fix_context):
    """Test get_parameter_context_hierarchy with inherited contexts."""

    # Create child context (will be inherited)
    child_ctx = fix_context.generate(name=conftest.test_parameter_context_name + "_child")
    child_param = parameters.prepare_parameter(
        name="ChildParam",
        value="child_value"
    )
    parameters.upsert_parameter_to_context(child_ctx, child_param)

    # Create parent context that inherits from child
    parent_ctx = parameters.create_parameter_context(
        name=conftest.test_parameter_context_name + "_parent",
        inherited_contexts=[child_ctx]
    )
    parent_param = parameters.prepare_parameter(
        name="ParentParam",
        value="parent_value"
    )
    parameters.upsert_parameter_to_context(parent_ctx, parent_param)

    try:
        # Get hierarchy from parent
        hierarchy = parameters.get_parameter_context_hierarchy(parent_ctx.id)

        assert hierarchy["id"] == parent_ctx.id
        assert hierarchy["name"] == parent_ctx.component.name
        assert len(hierarchy["inherited"]) == 1

        # Verify parent parameter
        parent_param_names = [p["name"] for p in hierarchy["parameters"]]
        assert "ParentParam" in parent_param_names

        # Verify child context in hierarchy
        child_hierarchy = hierarchy["inherited"][0]
        assert child_hierarchy["id"] == child_ctx.id
        child_param_names = [p["name"] for p in child_hierarchy["parameters"]]
        assert "ChildParam" in child_param_names

    finally:
        # Clean up parent context
        parameters.delete_parameter_context(parent_ctx)


def test_get_parameter_context_hierarchy_not_found():
    """Test get_parameter_context_hierarchy with invalid context."""

    import uuid
    with pytest.raises(ValueError, match="Parameter context not found"):
        parameters.get_parameter_context_hierarchy(str(uuid.uuid4()))


def test_get_parameter_context_hierarchy_include_bindings(fix_context, fix_pg):
    """Test get_parameter_context_hierarchy with include_bindings=True."""

    ctx = fix_context.generate()

    # Add a parameter
    param = parameters.prepare_parameter(
        name="BindingTestParam",
        value="test_value"
    )
    parameters.upsert_parameter_to_context(ctx, param)

    # Create a PG and bind the context to it
    pg = fix_pg.generate()
    parameters.assign_context_to_process_group(pg, ctx.id)

    # Get hierarchy with bindings
    hierarchy = parameters.get_parameter_context_hierarchy(
        ctx.id, include_bindings=True
    )

    assert hierarchy["id"] == ctx.id
    assert "bound_process_groups" in hierarchy
    assert isinstance(hierarchy["bound_process_groups"], list)
    assert len(hierarchy["bound_process_groups"]) == 1
    assert hierarchy["bound_process_groups"][0]["id"] == pg.id
    assert hierarchy["bound_process_groups"][0]["name"] == pg.component.name

    # Parameters should still be included by default
    assert "parameters" in hierarchy
    assert len(hierarchy["parameters"]) >= 1


def test_get_parameter_context_hierarchy_exclude_parameters(fix_context):
    """Test get_parameter_context_hierarchy with include_parameters=False."""

    ctx = fix_context.generate()

    # Add a parameter
    param = parameters.prepare_parameter(
        name="ExcludeTestParam",
        value="test_value"
    )
    parameters.upsert_parameter_to_context(ctx, param)

    # Get hierarchy without parameters
    hierarchy = parameters.get_parameter_context_hierarchy(
        ctx.id, include_parameters=False
    )

    assert hierarchy["id"] == ctx.id
    assert hierarchy["name"] == ctx.component.name
    assert "parameters" not in hierarchy
    assert "inherited" in hierarchy

    # Bindings should not be included by default
    assert "bound_process_groups" not in hierarchy


def test_get_parameter_context_hierarchy_bindings_only(fix_context, fix_pg):
    """Test get_parameter_context_hierarchy with bindings only (no parameters)."""

    # Create child context
    child_ctx = fix_context.generate(name=conftest.test_parameter_context_name + "_bind_child")
    child_param = parameters.prepare_parameter(name="ChildBindParam", value="child")
    parameters.upsert_parameter_to_context(child_ctx, child_param)

    # Create parent context that inherits from child
    parent_ctx = parameters.create_parameter_context(
        name=conftest.test_parameter_context_name + "_bind_parent",
        inherited_contexts=[child_ctx]
    )

    # Bind parent to a PG
    pg = fix_pg.generate()
    parameters.assign_context_to_process_group(pg, parent_ctx.id)

    try:
        # Get structure with bindings, no parameters
        hierarchy = parameters.get_parameter_context_hierarchy(
            parent_ctx.id,
            include_bindings=True,
            include_parameters=False
        )

        # Verify parent structure
        assert hierarchy["id"] == parent_ctx.id
        assert "parameters" not in hierarchy
        assert "bound_process_groups" in hierarchy
        assert len(hierarchy["bound_process_groups"]) == 1

        # Verify child inherits the flags
        assert len(hierarchy["inherited"]) == 1
        child_hierarchy = hierarchy["inherited"][0]
        assert child_hierarchy["id"] == child_ctx.id
        assert "parameters" not in child_hierarchy
        assert "bound_process_groups" in child_hierarchy
        # NiFi reports transitive bindings - inherited contexts show the PG that
        # binds their parent. This is correct behavior (shows all contexts in use).
        assert len(child_hierarchy["bound_process_groups"]) == 1
        assert child_hierarchy["bound_process_groups"][0]["id"] == pg.id

    finally:
        # Clean up parent context
        parameters.delete_parameter_context(parent_ctx)


def test_get_parameter_context_hierarchy_defaults_backwards_compatible(fix_context):
    """Test that default behavior is backwards compatible."""

    ctx = fix_context.generate()

    param = parameters.prepare_parameter(name="BackwardsParam", value="test")
    parameters.upsert_parameter_to_context(ctx, param)

    # Call with no extra arguments (original signature)
    hierarchy = parameters.get_parameter_context_hierarchy(ctx.id)

    # Should have parameters (default: True)
    assert "parameters" in hierarchy
    assert len(hierarchy["parameters"]) >= 1

    # Should NOT have bound_process_groups (default: False)
    assert "bound_process_groups" not in hierarchy

    # Basic structure preserved
    assert "id" in hierarchy
    assert "name" in hierarchy
    assert "inherited" in hierarchy


def test_get_parameter_ownership_map(fix_context):
    """Test get_parameter_ownership_map with simple context."""

    ctx = fix_context.generate()

    # Add parameters
    param1 = parameters.prepare_parameter(name="OwnerParam1", value="value1")
    param2 = parameters.prepare_parameter(
        name="OwnerParam2", value="value2", sensitive=True
    )
    parameters.upsert_parameter_to_context(ctx, param1)

    # Refresh context before adding second param
    ctx = parameters.get_parameter_context(ctx.id, "id")
    parameters.upsert_parameter_to_context(ctx, param2)

    # Get ownership map
    ownership = parameters.get_parameter_ownership_map(ctx.id)

    assert "OwnerParam1" in ownership
    assert "OwnerParam2" in ownership

    # Verify structure
    owner1 = ownership["OwnerParam1"]
    assert owner1["context_id"] == ctx.id
    assert owner1["context_name"] == ctx.component.name
    assert owner1["sensitive"] is False
    assert owner1["current_value"] == "value1"

    owner2 = ownership["OwnerParam2"]
    assert owner2["sensitive"] is True
    assert owner2["current_value"] is None  # Sensitive values not returned


def test_get_parameter_ownership_map_with_inheritance(fix_context):
    """Test get_parameter_ownership_map tracks correct owning context."""

    # Create child context with a parameter
    child_ctx = fix_context.generate(name=conftest.test_parameter_context_name + "_owner_child")
    child_param = parameters.prepare_parameter(name="ChildOwned", value="child_owns_this")
    parameters.upsert_parameter_to_context(child_ctx, child_param)

    # Create parent that inherits child
    parent_ctx = parameters.create_parameter_context(
        name=conftest.test_parameter_context_name + "_owner_parent",
        inherited_contexts=[child_ctx]
    )
    parent_param = parameters.prepare_parameter(name="ParentOwned", value="parent_owns_this")
    parameters.upsert_parameter_to_context(parent_ctx, parent_param)

    try:
        # Get ownership from parent's perspective
        ownership = parameters.get_parameter_ownership_map(parent_ctx.id)

        # Both parameters should be in map
        assert "ParentOwned" in ownership
        assert "ChildOwned" in ownership

        # Verify ownership attribution
        assert ownership["ParentOwned"]["context_id"] == parent_ctx.id
        assert ownership["ParentOwned"]["context_name"] == parent_ctx.component.name

        assert ownership["ChildOwned"]["context_id"] == child_ctx.id
        assert ownership["ChildOwned"]["context_name"] == child_ctx.component.name

    finally:
        parameters.delete_parameter_context(parent_ctx)


def test_update_parameter_in_context(fix_context):
    """Test update_parameter_in_context updates existing parameter."""

    ctx = fix_context.generate()

    # Create initial parameter
    param = parameters.prepare_parameter(name="UpdateMe", value="initial")
    parameters.upsert_parameter_to_context(ctx, param)

    # Update it
    result = parameters.update_parameter_in_context(
        context_id=ctx.id,
        param_name="UpdateMe",
        value="updated"
    )

    # Verify update
    updated_param = next(
        p for p in result.component.parameters
        if p.parameter.name == "UpdateMe"
    )
    assert updated_param.parameter.value == "updated"


def test_update_parameter_in_context_not_found(fix_context):
    """Test update_parameter_in_context raises error for missing parameter."""

    ctx = fix_context.generate()

    with pytest.raises(ValueError, match="not found in context"):
        parameters.update_parameter_in_context(
            context_id=ctx.id,
            param_name="NonExistent",
            value="value"
        )


def test_update_parameter_in_context_create_if_missing(fix_context):
    """Test update_parameter_in_context with create_if_missing=True."""

    ctx = fix_context.generate()

    # Create a new parameter with create_if_missing
    result = parameters.update_parameter_in_context(
        context_id=ctx.id,
        param_name="CreatedParam",
        value="created_value",
        create_if_missing=True
    )

    # Verify it was created
    param_names = [p.parameter.name for p in result.component.parameters]
    assert "CreatedParam" in param_names

    created_param = next(
        p for p in result.component.parameters
        if p.parameter.name == "CreatedParam"
    )
    assert created_param.parameter.value == "created_value"


def test_update_parameter_in_context_invalid_context():
    """Test update_parameter_in_context with invalid context raises error."""

    import uuid
    with pytest.raises(ValueError, match="Parameter context not found"):
        parameters.update_parameter_in_context(
            context_id=str(uuid.uuid4()),
            param_name="Param",
            value="value"
        )


# =============================================================================
# prepare_parameter Value Handling Tests
# =============================================================================


def test_prepare_parameter_with_value():
    """Test prepare_parameter with explicit value sets the value."""
    param = parameters.prepare_parameter("TestParam", value="test_value")
    assert param.parameter.name == "TestParam"
    assert param.parameter.value == "test_value"
    assert param.parameter.value_removed is None


def test_prepare_parameter_with_empty_string():
    """Test prepare_parameter with empty string sets empty string value."""
    param = parameters.prepare_parameter("TestParam", value="")
    assert param.parameter.name == "TestParam"
    assert param.parameter.value == ""
    assert param.parameter.value_removed is None


def test_prepare_parameter_with_none_unsets_value():
    """Test prepare_parameter with value=None sets value_removed=True."""
    param = parameters.prepare_parameter("TestParam", value=None)
    assert param.parameter.name == "TestParam"
    assert param.parameter.value is None
    assert param.parameter.value_removed is True


def test_prepare_parameter_omitted_value_leaves_unchanged():
    """Test prepare_parameter without value arg doesn't include value in DTO."""
    param = parameters.prepare_parameter("TestParam")
    assert param.parameter.name == "TestParam"
    assert param.parameter.value is None
    assert param.parameter.value_removed is None  # Not set = leave unchanged


def test_prepare_parameter_update_description_only():
    """Test prepare_parameter can update description without touching value."""
    param = parameters.prepare_parameter("TestParam", description="New description")
    assert param.parameter.name == "TestParam"
    assert param.parameter.description == "New description"
    assert param.parameter.value is None
    assert param.parameter.value_removed is None  # Value not touched


def test_prepare_parameter_unset_value_integration(fix_context):
    """Integration test: create param with value, then unset it."""

    ctx = fix_context.generate()

    # Create parameter with a value
    param = parameters.prepare_parameter("UnsetTest", value="initial_value")
    result = parameters.upsert_parameter_to_context(ctx, param)

    # Verify it has a value
    created = next(
        p for p in result.component.parameters if p.parameter.name == "UnsetTest"
    )
    assert created.parameter.value == "initial_value"

    # Now unset the value
    unset_param = parameters.prepare_parameter("UnsetTest", value=None)
    result = parameters.upsert_parameter_to_context(result, unset_param)

    # Verify the value is now unset
    updated = next(
        p for p in result.component.parameters if p.parameter.name == "UnsetTest"
    )
    assert updated.parameter.value is None


def test_prepare_parameter_update_description_preserves_value(fix_context):
    """Integration test: update description without changing existing value."""

    ctx = fix_context.generate()

    # Create parameter with a value
    param = parameters.prepare_parameter(
        "DescTest", value="keep_this", description="Original"
    )
    result = parameters.upsert_parameter_to_context(ctx, param)

    # Verify initial state
    created = next(
        p for p in result.component.parameters if p.parameter.name == "DescTest"
    )
    assert created.parameter.value == "keep_this"
    assert created.parameter.description == "Original"

    # Update only description (omit value)
    desc_only = parameters.prepare_parameter("DescTest", description="Updated")
    result = parameters.upsert_parameter_to_context(result, desc_only)

    # Verify value preserved, description updated
    updated = next(
        p for p in result.component.parameters if p.parameter.name == "DescTest"
    )
    assert updated.parameter.value == "keep_this"
    assert updated.parameter.description == "Updated"
