"""
Contains the Glitch object. This object is used by 
an instance of TwitterBot to distort an image during 
the Twitter Ritual

author@matthewfinch
"""

from core import ( io, os, copy, random, Image, logger )

class BadImageException(Exception):
    pass

class Glitch:
    """
        object to glitch image
        ----------------------
        image is glitched with pixel manipulation

        -  pathIn: path to image being glitched
        -  pathOut: path to resultant glitched image
        -  amnt: amount to change pixels by (0-1) - Default set at random
        -  seed: location of pixel changed within a window (0-1) - Default set at random
        -  n_iter: number of pixels (windows) to change - default set at random integer (0 - 40)
     """
    def __init__(self, pathIn: str,
                       pathOut: str, 
                       amnt: float = None, 
                       seed: float = None,
                       n_iter: int = None,
                       max_width: int = 900,
                       max_retries: int = 3,
                       verbose: bool = False):

        self.__pathIn: str = pathIn
        self.__pathOut: str = pathOut
        self.__amnt: float = amnt
        self.__seed: float = seed
        self.__n_iter: int = n_iter
        self.__max_width: int = max_width
        self.__max_retries: int = max_retries
        self.__verbose: bool = verbose

    @property
    def pathIn(self):
        return self.__pathIn

    @property
    def pathOut(self):
        return self.__pathOut

    @property
    def amnt(self):
        return self.__amnt

    @amnt.setter
    def amnt(self, value: float):
        self.__amnt = value

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value: float):
        self.__seed = value

    @property
    def n_iter(self):
        return self.__n_iter

    @n_iter.setter
    def n_iter(self, value: int):
        self.__n_iter = value

    @property
    def max_width(self):
        return self.__max_width

    @property
    def max_retires(self):
        return self.__max_retries

    @property
    def verbose(self):
        return self.__verbose

    def toBytes(self, img: object):
        """function to turn image into bytes"""
        out: object = io.BytesIO()
        img.save(out, quality=95, format='JPEG')
        out.seek(0)
        self.data: bytes = out.read()

    def png2data(self):
        """function to read in png image data"""
        img: object = Image.open(self.path)
        img.convert('RGB')
        self.toBytes(img=img)

    def jpg2data(self):
        """function to read in jpg image data"""
        with open(self.pathIn, 'rb') as f:
             self.data = f.read()

    def data2jpg(self):
        """function to write image as jpeg"""
        with open(self.pathOut, 'wb') as f:
            f.write(self.dataCopy)

    def data2png(self):
        """function to write image as png"""
        try:
            stream: bytes = io.BytesIO(self.dataCopy)
            img: object = Image.open(stream)
            img.save(self.pathOut)
        except Exception as e:
            raise BadImageException(e)

    def readImg(self):
        """function to read in image data"""
        ext: str = os.path.splitext(self.pathIn)[-1]
        if ext == '.png':
            self.png2data()
        elif ext in ('.jpg', '.jpeg', '.jpe'):
            self.jpg2data()
            
        else:
            raise BadImageException(f'Image extension {ext} is not supported')

    def writeImg(self):
        """function to write out image data"""
        ext: str = os.path.splitext(self.pathOut)[-1].lower()
        if ext in ('.jpg', '.jpeg', '.jpe'):
            self.data2jpg()
        elif extension == '.png':
            self.data2png()
        else:
            raise BadImageException(f'Image extension {ext} is not supported')

    def resize(self):
        """function to check and resize image"""
        inp: object = io.BytesIO(self.data)
        img: object = Image.open(inp)
        if img.size[0] > self.max_width:
             wpercent: float = (self.max_width / float(img.size[0]))
             hsize: int = int((float(img.size[1]) * float(wpercent)))
             img: object = img.resize((self.max_width, hsize), Image.ANTIALIAS)
             self.toBytes(img=img)

    def checkVariables(self):
        """function to check variables and set to random if needed"""
        self.amnt = min(self.amnt, 1.) if self.amnt is not None else random.random()
        self.seed = min(self.seed, 1.) if self.seed is not None else random.random()
        self.n_iter = min(self.n_iter, 115) if self.n_iter is not None else random.randint(0, 115)

    def glitch(self) -> bytes:
        """function to glich image by modifying bytes"""
        found: int = self.data.find(bytes((255, 218)))
        if not found: raise BadImageException('Not Valid JPEG')
        header_len: int = found + 2
        self.checkVariables()

        if self.verbose:
            logger.info(f'Data length: {len(self.data)}')
            logger.info(f'Amount: {self.amnt} | Seed: {self.seed} | n_iter: {self.n_iter}')

        max_idx: int = len(self.data) - header_len - 4
        windowSz: int = int(max_idx  // self.n_iter)
        dataCopy: bytearray = bytearray(copy.copy(self.data))

        for i in range(header_len, max_idx, windowSz):
            modified_idx: int = i + int(windowSz * self.seed)
            modified_idx: int = min(modified_idx, max_idx)
            dataCopy[modified_idx]: int = int(self.amnt * 256 / 100)

        return dataCopy

    def processGlitch(self):
        """function to run glitch process and iterate through retires"""
        self.readImg()
        self.resize()
        max_retr = self.max_retires
        self.data = bytearray(self.data)
        while max_retr:
            self.dataCopy = self.glitch()
            try:
                self.writeImg()
                if self.verbose: logger.info(f"glitched image saved to {self.pathOut}")
                return
            except BadImageException:
                max_retr -= 1
                if self.n_iter >= 10:
                    if self.verbose: logger.info(f"Bad Image... retrying | {max_retr} retries left...")
                    self.n_iter = int(0.9 * self.n_iter)