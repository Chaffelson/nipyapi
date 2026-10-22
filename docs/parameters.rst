Parameter providers and contexts
================================

Provider workflow
-----------------

Discover configured providers with ``list_all_parameter_providers()`` and
``get_parameter_provider()``. Discover installed provider types with
``list_all_parameter_provider_types()`` and ``get_parameter_provider_type()``.
Lookups return ``None``, a single model, or a list of matches. Mutating helpers
require exactly one provider.

The provider operation helpers accept ``refresh=True`` by default: resolve the
input, get a fresh provider by ID, then perform the operation. Set
``refresh=False`` to use the resolved entity without that extra GET; NiFi rejects
it if its revision is stale. The inheritance, alias, and process-group binding
helpers always re-read their target, because the update is built from its current
state. Refreshing does not lock the object.

.. code-block:: python

    from nipyapi import parameters

    provider = parameters.get_parameter_provider("my-provider", greedy=False)
    fetched = parameters.fetch_parameter_provider(provider)
    result = parameters.apply_parameter_provider(
        provider,
        group_names=["my-secrets"],
        fetch_result=fetched,
    )
    affected = result.referencing_components

Fetching is a write: it stages source parameters in NiFi. Applying creates or
updates parameter contexts and may stop and restart affected components.
New parameters default to ``SENSITIVE``. Explicit per-parameter ``sensitivities``
overrides take precedence over existing staged choices, which take precedence
over the default. The staged ``synchronized`` setting is also kept unless
``synchronized`` is passed; unset groups default to synchronized, because NiFi
only creates or updates contexts for synchronized groups. Both apply and context-inheritance operations wait for completion
and return the completed request DTO. They delete the server-side request only
once completion is observed, whether it succeeded or failed. A terminal request
failure is raised with NiFi's diagnostic; if deletion also fails, that failure
remains primary and a cleanup warning is logged. Deletion errors otherwise propagate.
Timeouts, polling errors and interruptions do not delete an unfinished request:
early deletion would cancel subsequent server-side steps. NiFi may continue the
operation after the client stops waiting; interruption is not a rollback.

For a combined operation, use ``fetch_and_apply_parameter_provider(provider)``.
The CLI form is ``nipyapi parameters fetch_and_apply_parameter_provider <provider-id>``; a UUID is looked up by ID automatically.
It rejects missing or empty selected groups by default. Scope provider properties
before fetching.

Per-parameter ``sensitivities`` overrides are keyed by parameter name and apply in
every selected group; a name that matches no selected parameter raises
``ValueError`` rather than being ignored. Both apply helpers accept
``sensitivities`` and ``synchronized``. If no selected group is synchronized, NiFi
completes the request without changing anything, and nipyapi logs a warning.

Sensitive data and diagnostics
------------------------------

NiFi masks sensitive parameter and provider-property values in returned models.
Keep secrets marked sensitive: values deliberately applied as ``NON_SENSITIVE``
are readable from NiFi.

The helpers preserve NiFi's diagnostics. Failed asynchronous operations raise
``ValueError`` with the server's ``failure_reason``. REST failures propagate the
original ``ApiException``, including its status, reason, headers, and response
body. Fetch HTTP 500 errors also log a configuration/source-access/scope hint.
The generated clients retain their existing response-body DEBUG logging.

Context inheritance and aliases
-------------------------------

``get_process_group_parameter_context(pg)`` reads the group's current binding;
it returns ``None`` for an unbound group. ``set_inherited_parameter_contexts``
prepends contexts in precedence order or replaces the inheritance list.

.. code-block:: python

    result = parameters.connect_parameter_provider_group(
        target="my-process-group",
        group_name="my-secrets",
        mappings={"Local API Secret": "API_KEY"},
        greedy=False,
    )

This creates a local sensitive parameter whose value is ``#{API_KEY}`` and inherits
the named context, in one context update. The first inherited context defining a
name takes precedence, and the alias resolves against it, so a newly inherited
context is placed first. An already inherited context keeps its position unless a
higher-precedence context defines a mapped source name; that raises
``ValueError``, and the order can be set explicitly with
``set_inherited_parameter_contexts(..., mode="replace")``. It preserves other
local parameters
and inherited contexts. The target can also be a context entity, process-group
entity, or ID. Ambiguous names and unbound process groups are rejected. Existing
sensitive locals are overwritten with their descriptions kept. Non-sensitive
source parameters are rejected, because NiFi leaves a sensitive alias to them
unresolved. Existing non-sensitive locals are rejected
because NiFi does not allow changing their sensitivity in place. Deleting and
recreating such a parameter is a separate operator-managed change, not an atomic
alias update.

The existing ``update_parameter_context`` and ``upsert_parameter_to_context``
functions continue returning the updated context, not the request DTO.

See :doc:`nipyapi-docs/core_modules/parameters` for the API reference.
