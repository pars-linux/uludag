# package abstraction
# provides methods to add/remove files, extract control files
# maintainer: baris and meren

class Package:
    """Package: PISI package class"""
    def __init__(self, packagefn, mode):
        self.filename = packagefn
        self.mode = mode                # bu gerekli mi?
        # etc. etc.

    def add_file(self, fn):
        """add a file to package"""

    def extract(self, outdir):
        """extract entire package contents to directory"""
        extract_dir('', outdir)         # means package root

    def extract_file(self, path, outdir):
        """extract file with path to outdir"""

    def extract_dir(self, dir, outdir):
        """extract directory recursively"""

    def extract_PISI_files(self, outdir):
        """extract PISI control files: metadata.xml, files.xml,
        action scripts, etc."""
        self.extract_file('metadata.xml', outdir)
        self.extract_file('files.xml', outdir)
        self.extract_dir('Config', outdir)
