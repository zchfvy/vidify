from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree.ElementTree import QName

class VidifyTreeprocessor(Treeprocessor):
    extensions = ["webm", "mp4", "ogg"]
    def __init__(self, md, autoplay, controls, loop, muted):
        self.md = md
        self.autoplay = autoplay
        self.controls = controls
        self.loop = loop
        self.muted = muted

    def run(self, root):
        for img in root.findall(".//img"):
            for extension in self.extensions:
                if img.attrib.get("src", "").lower().endswith(extension):
                    break
            else:
                continue  # not a video format

            img.tag = "video"
            if "alt" in img.attrib.keys():
                del img.attrib["alt"]

            if self.autoplay:
                img.attrib["autoplay"] = "autoplay"
            if self.controls:
                img.attrib["controls"] = "controls"
            if self.loop:
                img.attrib["loop"] = "loop"
            if self.muted:
                img.attrib["muted"] = "muted"

class VidifyExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
                "autoplay" : [False, "Videos should autoplay by default"],
                "controls" : [False, "Videos should have controls by default"],
                "loop" :     [False, "Videos should loop by default"],
                "muted" :    [False, "Videos should be muted by default"],
                }
        super(VidifyExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
                VidifyTreeprocessor(
                    md,
                    autoplay=self.getConfig("autoplay"),
                    controls=self.getConfig("controls"),
                    loop=self.getConfig("loop"),
                    muted=self.getConfig("muted"),
                ),
                "vidifytreeprocessor",
                5)

def makeExtension(**kwargs):
    return VidifyExtension(**kwargs)
