

class DownloadError(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "Problem downloading content from %s" % url
