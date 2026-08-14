import importlib
import os.path as osp

def load(name):
    file_path = osp.join(osp.dirname(__file__), name)
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# def load(name):
#     pathname = osp.join(osp.dirname(__file__), name)
#     print(pathname)
#     return imp.import_module(pathname)
