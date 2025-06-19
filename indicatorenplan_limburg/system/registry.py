import importlib
import pkgutil
from indicatorenplan_limburg.system.logger import setup_logger
from indicatorenplan_limburg import indicatoren

log = setup_logger(name=__name__)


class IndicatorRegistry(type):
    """Registry for all indicators."""
    INDICATOR_REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if name != "BaseIndicator":  # Avoid registering the base class itself
            # Register the class in the registry with its lowercase name
            indicator_name = new_cls.__name__.lower().replace('indicator', '')
            cls.INDICATOR_REGISTRY[indicator_name] = new_cls
            log.debug(f"Registered indicator: {indicator_name}")
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
        package_path = indicatoren.__path__
        log.debug(f"Discovering indicators in package path: {package_path}")

        for _, module_name, _ in pkgutil.walk_packages(package_path, indicatoren.__name__ + "."):
            try:
                importlib.import_module(module_name)
                log.debug(f"Successfully imported {module_name}")
            except Exception as e:
                log.warning(f"Failed to import {module_name}: {e.__class__.__name__} - {e}")
                cls._fail_load = {
                    module_name: str(e)
                }

        log.info(f"Discovered indicators: {cls.list()}")

