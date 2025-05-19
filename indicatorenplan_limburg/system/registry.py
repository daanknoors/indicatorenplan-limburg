import importlib
import pkgutil


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
    def discover_indicators(cls, categories=None):
        """
        Dynamically imports all modules in the metrics package
        to ensure subclasses are defined and registered.
        """
        # import all modules in subfolders
        if categories is None:
            package_name = f"indicatorenplan_limburg.indicatoren"
            for _, module_name, _ in pkgutil.walk_packages([package_name.replace('.', '/')], package_name + "."):
                importlib.import_module(module_name)
        else:
            if isinstance(categories, str):
                categories = [categories]
            for category in categories:

                package_name = f"indicatorenplan_limburg.indicatoren.{category}"
                # check if package name directory exists
                if not importlib.util.find_spec(package_name):
                    raise ImportError(f"Category with directory: '{package_name}' not found.")

                for _, module_name, _ in pkgutil.walk_packages([package_name.replace('.', '/')], package_name + "."):
                    importlib.import_module(module_name)

