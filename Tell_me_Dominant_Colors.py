"""
3_Dominant_Color_Webcam_ver.py needs rgb.txt
press 'q' key when you want exit

*** Made by Almighty_Denver ***

"""
import time
from sklearn.cluster import KMeans
import cv2
import numpy as np
import os
import tensorflow as tf
import sys
from PIL import ImageFont, ImageDraw, Image
#-*- coding: utf-8 -*-
# capturing video through webcam
from utils import label_map_util
from utils import visualization_utils as vis_util
cap = cv2.VideoCapture(0)
sys.path.append("..")


# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 4

## Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')




while(1):
    

    # Capture frame-by-frame
    (ret, frame) = cap.read() 
    frame_expanded = np.expand_dims(frame, axis=0)
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})
    
    
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    ymin = boxes[0][0][0]*height
    xmin = boxes[0][0][1]*width
    ymax = boxes[0][0][2]*height
    xmax = boxes[0][0][3]*width


    """COLOR"""

    _, img = cap.read()

    # load the image and convert it from BGR to RGB so that
    # we can dispaly it with matplotlib
    img_C = img[int(ymin):int(ymax), int(xmin):int(xmax)]
    cv2.imshow('croped', img_C)
    img_c = cv2.resize(img, (40, 40), interpolation=cv2.INTER_CUBIC)
    img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2RGB)
   
    # reshape the image to be a list of pixels
    #width와 height를 한개의 array로 통합
    img_c = img_c.reshape((img_c.shape[0] * img_c.shape[1], 3))

    # cluster the pixel intensities
    clt = KMeans(n_clusters = 3)
    clt.fit(img_c)



    """Color Database.
    This file contains one class, called ColorDB, and several utility functions.
    The class must be instantiated by the get_colordb() function in this file,
    passing it a filename to read a database out of.
    The get_colordb() function will try to examine the file to figure out what the
    format of the file is.  If it can't figure out the file format, or it has
    trouble reading the file, None is returned.  You can pass get_colordb() an
    optional filetype argument.
    Supporte file types are:
        X_RGB_TXT -- X Consortium rgb.txt format files.  Three columns of numbers
                    from 0 .. 255 separated by whitespace.  Arbitrary trailing
                    columns used as the color name.
    The utility functions are useful for converting between the various expected
    color formats, and for calculating other color values.
    """
    import re
    from types import *

    class BadColor(Exception):
        pass

    DEFAULT_DB = None
    SPACE = ' '
    COMMASPACE = ', '

    # generic class
    class ColorDB:
        def __init__(self, fp):
            lineno = 2
            self.__name = fp.name
            # Maintain several dictionaries for indexing into the color database.
            # Note that while Tk supports RGB intensities of 4, 8, 12, or 16 bits,
            # for now we only support 8 bit intensities.  At least on OpenWindows,
            # all intensities in the /usr/openwin/lib/rgb.txt file are 8-bit
            #
            # key is (red, green, blue) tuple, value is (name, [aliases])
            self.__byrgb = {}
            # key is name, value is (red, green, blue)
            self.__byname = {}
            # all unique names (non-aliases).  built-on demand
            self.__allnames = None
            for line in fp:
                # get this compiled regular expression from derived class
                mo = self._re.match(line)
                if not mo:
                    print('Error in', fp.name, ' line', lineno, file=sys.stderr)
                    lineno += 1
                    continue
                # extract the red, green, blue, and name
                red, green, blue = self._extractrgb(mo)
                name = self._extractname(mo)
                keyname = name.lower()
                # BAW: for now the `name' is just the first named color with the
                # rgb values we find.  Later, we might want to make the two word
                # version the `name', or the CapitalizedVersion, etc.
                key = (red, green, blue)
                foundname, aliases = self.__byrgb.get(key, (name, []))
                if foundname != name and foundname not in aliases:
                    aliases.append(name)
                self.__byrgb[key] = (foundname, aliases)
                # add to byname lookup
                self.__byname[keyname] = key
                lineno = lineno + 1

        # override in derived classes
        def _extractrgb(self, mo):
            return [int(x) for x in mo.group('red', 'green', 'blue')]

        def _extractname(self, mo):
            return mo.group('name')

        def filename(self):
            return self.__name

        def find_byrgb(self, rgbtuple):
            """Return name for rgbtuple"""
            try:
                return self.__byrgb[rgbtuple]
            except KeyError:
                raise BadColor(rgbtuple) from None

        def find_byname(self, name):
            """Return (red, green, blue) for name"""
            name = name.lower()
            try:
                return self.__byname[name]
            except KeyError:
                raise BadColor(name) from None

        def nearest(self, red, green, blue):
            """Return the name of color nearest (red, green, blue)"""
            # BAW: should we use Voronoi diagrams, Delaunay triangulation, or
            # octree for speeding up the locating of nearest point?  Exhaustive
            # search is inefficient, but seems fast enough.
            nearest = -1
            nearest_name = ''
            for name, aliases in self.__byrgb.values():
                r, g, b = self.__byname[name.lower()]
                rdelta = red - r
                gdelta = green - g
                bdelta = blue - b
                distance = rdelta * rdelta + gdelta * gdelta + bdelta * bdelta
                if nearest == -1 or distance < nearest:
                    nearest = distance
                    nearest_name = name
            return nearest_name

        def unique_names(self):
            # sorted
            if not self.__allnames:
                self.__allnames = []
                for name, aliases in self.__byrgb.values():
                    self.__allnames.append(name)
                self.__allnames.sort(key=str.lower)
            return self.__allnames

        def aliases_of(self, red, green, blue):
            try:
                name, aliases = self.__byrgb[(red, green, blue)]
            except KeyError:
                raise BadColor((red, green, blue)) from None
            return [name] + aliases

    
    class RGBColorDB(ColorDB):
        _re = re.compile(
            r'\s*(?P<red>\d+)\s+(?P<green>\d+)\s+(?P<blue>\d+)\s+(?P<name>.*)')


    class HTML40DB(ColorDB):
        _re = re.compile(r'(?P<name>\S+)\s+(?P<hexrgb>#[0-9a-fA-F]{6})')

        def _extractrgb(self, mo):
            return rrggbb_to_triplet(mo.group('hexrgb'))

    class LightlinkDB(HTML40DB):
        _re = re.compile(r'(?P<name>(.+))\s+(?P<hexrgb>#[0-9a-fA-F]{6})')

        def _extractname(self, mo):
            return mo.group('name').strip()

    class WebsafeDB(ColorDB):
        _re = re.compile('(?P<hexrgb>#[0-9a-fA-F]{6})')

        def _extractrgb(self, mo):
            return rrggbb_to_triplet(mo.group('hexrgb'))

        def _extractname(self, mo):
            return mo.group('hexrgb').upper()

    # format is a tuple (RE, SCANLINES, CLASS) where RE is a compiled regular
    # expression, SCANLINES is the number of header lines to scan, and CLASS is
    # the class to instantiate if a match is found

    FILETYPES = [
        (re.compile('Xorg'), RGBColorDB),
        (re.compile('XConsortium'), RGBColorDB),
        (re.compile('HTML'), HTML40DB),
        (re.compile('lightlink'), LightlinkDB),
        (re.compile('Websafe'), WebsafeDB),
        ]

    def get_colordb(file, filetype=None):
        colordb = None
        fp = open(file)
        try:
            line = fp.readline()
            if not line:
                return None
            # try to determine the type of RGB file it is
            if filetype is None:
                filetypes = FILETYPES
            else:
                filetypes = [filetype]
            for typere, class_ in filetypes:
                mo = typere.search(line)
                if mo:
                    break
            else:
                # no matching type
                return None
            # we know the type and the class to grok the type, so suck it in
            colordb = class_(fp)
        finally:
            fp.close()
        # save a global copy
        global DEFAULT_DB
        DEFAULT_DB = colordb
        return colordb


    
    _namedict = {}

    def rrggbb_to_triplet(color):
        """Converts a #rrggbb color to the tuple (red, green, blue)."""
        rgbtuple = _namedict.get(color)
        if rgbtuple is None:
            if color[0] != '#':
                raise BadColor(color)
            red = color[1:3]
            green = color[3:5]
            blue = color[5:7]
            rgbtuple = int(red, 16), int(green, 16), int(blue, 16)
            _namedict[color] = rgbtuple
        return rgbtuple


    _tripdict = {}
    def triplet_to_rrggbb(rgbtuple):
        """Converts a (red, green, blue) tuple to #rrggbb."""
        global _tripdict
        hexname = _tripdict.get(rgbtuple)
        if hexname is None:
            hexname = '#%02x%02x%02x' % rgbtuple
            _tripdict[rgbtuple] = hexname
        return hexname


    def triplet_to_fractional_rgb(rgbtuple):
        return [x / 256 for x in rgbtuple]


    def triplet_to_brightness(rgbtuple):
        # return the brightness (grey level) along the scale 0.0==black to
        # 1.0==white
        r = 0.299
        g = 0.587
        b = 0.114
        return r*rgbtuple[0] + g*rgbtuple[1] + b*rgbtuple[2]

    
    if __name__ == '__main__':
        colordb = get_colordb('C:\tensorflow1\models\research\object_detectionRGB_REAL.txt')
        if not colordb:
            print('No parseable color database found')
            sys.exit(1)
        # on my system, this color matches exactly
        #center값 확인
        nearest = []
        for center in clt.cluster_centers_:
            center = np.round(center, 0)
            cent = center.tolist()
            for k in range(len(cent)):
                cent[k] = int(cent[k])
                (r, g, b) = cent
            nearnest = colordb.nearest(r, g, b)
            nearest.append(nearnest)

    d = {}
    file = open("C:\\Users\\AlmightyDenver\\Anaconda3\\pkgs\\python-3.7.0-hea74fb7_0\\Tools\\pynche\\X\\RGB_REAL_KR.txt")
    for line in file:
        x = line.split(',')
        key = x[0]
        val = x[1]
        d[key] = val
    
    NE_0 = d[nearest[0]];    NE_1 = d[nearest[2]];    NE_2 = d[nearest[2]]

    #결과 창 만들기. 시력약자를 위해 고대비 배경 - 노랑(BGR), 글자-보라(BGR), 글씨체 - 고딕(HY견고딕), 24p이상
    button_img = Image.new('RGBA', (int(width), 50), (0, 228, 255))
    txt = """색깔은 {}, {}, {} 입니다. """.format(NE_0[:-1], NE_1[:-1], NE_2[:-1])
    fon = ImageFont.truetype("./H2GTRE.TTF", 24, 0) 
    button_draw = ImageDraw.Draw(button_img)
    # put button on source image in position (0, 0)
    button_draw.text((10, 10), str(txt), font = fon, fill=(255, 0, 95))

    
    img = Image.fromarray(img)
    img.paste(button_img, (0,0))
    frame = np.array(img)
    cv2.rectangle(frame, (int(xmin),int(ymin)), (int(xmax),int(ymax)), (0, 255, 0), 2)
    # Display the resulting frame
    cv2.imshow('Tell me Dominant Colors', frame)
    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break
