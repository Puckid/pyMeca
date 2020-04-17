"""
geometry module
"""

__version__ = '0.0.1'
__author__ = 'Yann Roth'

import math
import uuid
from datetime import datetime
import pathlib
import pickle
from fuzzywuzzy import fuzz

class PyMecObject:
    """
    define the common properties of all objects to be inherited
    """
    def __init__(self, name=''):
        self.__uid = uuid.uuid4().hex
        self.__name = name

    def __equal__(self, obj):
        return self.uid == obj.uid

    @property
    def uid(self):
        """
        returns identifier of the object
        """
        return self.__uid

    @property
    def name(self):
        """
        returns the name of the object
        """
        return self.__name

    @name.setter
    def name(self, value):
        """
        Setter for the name. The name can be changed at any time
        """
        self.__name = value

class PyMecSession:
    """
    Define a session, used to record objects. What will be saved is what is in
    the workspace.
    """
    def __init__(self):
        self.__workspace = []
        self.__header_common = {'pyMec version': __version__}
        self.__header = {}

    @property
    def workspace(self):
        """
        returns a list of instantiated objects
        """
        return self.__workspace

    @property
    def header_common(self):
        """
        returns the common fixed header
        """
        return self.__header_common

    @property
    def header(self):
        """
        Returns the dictionnary header
        """
        return self.__header

    @header.setter
    def header(self, value):
        """
        Set the header
        """
        self.__header = value

    @header.deleter
    def header(self):
        """
        Delete the header
        """
        self.__header = {}

    def append(self, obj):
        """
        Add a PyMecObject to the workspace
        """
        if not isinstance(obj, PyMecObject):
            raise TypeError("can't add non-PyMecObject to workspace")
        self.__workspace.append(obj)

    def delete(self, obj):
        """
        Remove the object from the workspace
        """
        result = self.search_by_uid(obj.uid)
        self.__workspace.pop(result[0][1])

    def wipe_workspace(self):
        """
        Remove all objects in workspace.
        """
        del self.__workspace[:]

    def search_by_name(self, name):
        """
        Uses fuzzy search to return the most probable object, returns multiple
        objects if same results is found
        """
        scores = [fuzz.ratio(obj.name, name) for obj in self.__workspace]
        best = max(scores)
        if best < 70:
            return []
        return [(x, i) for i, x in enumerate(self.__workspace)
                if scores[i] == best]

    def search_by_uid(self, uid):
        """
        Returns object with corresponding uid and correspond index in
        __workspace. Returns None if uid is not found. Returns an array with
        a single result to be consistant with other search function but can only
        return one result.
        """
        for i, obj in enumerate(self.__workspace):
            if obj.uid == uid:
                return [(obj, i)]
        return None

    def add_to_header(self, header):
        """
        Add info to header for to be stored in save file
        """
        self.__header.update(header)

    def save_to_file(self, filename=None, overwrite=False):
        """
        Saves the current status of the workspace and the header to given file.
        Creates folders if does not exist.
        """
        if filename is None:
            filepath = self.__header['filename']
        else:
            filepath = pathlib.Path(filename)
        self.__header['filename'] = filepath
        self.__header['savedate'] = datetime.now()
        if filepath.exists() and not overwrite:
            raise FileExistsError("File '" + str(filepath) + "' already exist. "
                                  "Set overwrite to True to overwrite")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'bw') as savefile:
            pickle.dump([self.__header_common, self.__header, self.__workspace],
                        savefile, pickle.HIGHEST_PROTOCOL)

    def load_file(self, filename=None, overwrite=False):
        """
        Loads a saved file to workspace.
        """
        if self.__workspace and not overwrite:
            raise FileExistsError("Workspace is not empty. "
                                  "Set overwrite to True to overwrite")
        if filename is None:
            filepath = self.__header['filename']
        else:
            filepath = pathlib.Path(filename)
        with open(filepath, 'br') as savefile:
            loaded = pickle.load(savefile)
        if len(loaded) != 3:
            raise TypeError("Loaded file is not in the appropriate format.")
        self.__header_common = loaded[0]
        self.__header = loaded[1]
        self.__workspace = loaded[2]

class Vector(PyMecObject):
    """
    define a vector
    """
    def __init__(self, coord=None, name=''):
        if coord is None:
            coord = []
        super().__init__(name)
        self.coordinates = [float(i) for i in coord]

    def check_dim(self, vect):
        """
        check that given vector is the same dimension as instance
        raises ValueError
        """
        if self.dim != vect.dim:
            raise ValueError("Vectors are not the same dimension")

    def __add__(self, vect):
        self.check_dim(vect)
        return Vector([sum(x) for x in zip(self.coordinates, vect.coordinates)])

    def __sub__(self, vect):
        self.check_dim(vect)
        return Vector([x[0] - x[1] for x in zip(self.coordinates, vect.coordinates)])

    def __mul__(self, num):
        return Vector([num * coord for coord in self.coordinates])

    def __truediv__(self, num):
        return Vector([coord / num for coord in self.coordinates])

    def __str__(self):
        return self.name + str(self.coordinates)

    def __eq__(self, vector):
        return self.coordinates == vector.coordinates

    @property
    def norm(self):
        """
        returns the norm (length) of the vector
        """
        return math.sqrt(sum([x*x for x in self.coordinates]))

    @property
    def dim(self):
        """
        returns the dimension space of the vector
        """
        return len(self.coordinates)

    def cross_product(self, vect):
        """
        returns the cross product of vectors
        """
        self.check_dim(vect)
        if self.dim != 3:
            raise ValueError("Cross product doesn't exist for vector not in"
                             "dimension 3")
        return Vector([self.coordinates[(i+1)%3]*vect.coordinates[(i+2)%3] -
                       self.coordinates[(i+2)%3]*vect.coordinates[(i+1)%3]
                       for i in range(3)])

class Point(PyMecObject):
    """
    define a point which is some coordinates define by a vector and a frame of
    reference. If no frame of reference is given, standard frame is used.
    """
    def __init__(self, pos=None, name=''):
        if pos is None:
            pos = Vector()
        if not isinstance(pos, Vector):
            raise TypeError("Point position can't be non-Vector")
        super().__init__(name)
        self._position = pos

    @property
    def position(self):
        """
        property of the vector position
        """
        return self._position

    @position.setter
    def position(self, pos):
        if not isinstance(pos, Vector):
            raise TypeError("Point position can't be non-Vector")
        self._position = pos

    def __str__(self):
        return self.name + str(self.position.coordinates)

    def __add__(self, vect):
        """
        A Vector can be added to a Point. returns a Point.
        """
        if not isinstance(vect, Vector):
            raise TypeError("can't add non-Vector to Point")
        return Point(self.position + vect)

    def __sub__(self, point):
        """
        Substracting a point to a point returns a vector
        """
        return self.position - point.position

class Segment(PyMecObject):
    """
    define part of an outline. It has a start and an end. The shape between
    start and end can have different shape.
    TODO: now only straight lines available, add more shapes
    """
    def __init__(self, start=None, end=None, name=''):
        if start is None:
            start = Point()
        if end is None:
            end = Point()
        super().__init__(name)
        self._start = start
        self._end = end

    @property
    def start(self):
        """
        property for the start point
        """
        return self._start

    @start.setter
    def start(self, point):
        self._start = point

    @property
    def end(self):
        """
        property for the end point
        """
        return self._end

    @end.setter
    def end(self, point):
        self._end = point

    def __str__(self):
        return self.name + ':' + str(self.start) + '--' + str(self.end)

    def midpoint(self):
        """
        returns the midpoint of the segment as a Point
        """
        return self.start + (self.end - self.start)/2

class Contour(PyMecObject):
    """
    define the outline of a shape. Is basically a list of segment
    """
    def __init__(self, name=''):
        super().__init__(name)
        self._segment_list = []

    def __str__(self):
        ret = self.name + ':'
        for seg in self._segment_list:
            ret += '\n' + str(seg)
        return ret

    @property
    def segments(self):
        """
        returns the list of segments added to Contour
        """
        return self._segment_list

    def add_segment(self, segment):
        """
        add a segment to the contour
        """
        self._segment_list.append(segment)

def parallelogram(corner=None, vect_1=None, vect_2=None, name=''):
    """
    factory to generate a contour in a parallelogram shape.
    corner -- starting point corner
    vect_1 -- used to define the first side of the parallelogram
    vect_2 -- used to define the second side of the parallelogram
    """
    if corner is None:
        corner = Point()
    if vect_1 is None:
        vect_1 = Vector()
    if vect_2 is None:
        vect_2 = Vector()
    ret = Contour(name)
    c_1 = corner
    c_2 = corner + vect_1
    c_3 = corner + vect_1 + vect_2
    c_4 = corner + vect_2
    ret.add_segment(Segment(c_1, c_2))
    ret.add_segment(Segment(c_2, c_3))
    ret.add_segment(Segment(c_3, c_4))
    ret.add_segment(Segment(c_4, c_1))
    return ret
