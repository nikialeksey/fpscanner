from RsBytes import RsBytes
from RsPackage import RsPackage


class RsCached(RsPackage):

    def __init__(self, package):
        # type: (RsPackage) -> RsCached
        self.origin = package
        self.cache = []

    def bytes(self):
        # type: () -> RsBytes
        if not self.cache:
            self.cache.append(self.origin.bytes())
        return self.cache[0]
