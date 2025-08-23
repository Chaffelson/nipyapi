#!/usr/bin/env python3
"""
Custom Sphinx documentation generator for NiPyApi.

This script replaces the default sphinx-apidoc behavior to create better-organized,
more navigable documentation that addresses GitHub issue #376.

Instead of monolithic files with 1000+ lines, this creates logical groupings
of APIs and models for easier navigation.

This script automatically introspects the current codebase structure to ensure
it stays synchronized with client generation updates.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

def get_actual_core_modules():
    """Get the actual core nipyapi modules by introspecting __all__."""
    sys.path.insert(0, os.path.abspath('.'))
    try:
        import nipyapi
        # Remove the generated client modules to get just the core modules
        core_modules = [mod for mod in nipyapi.__all__ if mod not in ['nifi', 'registry']]
        return core_modules
    except ImportError:
        # Fallback to known modules if import fails
        return ['canvas', 'config', 'parameters', 'security', 'system', 'utils', 'versioning']

def get_actual_apis(module_path):
    """Get actual APIs by introspecting the generated modules."""
    try:
        module = importlib.import_module(f"{module_path}.apis")
        # Get all classes that end with 'Api'
        apis = []
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and
                name.endswith('Api') and
                hasattr(obj, '__module__') and
                obj.__module__.startswith(module_path)):
                # Convert class name to snake_case module name
                snake_name = ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
                apis.append(snake_name)
        return sorted(apis)
    except (ImportError, AttributeError):
        return []

def categorize_apis_automatically(apis):
    """Automatically categorize APIs based on naming patterns."""
    categories = {
        "core_flow": {
            "title": "Core Flow Management",
            "description": "Essential APIs for managing NiFi flows, processors, and connections",
            "apis": []
        },
        "security": {
            "title": "Security & Access Control",
            "description": "Authentication, authorization, policies, and user management",
            "apis": []
        },
        "data_management": {
            "title": "Data & Provenance",
            "description": "Data transfer, queues, provenance tracking, and lineage",
            "apis": []
        },
        "system_monitoring": {
            "title": "System & Monitoring",
            "description": "System diagnostics, counters, and reporting",
            "apis": []
        },
        "configuration": {
            "title": "Configuration Management",
            "description": "Parameters, controller services, and configuration",
            "apis": []
        },
        "templates_versioning": {
            "title": "Templates & Versioning",
            "description": "Flow templates, snippets, and version control",
            "apis": []
        },
        "infrastructure": {
            "title": "Infrastructure Components",
            "description": "Ports, funnels, labels, and remote connections",
            "apis": []
        },
        "other": {
            "title": "Other APIs",
            "description": "Additional API endpoints",
            "apis": []
        }
    }

    # Categorize based on API names
    for api in apis:
        if any(keyword in api for keyword in ['flow', 'process', 'connection', 'processor']):
            categories["core_flow"]["apis"].append(api)
        elif any(keyword in api for keyword in ['access', 'authentication', 'policies', 'tenant']):
            categories["security"]["apis"].append(api)
        elif any(keyword in api for keyword in ['data_transfer', 'provenance', 'queue']):
            categories["data_management"]["apis"].append(api)
        elif any(keyword in api for keyword in ['system', 'counter', 'reporting']):
            categories["system_monitoring"]["apis"].append(api)
        elif any(keyword in api for keyword in ['parameter', 'controller_service', 'config']):
            categories["configuration"]["apis"].append(api)
        elif any(keyword in api for keyword in ['snippet', 'version', 'template']):
            categories["templates_versioning"]["apis"].append(api)
        elif any(keyword in api for keyword in ['port', 'funnel', 'label', 'remote', 'site']):
            categories["infrastructure"]["apis"].append(api)
        else:
            categories["other"]["apis"].append(api)

    # Remove empty categories
    return {k: v for k, v in categories.items() if v["apis"]}

# Legacy API groupings (kept for reference but will be replaced by automated detection)
NIFI_API_GROUPS = {
    "core_flow": {
        "title": "Core Flow Management",
        "description": "Essential APIs for managing NiFi flows, processors, and connections",
        "apis": [
            "flow_api",
            "process_groups_api",
            "processors_api",
            "connections_api",
            "controller_api",
        ]
    },
    "security": {
        "title": "Security & Access Control",
        "description": "Authentication, authorization, policies, and user management",
        "apis": [
            "access_api",
            "authentication_api",
            "policies_api",
            "tenants_api",
        ]
    },
    "data_management": {
        "title": "Data & Provenance",
        "description": "Data transfer, queues, provenance tracking, and lineage",
        "apis": [
            "data_transfer_api",
            "flow_file_queues_api",
            "provenance_api",
            "provenance_events_api",
        ]
    },
    "system_monitoring": {
        "title": "System & Monitoring",
        "description": "System diagnostics, counters, and reporting",
        "apis": [
            "system_diagnostics_api",
            "counters_api",
            "reporting_tasks_api",
        ]
    },
    "configuration": {
        "title": "Configuration Management",
        "description": "Parameters, controller services, and configuration",
        "apis": [
            "parameter_contexts_api",
            "parameter_providers_api",
            "controller_services_api",
        ]
    },
    "templates_versioning": {
        "title": "Templates & Versioning",
        "description": "Flow templates, snippets, and version control",
        "apis": [
            "snippets_api",
            "versions_api",
        ]
    },
    "infrastructure": {
        "title": "Infrastructure Components",
        "description": "Ports, funnels, labels, and remote connections",
        "apis": [
            "input_ports_api",
            "output_ports_api",
            "funnels_api",
            "labels_api",
            "remote_process_groups_api",
            "site_to_site_api",
        ]
    },
    "resources": {
        "title": "Resources & Utilities",
        "description": "Resource management and utility functions",
        "apis": [
            "resources_api",
        ]
    }
}

# Note: Model groupings removed - using comprehensive single-section approach
# for better cross-referencing between APIs and models

REGISTRY_API_GROUPS = {
    "core": {
        "title": "Core Registry APIs",
        "description": "Flow management, buckets, and version control",
        "apis": ["flows_api", "buckets_api", "items_api"]
    },
    "access": {
        "title": "Access & Security",
        "description": "Authentication and access control",
        "apis": ["access_api", "policies_api", "tenants_api"]
    },
    "config": {
        "title": "Configuration",
        "description": "Configuration and administrative functions",
        "apis": ["config_api", "about_api"]
    }
}


def write_rst_file(filepath, content):
    """Write content to RST file with proper encoding."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {filepath}")


def generate_individual_api_files(apis, base_module, output_dir):
    """Generate individual RST files for each API (flat structure)."""
    api_files = []
    for api in apis:
        api_content = f".. automodule:: {base_module}.{api}\n"
        api_content += "    :members:\n"
        api_content += "    :undoc-members:\n"
        api_content += "    :show-inheritance:\n"

        api_filename = f"{api}.rst"
        api_filepath = os.path.join(output_dir, api_filename)
        write_rst_file(api_filepath, api_content)
        api_files.append(api_filename)

    return api_files


def generate_flat_api_index(api_files, base_module, output_dir, title_prefix):
    """Generate main index file for all APIs (flat structure)."""
    title = f"{title_prefix} APIs"
    content = f"{title}\n"
    content += "=" * len(title) + "\n\n"
    content += f"Complete {title_prefix} REST API client documentation.\n\n"

    content += f"This section documents all **{len(api_files)}** {title_prefix} API classes. "
    content += f"Each API class provides methods for interacting with specific {title_prefix} endpoints. "
    content += "Click any API to see its methods and their model parameters.\n\n"

    # Add clean toctree with all APIs
    content += ".. toctree::\n"
    content += "   :maxdepth: 1\n\n"

    for api_file in sorted(api_files):
        # Clean display name: connections_api -> Connections API
        api_name = api_file.replace('.rst', '').replace('_api', '').replace('_', ' ').title() + ' API'
        content += f"   {api_file.replace('.rst', '')}\n"

    filepath = os.path.join(output_dir, "index.rst")
    write_rst_file(filepath, content)


def generate_core_module_docs(output_dir):
    """Generate modular documentation for core nipyapi modules."""
    # Get actual modules from the codebase
    actual_modules = get_actual_core_modules()

    # Module descriptions
    module_descriptions = {
        "canvas": "Canvas operations and flow management",
        "config": "Configuration management",
        "parameters": "Parameter context management",
        "security": "Security and authentication utilities",
        "system": "System information and diagnostics",
        "utils": "Utility functions and helpers",
        "versioning": "Version control operations",
    }

    # Create core_modules directory
    core_modules_dir = os.path.join(output_dir, "core_modules")
    os.makedirs(core_modules_dir, exist_ok=True)

    # Generate individual module files
    for module_name in actual_modules:
        description = module_descriptions.get(module_name, f"{module_name.title()} functionality")
        module_title = module_name.title()

        content = f"{module_title}\n"
        content += "=" * len(module_title) + "\n\n"
        content += f"{description}\n\n"
        content += f".. automodule:: nipyapi.{module_name}\n"
        content += "    :members:\n"
        content += "    :undoc-members:\n"
        content += "    :show-inheritance:\n"

        filepath = os.path.join(core_modules_dir, f"{module_name}.rst")
        write_rst_file(filepath, content)

    # Generate core modules index
    title = "Core Client Modules"
    content = f"{title}\n"
    content += "=" * len(title) + "\n\n"
    content += "These modules provide high-level convenience functions for common NiFi operations.\n"
    content += "They wrap the lower-level generated API clients with Pythonic interfaces.\n\n"

    # Add toctree for separate module files
    content += ".. toctree::\n"
    content += "   :maxdepth: 1\n\n"

    for module_name in actual_modules:
        content += f"   core_modules/{module_name}\n"

    filepath = os.path.join(output_dir, "core_modules.rst")
    write_rst_file(filepath, content)
    return "core_modules.rst"


def generate_main_api_reference(output_dir):
    """Generate the main API reference index."""
    title = "API Reference"
    content = f"{title}\n"
    content += "=" * len(title) + "\n\n"
    content += "Complete API documentation for NiPyApi, organized for easy navigation.\n\n"

    content += ".. toctree::\n"
    content += "   :maxdepth: 2\n"
    content += "   :caption: Documentation Sections\n\n"
    content += "   client_architecture\n"
    content += "   core_modules\n"
    content += "   nifi_apis/index\n"
    content += "   nifi_models/index\n"
    content += "   registry_apis/index\n"
    content += "   registry_models/index\n"
    content += "   examples\n\n"

    content += "Overview\n"
    content += "--------\n\n"
    content += "**Core Modules**: High-level Python interfaces for common operations\n\n"
    content += "**NiFi APIs**: Complete generated client for all NiFi REST endpoints\n\n"
    content += "**NiFi Models**: Data structures and DTOs used by NiFi APIs\n\n"
    content += "**Registry APIs**: Complete generated client for NiFi Registry\n\n"
    content += "**Registry Models**: Data structures used by Registry APIs\n\n"
    content += "**Examples**: Example scripts and tutorials\n\n"

    filepath = os.path.join(output_dir, "api_reference.rst")
    write_rst_file(filepath, content)


def generate_examples_docs(output_dir):
    """Generate documentation for example scripts (not a module)."""
    title = "Examples and Tutorials"
    content = f"{title}\n"
    content += "=" * len(title) + "\n\n"
    content += "Example scripts demonstrating NiPyApi functionality can be found in the\n"
    content += "`examples/ directory <https://github.com/Chaffelson/nipyapi/tree/master/examples>`_\n"
    content += "of the source repository.\n\n"

    content += "Available Examples\n"
    content += "------------------\n\n"
    content += "* **fdlc.py**: Flow Development Life Cycle examples\n\n"

    content += "Sandbox Environment\n"
    content += "-------------------\n\n"
    content += "For quick experimentation, use the sandbox make target to set up a ready-to-use environment:\n\n"
    content += ".. code-block:: console\n\n"
    content += "    $ make sandbox NIPYAPI_PROFILE=single-user     # Recommended - simple setup\n"
    content += "    $ make sandbox NIPYAPI_PROFILE=secure-ldap     # LDAP authentication\n"
    content += "    $ make sandbox NIPYAPI_PROFILE=secure-mtls     # Certificate authentication (advanced)\n\n"
    content += "The sandbox automatically creates:\n\n"
    content += "* Properly configured authentication and SSL\n"
    content += "* Sample registry client and bucket\n"
    content += "* Simple demo flow ready for experimentation\n"
    content += "* All necessary security bootstrapping\n\n"
    content += "When finished experimenting:\n\n"
    content += ".. code-block:: console\n\n"
    content += "    $ make down  # Clean up Docker containers\n\n"

    content += ".. note::\n"
    content += "   These are standalone Python scripts, not importable modules.\n"
    content += "   Run them directly with Python after setting up your environment.\n\n"

    filepath = os.path.join(output_dir, "examples.rst")
    write_rst_file(filepath, content)


def generate_client_architecture_docs(output_dir):
    """Generate documentation explaining the client architecture."""
    title = "Client Architecture"
    content = f"{title}\n"
    content += "=" * len(title) + "\n\n"
    content += "Understanding how NiPyApi clients are structured and how to use them effectively.\n\n"

    content += "Client Layers\n"
    content += "-------------\n\n"
    content += "NiPyApi provides multiple layers of abstraction:\n\n"
    content += "**Core Modules** (High-level): :doc:`core_modules` - Convenient Python functions for common operations\n\n"
    content += "**Generated APIs** (Low-level): :doc:`nifi_apis/index` and :doc:`registry_apis/index` - Direct REST API access\n\n"
    content += "**Models**: :doc:`nifi_models/index` and :doc:`registry_models/index` - Data structures used by APIs\n\n"

    content += "Generated API Structure\n"
    content += "-----------------------\n\n"
    content += "Each generated API class provides two methods for every operation:\n\n"
    content += "**Base Methods** (e.g., ``copy()``)\n"
    content += "  Return response data directly. Use these for most operations.\n\n"
    content += "**HTTP Info Methods** (e.g., ``copy_with_http_info()``)\n"
    content += "  Return detailed response including status code and headers.\n"
    content += "  Use when you need HTTP metadata or error details.\n\n"

    content += "Example Usage\n"
    content += "~~~~~~~~~~~~~\n\n"
    content += ".. code-block:: python\n\n"
    content += "   import nipyapi\n\n"
    content += "   # High-level approach (recommended for most users)\n"
    content += "   process_groups = nipyapi.canvas.list_all_process_groups()\n\n"
    content += "   # Low-level API approach\n"
    content += "   api_instance = nipyapi.nifi.ProcessGroupsApi()\n"
    content += "   \n"
    content += "   # Get just the data\n"
    content += "   flow = api_instance.get_flow('root')\n"
    content += "   \n"
    content += "   # Get data + HTTP details\n"
    content += "   flow, status, headers = api_instance.get_flow_with_http_info('root')\n"
    content += "   print(f\"HTTP Status: {status}\")\n\n"

    content += "Callback Functions\n"
    content += "------------------\n\n"
    content += "The generated clients support callback functions for asynchronous operations:\n\n"
    content += ".. code-block:: python\n\n"
    content += "   def my_callback(response):\n"
    content += "       print(f\"Response received: {response}\")\n\n"
    content += "   # Use callback for async-style processing\n"
    content += "   api_instance.get_flow('root', callback=my_callback)\n\n"
    content += "**Note**: Callbacks are inherited from the original Swagger-generated client.\n"
    content += "They maintain backwards compatibility but are not commonly used.\n\n"

    content += "Error Handling\n"
    content += "--------------\n\n"
    content += "APIs can raise exceptions on HTTP errors:\n\n"
    content += ".. code-block:: python\n\n"
    content += "   from nipyapi.nifi.rest import ApiException\n\n"
    content += "   try:\n"
    content += "       flow = api_instance.get_flow('invalid-id')\n"
    content += "   except ApiException as e:\n"
    content += "       print(f\"API Error: {e.status} - {e.reason}\")\n\n"

    content += "Model Cross-References\n"
    content += "----------------------\n\n"
    content += "API documentation includes clickable links to model classes.\n"
    content += "Click any model type (e.g., :class:`~nipyapi.nifi.models.ProcessGroupEntity`) "
    content += "to jump to its detailed documentation.\n\n"

    filepath = os.path.join(output_dir, "client_architecture.rst")
    write_rst_file(filepath, content)


def generate_comprehensive_models_docs(base_module, output_dir, title_prefix):
    """Generate comprehensive model documentation with all classes for proper cross-referencing."""
    title = f"{title_prefix} Models"

    # Get all model classes from the module
    try:
        import importlib
        module = importlib.import_module(base_module)
        # Get all classes that don't start with underscore
        model_classes = [name for name in dir(module)
                        if not name.startswith('_') and
                        hasattr(getattr(module, name), '__module__') and
                        getattr(module, name).__module__.startswith(base_module)]
        print(f"   Found {len(model_classes)} model classes")
    except Exception as e:
        print(f"   ⚠️  Could not import {base_module}: {e}")
        model_classes = []

    content = f"{title}\n"
    content += "=" * len(title) + "\n\n"
    content += f"Complete model class reference for {title_prefix} APIs.\n\n"

    if model_classes:
        content += f"This reference documents all **{len(model_classes)}** model classes used by {title_prefix} APIs. "
        content += "These classes are automatically cross-referenced from API documentation - "
        content += "click any model type in API documentation to jump directly to its definition here.\n\n"

        content += "Model Type Patterns\n"
        content += "--------------------\n\n"
        content += "**Entity Classes** (e.g., ProcessGroupEntity): Complete API objects with metadata and revision information\n\n"
        content += "**DTO Classes** (e.g., ProcessGroupDTO): Core data transfer objects containing the essential properties\n\n"
        content += "**Status Classes** (e.g., ProcessGroupStatus): Runtime status and statistics for monitoring\n\n"
        content += "**Configuration Classes**: Settings, parameters, and configuration objects\n\n"

        content += f"\n.. currentmodule:: {base_module}\n\n"
        content += "All Model Classes\n"
        content += "------------------\n\n"

        # Document ALL classes individually for proper cross-referencing
        for cls in sorted(model_classes):
            content += f".. autoclass:: {cls}\n"
            content += f"   :members:\n"
            content += f"   :show-inheritance:\n\n"

    else:
        content += ".. note::\n"
        content += f"   Model classes for {title_prefix} could not be loaded.\n"
        content += f"   Please check the :py:mod:`{base_module}` module.\n\n"

    # Create index file
    index_content = f"{title}\n"
    index_content += "=" * len(title) + "\n\n"
    index_content += f"Complete {title_prefix} model class documentation with cross-reference support.\n\n"
    index_content += ".. toctree::\n"
    index_content += "   :maxdepth: 1\n\n"
    index_content += "   models\n\n"

    os.makedirs(output_dir, exist_ok=True)
    write_rst_file(os.path.join(output_dir, "index.rst"), index_content)
    write_rst_file(os.path.join(output_dir, "models.rst"), content)


def generate_dependencies_docs(docs_dir):
    """Generate dependencies documentation from actual dependency files."""
    import re

    project_root = Path(__file__).parent.parent.parent

    # Read requirements.txt
    requirements_file = project_root / "requirements.txt"
    runtime_deps = []

    if requirements_file.exists():
        with open(requirements_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    runtime_deps.append(line)

    # Read pyproject.toml for optional dependencies
    pyproject_file = project_root / "pyproject.toml"
    dev_deps = []
    docs_deps = []

    if pyproject_file.exists():
        # Try to parse pyproject.toml for optional dependencies
        try:
            # Python 3.11+ has tomllib built-in
            try:
                import tomllib
            except ImportError:
                # Fallback to tomli for older Python versions
                try:
                    import tomli as tomllib
                except ImportError:
                    tomllib = None

            if tomllib:
                with open(pyproject_file, 'rb') as f:
                    data = tomllib.load(f)
                    optional_deps = data.get('project', {}).get('optional-dependencies', {})
                    dev_deps = optional_deps.get('dev', [])
                    docs_deps = optional_deps.get('docs', [])
            else:
                # Fallback: parse manually for known sections
                print("⚠️  TOML parsing not available, using basic fallback")
                with open(pyproject_file, 'r') as f:
                    content = f.read()
                    # Simple regex-based parsing for our specific use case
                    if '[project.optional-dependencies]' in content:
                        lines = content.split('\n')
                        in_dev = False
                        in_docs = False
                        for line in lines:
                            line = line.strip()
                            if line.startswith('dev = ['):
                                in_dev = True
                                in_docs = False
                            elif line.startswith('docs = ['):
                                in_docs = True
                                in_dev = False
                            elif line.startswith(']'):
                                in_dev = in_docs = False
                            elif in_dev and line.startswith('"') and line.endswith('",'):
                                dev_deps.append(line.strip('"",'))
                            elif in_docs and line.startswith('"') and line.endswith('",'):
                                docs_deps.append(line.strip('"",'))
        except Exception as e:
            print(f"⚠️  Could not parse pyproject.toml: {e}")
            print("   Continuing with runtime dependencies only...")

    # Categorize runtime dependencies
    def categorize_runtime_deps(deps):
        categories = {
            'Core HTTP Stack': [],
            'Utilities': [],
            'Build & Packaging': []
        }

        for dep in deps:
            dep_lower = dep.lower()
            if any(x in dep_lower for x in ['requests', 'urllib3', 'certifi', 'pysocks']):
                categories['Core HTTP Stack'].append(dep)
            elif any(x in dep_lower for x in ['pyyaml', 'packaging']):
                categories['Utilities'].append(dep)
            elif any(x in dep_lower for x in ['setuptools']):
                categories['Build & Packaging'].append(dep)
            else:
                categories['Utilities'].append(dep)  # Default category

        return categories

    runtime_categories = categorize_runtime_deps(runtime_deps)

    # Generate the dependencies.rst file
    deps_content = """Dependencies
-------------

NiPyAPI automatically manages its dependencies during installation. Here are the complete dependency details, automatically generated from the actual project dependency files.

Runtime Dependencies
--------------------

These dependencies are automatically installed when you install NiPyAPI:

"""

    # Add runtime dependencies by category
    for category, deps in runtime_categories.items():
        if deps:
            deps_content += f"\n**{category}:**\n\n"
            for dep in sorted(deps):
                # Parse dependency for description
                dep_name = re.split(r'[>=<]', dep)[0]

                descriptions = {
                    'requests': 'Primary HTTP client for API communication',
                    'urllib3': 'HTTP client backend and connection pooling',
                    'certifi': 'SSL certificate verification',
                    'pysocks': 'SOCKS proxy support',
                    'PyYAML': 'YAML file processing and serialization',
                    'packaging': 'Version comparison utilities',
                    'setuptools': 'Package management and distribution'
                }

                desc = descriptions.get(dep_name, 'Required dependency')
                deps_content += f"- ``{dep}`` - {desc}\n"

    # Add optional dependencies
    if dev_deps or docs_deps:
        deps_content += "\nOptional Dependencies\n---------------------\n\n"

        if dev_deps:
            deps_content += "**Development Dependencies** (install with ``pip install nipyapi[dev]``):\n\n"
            for dep in sorted(dev_deps):
                dep_name = re.split(r'[>=<]', dep)[0]
                dev_descriptions = {
                    'pytest': 'Testing framework',
                    'pytest-cov': 'Test coverage measurement',
                    'coverage': 'Coverage analysis and reporting',
                    'codecov': 'Coverage reporting service integration',
                    'flake8': 'Code style and syntax checking',
                    'pylint': 'Advanced code analysis and linting',
                    'deepdiff': 'Deep data structure comparison for testing',
                    'twine': 'Package distribution to PyPI'
                }
                desc = dev_descriptions.get(dep_name, 'Development tool')
                deps_content += f"- ``{dep}`` - {desc}\n"

        if docs_deps:
            deps_content += "\n**Documentation Dependencies** (install with ``pip install nipyapi[docs]``):\n\n"
            for dep in sorted(docs_deps):
                dep_name = re.split(r'[>=<]', dep)[0]
                docs_descriptions = {
                    'Sphinx': 'Documentation generation framework',
                    'sphinx_rtd_theme': 'Read the Docs theme for Sphinx',
                    'sphinxcontrib-jquery': 'jQuery support for Sphinx themes'
                }
                desc = docs_descriptions.get(dep_name, 'Documentation tool')
                deps_content += f"- ``{dep}`` - {desc}\n"

    deps_content += f"""
Dependency Management
---------------------

**Automatic Installation:**
All runtime dependencies are automatically installed when you install NiPyAPI via pip.

**Version Constraints:**
NiPyAPI specifies minimum versions for compatibility but allows newer versions unless there are known incompatibilities.

**Development Setup:**
For a complete development environment with all optional dependencies:

.. code-block:: console

    $ pip install -e ".[dev,docs]"

**Minimal Installation:**
NiPyAPI requires only {len(runtime_deps)} runtime dependencies for basic functionality.

.. note::
   This dependency information is automatically generated from the project's
   ``requirements.txt`` and ``pyproject.toml`` files during documentation build.

"""

    # Write the dependencies file
    deps_file = docs_dir / "dependencies.rst"
    with open(deps_file, 'w') as f:
        f.write(deps_content)

    print(f"Generated: {deps_file}")
    return deps_file


def main():
    """Generate structured documentation."""
    print("🚀 Generating structured NiPyApi documentation...")
    print("🔍 Auto-detecting current codebase structure...")

    # Base output directory
    docs_dir = Path("docs/nipyapi-docs")

    # Clean and recreate output directory
    import shutil
    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Generate core modules documentation
    print("\n📚 Generating core modules...")
    actual_modules = get_actual_core_modules()
    generate_core_module_docs(docs_dir)
    print(f"Generated: docs/nipyapi-docs/core_modules.rst (index)")
    for module in actual_modules:
        print(f"Generated: docs/nipyapi-docs/core_modules/{module}.rst")

    # Auto-detect and generate NiFi API documentation (flat structure)
    print("\n🔧 Auto-detecting NiFi APIs...")
    nifi_apis = get_actual_apis("nipyapi.nifi")
    print(f"   Found {len(nifi_apis)} APIs")

    nifi_apis_dir = docs_dir / "nifi_apis"
    nifi_apis_dir.mkdir(exist_ok=True)

    nifi_api_files = generate_individual_api_files(nifi_apis, "nipyapi.nifi.apis", nifi_apis_dir)
    generate_flat_api_index(nifi_api_files, "nipyapi.nifi.apis", nifi_apis_dir, "NiFi")

    # Auto-detect and generate Registry API documentation (flat structure)
    print("\n📋 Auto-detecting Registry APIs...")
    registry_apis = get_actual_apis("nipyapi.registry")
    print(f"   Found {len(registry_apis)} APIs")

    registry_apis_dir = docs_dir / "registry_apis"
    registry_apis_dir.mkdir(exist_ok=True)

    registry_api_files = generate_individual_api_files(registry_apis, "nipyapi.registry.apis", registry_apis_dir)
    generate_flat_api_index(registry_api_files, "nipyapi.registry.apis", registry_apis_dir, "Registry")

    # Generate comprehensive model documentation for cross-referencing
    print("\n📊 Generating model documentation...")
    generate_comprehensive_models_docs("nipyapi.nifi.models", docs_dir / "nifi_models", "NiFi")
    generate_comprehensive_models_docs("nipyapi.registry.models", docs_dir / "registry_models", "Registry")

    # Generate examples documentation (not a module)
    print("\n🎯 Generating examples documentation...")
    generate_examples_docs(docs_dir)

    # Generate client architecture documentation
    print("\n📚 Generating client architecture documentation...")
    generate_client_architecture_docs(docs_dir)

    # Generate dependencies documentation
    print("\n📦 Generating dependencies documentation...")
    generate_dependencies_docs(docs_dir)

    # Generate main API reference
    print("\n📖 Generating main API reference...")
    generate_main_api_reference(docs_dir)

    print(f"\n✅ Documentation generation complete!")
    print(f"📁 Output directory: {docs_dir.resolve()}")
    print(f"🔗 Entry point: {docs_dir / 'api_reference.rst'}")
    print(f"🤖 Auto-detected: {len(nifi_apis)} NiFi APIs, {len(registry_apis)} Registry APIs")


if __name__ == "__main__":
    main()
