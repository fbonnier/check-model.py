# Archives

archive_format = [".tar.gz", ".tar", ".zip", ".rar"]

# Entry: Soure: str, URL/Path of the archive
def is_archive(source) :
    test = [source.endswith(format) for format in archive_format]
    if (True in test):
        # return test.index(True)
        return True
    return False
