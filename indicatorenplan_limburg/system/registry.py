import importlib
import pkgutil
from indicatorenplan_limburg.system.logger import setup_logger

log = setup_logger(name=__name__)


class IndicatorRegistry(type):
    """Registry for all indicators."""
    INDICATOR_REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if name != "BaseIndicator":  # Avoid registering the base class itself
            # Register the class in the registry with its lowercase name
            cls.INDICATOR_REGISTRY[new_cls.__name__.lower().replace('indicator', '')] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.INDICATOR_REGISTRY)

    @classmethod
    def get(cls, name):
        """Get an indicator class by name."""
        return cls.INDICATOR_REGISTRY.get(name)

    @classmethod
    def list(cls):
        """List all registered indicators."""
        return list(cls.INDICATOR_REGISTRY.keys())

    @classmethod
    def discover_indicators(cls):
        """
        Dynamically imports all modules in the metrics package
        to ensure subclasses are defined and registered.
        """
        # import all modules in subfolders
        package_name = f"indicatorenplan_limburg.indicatoren"

        for _, module_name, _ in pkgutil.walk_packages([package_name.replace('.', '/')], package_name + "."):
            try:
                if module_name.endswith('__init__'):
                    continue

                importlib.import_module(module_name)
                log.info(f"Loaded indicator: {module_name}")
            except Exception as e:
                log.warning(f"Failed to import {module_name}: {e.__class__.__name__} - {e}")
                cls._fail_load = {
                    module_name: str(e)
                }
