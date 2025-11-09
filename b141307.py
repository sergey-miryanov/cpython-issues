import importlib.machinery as machinery
import importlib.util
import os
import sys

is_apple_mobile = False

if hasattr(machinery, "ExtensionFileLoader"):
    LoaderClass = machinery.ExtensionFileLoader

dummy_name = "fake_extension_module_for_test"

dummy_path = __file__

loader = LoaderClass(dummy_name, dummy_path)
spec = importlib.util.spec_from_loader(dummy_name, loader)
module = importlib.util.module_from_spec(spec)
