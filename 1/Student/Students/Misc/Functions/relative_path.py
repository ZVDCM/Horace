def relative_path(app, folder, file):
    import os

    return os.path.join(os.getcwd(), '..', app, "\\".join(folder), file).replace("\\", "/")
