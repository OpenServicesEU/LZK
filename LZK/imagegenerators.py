from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


class Slide(ImageSpec):
    processors = [ResizeToFill(1110, 624)]
    format = "WEBP"
    options = {"quality": 70}


register.generator("LZK:slide", Slide)
