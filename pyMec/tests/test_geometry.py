"""
test_geometry module
This implements the unit tests for the geometry module
execute with:
python -m unittest -v test_geometry.py
"""
import unittest
import os
import pyMec.geometry as geometry

class PyMecObjectTest(unittest.TestCase):
    """
    Test the generic class PyMecObject
    """
    def test_equal(self):
        """
        Test equal fonction
        """
        obj_1 = geometry.PyMecObject()
        obj_2 = geometry.PyMecObject()
        self.assertNotEqual(obj_1, obj_2)

    def test_uid(self):
        """
        Test that the uid fonction is working and that we generate different
        uid during init
        """
        obj_1 = geometry.PyMecObject()
        self.assertTrue(obj_1.uid)
        obj_2 = geometry.PyMecObject()
        self.assertNotEqual(obj_1.uid, obj_2.uid)

    def name(self):
        """
        Test that the name fonction is returning the name set at init
        """
        obj_1 = geometry.PyMecObject()
        self.assertEqual(obj_1.name, '')
        obj_2 = geometry.PyMecObject('myname')
        self.assertEqual(obj_2.name, 'myname')
        obj_1.name = 'newname'
        self.assertEqual(obj_1, 'newname')

class PyMecSessionTest(unittest.TestCase):
    """
    Test class GenericObject
    """
    def test_version(self):
        """
        Testing that the version is set. Update when version changes.
        """
        self.assertEqual(geometry.__version__, '0.0.1')

    def test_workspace(self):
        """
        Test getting the workspace.
        """
        session = geometry.PyMecSession()
        elem = geometry.PyMecObject()
        session.append(elem)
        workspace = session.workspace
        self.assertTrue(workspace)
        self.assertEqual(workspace[0], elem)

    def test_header_common(self):
        """
        test header_common
        """
        session = geometry.PyMecSession()
        hdr = session.header_common
        self.assertTrue(hdr['pyMec version'])

    def test_header(self):
        """
        test header
        """
        session = geometry.PyMecSession()
        self.assertFalse(session.header)
        session.header = {'prop_1':'a', 'prop_2':'b'}
        self.assertEqual(len(session.header), 2)

    def test_append(self):
        """
        Testing the append fonction
        """
        session = geometry.PyMecSession()
        self.assertFalse(session.workspace)
        session.append(geometry.PyMecObject())
        self.assertEqual(len(session.workspace), 1)

    def test_delete(self):
        """
        Test that we actually delete the right element.
        depends on:
        PyMecSession.append
        PyMecSession.search_by_uid
        """
        session = geometry.PyMecSession()
        elem = geometry.PyMecObject('to be deleted')
        session.append(elem)
        for _ in range(5):
            session.append(geometry.PyMecObject())
        n_obj = len(session.workspace)
        session.delete(elem)
        self.assertEqual(len(session.workspace), n_obj - 1)
        result = session.search_by_uid(elem.uid)
        self.assertFalse(result)

    def test_wipe_workspace(self):
        """
        Test that the workspace is actually empty after wiping
        """
        session = geometry.PyMecSession()
        session.append(geometry.PyMecObject())
        self.assertTrue(session.workspace)
        session.wipe_workspace()
        self.assertFalse(session.workspace)

    def test_search_by_name(self):
        """
        Test the search is working, especially the fuzzy search
        """
        session = geometry.PyMecSession()
        obj_1 = geometry.PyMecObject("this is a schmilblick")
        obj_2 = geometry.PyMecObject("Object_2")
        obj_3 = geometry.PyMecObject("Object_3")
        obj_4 = geometry.PyMecObject("Object_4")
        session.append(obj_1)
        session.append(obj_2)
        session.append(obj_3)
        session.append(obj_4)
        result = session.search_by_name("tihs a si schmilblick")
        self.assertEqual(obj_1.uid, result[0][0].uid, "Wrong result with fuzzy")
        workspace = session.workspace
        self.assertEqual(obj_1.uid, workspace[result[0][1]].uid, "Index is wrong")
        result = session.search_by_name("Nothin in common")
        self.assertFalse(result, "Fuzzy might be too fuzzy")

    def test_search_by_uid(self):
        """
        Test that we receive the correct uid
        """
        session = geometry.PyMecSession()
        obj = geometry.PyMecObject()
        session.append(obj)
        for _ in range(5):
            session.append(geometry.PyMecObject())
        result = session.search_by_uid(obj.uid)
        self.assertEqual(len(result), 1)
        self.assertEqual(obj.uid, result[0][0].uid)
        workspace = session.workspace
        self.assertEqual(obj.uid, workspace[result[0][1]].uid)
        result = session.search_by_uid('this is not a uid')
        self.assertFalse(result)

    def test_save_load_file(self):
        """
        test if file saving is working
        """
        dirname = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dirname, 'test_save_load.pymec')
        session = geometry.PyMecSession()
        obj = geometry.PyMecObject('an object')
        session.append(obj)
        self.assertRaises(KeyError, session.save_to_file)
        self.assertRaises(FileExistsError, session.save_to_file, filename)
        session.save_to_file(filename, True)
        new_session = geometry.PyMecSession()
        self.assertRaises(FileExistsError, session.load_file)
        self.assertRaises(KeyError, new_session.load_file)
        new_session.load_file(filename)
        self.assertEqual(session.workspace[0].uid, new_session.workspace[0].uid)
        session.load_file(overwrite=True)

class VectorTest(unittest.TestCase):
    """
    Test class VectorTest
    """
    def test_check_dim(self):
        """
        Test that check_dim is actually checking and working
        """
        v_1 = geometry.Vector([1, 2])
        v_2 = geometry.Vector([3, 4])
        v_3 = geometry.Vector([1, 2, 3])
        v_1.check_dim(v_2)
        self.assertRaises(ValueError, v_1.check_dim, v_3)

    def test_add(self):
        """
        Test that the add function is working
        """
        v_1 = geometry.Vector([1, 2])
        v_2 = geometry.Vector([3, 4])
        v_3 = v_1 + v_2
        self.assertEqual(v_3.coordinates, [4, 6])
        v_4 = geometry.Vector([1, 2, 3])
        self.assertRaises(ValueError, v_1.__add__, v_4)

    def test_sub(self):
        """
        Test the sub function
        """
        v_1 = geometry.Vector([1, 2])
        v_2 = geometry.Vector([3, 4])
        v_3 = v_1 - v_2
        self.assertEqual(v_3.coordinates, [-2, -2])
        v_4 = geometry.Vector([1, 2, 3])
        self.assertRaises(ValueError, v_1.__sub__, v_4)

    def test_mul(self):
        """
        Test the mul function
        """
        v_1 = geometry.Vector([1, 2, 3])
        self.assertRaises(TypeError, v_1.__mul__, 'a')
        self.assertRaises(TypeError, v_1.__mul__, [2])
        v_2 = v_1 * 2
        self.assertEqual(v_2.coordinates, [2, 4, 6])

    def test_truediv(self):
        """
        Test the truediv function
        """
        v_1 = geometry.Vector([2, 4, 6])
        self.assertRaises(TypeError, v_1.__truediv__, 'a')
        self.assertRaises(TypeError, v_1.__truediv__, [2])
        v_2 = v_1 / 2
        self.assertEqual(v_2.coordinates, [1, 2, 3])

    def test_eq(self):
        """
        Test the equal fonction
        """
        v_1 = geometry.Vector([1, 2])
        v_2 = geometry.Vector([1, 2])
        v_3 = geometry.Vector([1, 3])
        v_4 = geometry.Vector([1, 2, 3])
        self.assertEqual(v_1 == v_2, True)
        self.assertEqual(v_1 == v_3, False)
        self.assertEqual(v_1 == v_4, False)

    def test_norm(self):
        """
        Test that we get the right norm
        """
        v_1 = geometry.Vector([3, 4])
        self.assertEqual(v_1.norm, 5)
        v_2 = geometry.Vector([1, 2, 3])
        self.assertAlmostEqual(v_2.norm, 3.74165738677)

    def test_len(self):
        """
        Test the len function
        """
        v_1 = geometry.Vector([1, 2])
        v_2 = geometry.Vector([1, 2, 3])
        self.assertEqual(len(v_1), 2)
        self.assertEqual(len(v_2), 3)

    def test_cross_product(self):
        """
        Test the cross product function
        """
        a_1 = geometry.Vector([2, 0, 0])
        a_2 = geometry.Vector([0, 2, 0])
        a_3 = a_1.cross_product(a_2)
        a_3_check = geometry.Vector([0, 0, 4])
        self.assertEqual(a_3 == a_3_check, True)
        b_1 = geometry.Vector([1, 2, 0])
        b_2 = geometry.Vector([2, 4, 0])
        b_3 = b_1.cross_product(b_2)
        b_3_check = geometry.Vector([0, 0, 0])
        self.assertEqual(b_3 == b_3_check, True)
        c_1 = geometry.Vector([1, 2, 3, 4])
        self.assertRaises(ValueError, c_1.cross_product, a_1)
        self.assertRaises(ValueError, a_1.cross_product, c_1)

    def test_dot_product(self):
        """
        Test the dot product
        """
        v_1 = geometry.Vector([1, 3, -5])
        v_2 = geometry.Vector([4, -2, -1])
        self.assertEqual(v_1.dot_product(v_2), 3)
        self.assertEqual(v_2.dot_product(v_1), 3)
        v_3 = geometry.Vector([1, 2])
        self.assertRaises(ValueError, v_3.dot_product, v_1)
        a_1 = geometry.Vector([2, 0, 0])
        a_2 = geometry.Vector([0, 1, 0])
        self.assertEqual(a_1.dot_product(a_2), 0)

    def test_triple_product(self):
        """
        Test the triple product
        """
        v_1 = geometry.Vector([1, 0, 0])
        v_2 = geometry.Vector([0, 2, 0])
        v_3 = geometry.Vector([0, 0, 3])
        v_b = geometry.Vector([1, 2])
        self.assertRaises(ValueError, v_1.triple_product, v_2, v_b)
        self.assertRaises(ValueError, v_2.triple_product, v_b, v_1)
        self.assertRaises(ValueError, v_b.triple_product, v_1, v_2)
        self.assertEqual(v_1.triple_product(v_2, v_3), 6)
        v_4 = geometry.Vector([3, 4, 0])
        self.assertEqual(v_1.triple_product(v_2, v_4), 0)

class PointTest(unittest.TestCase):
    """
    Test cases for Point
    """
    def test_str(self):
        """
        Test that the format is right
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3], 'vectorExample'), 'pointExample')
        str_1 = str(p_1)
        str_2 = "pointExample[1.0, 2.0, 3.0]"
        self.assertEqual(str_1, str_2)

    def test_add(self):
        """
        Test adding a vector to a point
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3]))
        p_2 = geometry.Point(geometry.Vector([3, 4, 5]))
        v_1 = geometry.Vector([2, 2, 2])
        self.assertRaises(TypeError, p_1.__add__, 1)
        self.assertRaises(TypeError, p_1.__add__, p_2)
        p_3 = p_1 + v_1
        self.assertEqual(p_2.position, p_3.position)

    def test_sub(self):
        """
        Test sub a Point to another Point
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3]))
        p_2 = geometry.Point(geometry.Vector([3, 4, 5]))
        v_1 = geometry.Vector([2, 2, 2])
        v_2 = p_2 - p_1
        self.assertEqual(v_1.coordinates, v_2.coordinates)

class SegmentTest(unittest.TestCase):
    """
    Test cases for Segment
    """
    def test_str(self):
        """
        Test that the format is right
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3], 'vector1Example'), 'point1Ex')
        p_2 = geometry.Point(geometry.Vector([2, 4, 6], 'vector2Example'), 'point2Ex')
        s_1 = geometry.Segment(p_1, p_2, 'segmentExample')
        str_1 = str(s_1)
        str_2 = "segmentExample:point1Ex[1.0, 2.0, 3.0]--point2Ex[2.0, 4.0, 6.0]"
        self.assertEqual(str_1, str_2)

    def test_vector(self):
        """
        Test that we get the vector direction of the segment
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3], 'vector1Example'), 'point1Ex')
        p_2 = geometry.Point(geometry.Vector([2, 4, 7], 'vector2Example'), 'point2Ex')
        s_1 = geometry.Segment(p_1, p_2, 'segmentExample')
        v_1 = s_1.vector()
        v_2 = geometry.Vector([1, 2, 4])
        self.assertEqual(v_1.coordinates, v_2.coordinates)

    def test_midpoint(self):
        """
        Test the midpoint function
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3]))
        p_2 = geometry.Point(geometry.Vector([3, 4, 5]))
        s_1 = geometry.Segment(p_1, p_2)
        p_mid = s_1.midpoint()
        p_3 = geometry.Point(geometry.Vector([2, 3, 4]))
        self.assertEqual(p_mid.position, p_3.position)

class ContourTest(unittest.TestCase):
    """
    Test cases for Contour
    """
    def test_str(self):
        """
        Test that the format is right
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3]), 'point1')
        p_2 = geometry.Point(geometry.Vector([3, 4, 5]), 'point2')
        p_3 = geometry.Point(geometry.Vector([0, 0, 0]), 'point3')
        s_1 = geometry.Segment(p_1, p_2, 'segment1')
        s_2 = geometry.Segment(p_2, p_3, 'segment2')
        s_3 = geometry.Segment(p_3, p_1, 'segment3')
        contour = geometry.Contour(name='contour1')
        contour.append(s_1)
        contour.append(s_2)
        contour.append(s_3)
        str_1 = str(contour)
        str_2 = ("contour1:\n"
                 "segment1:point1[1.0, 2.0, 3.0]--point2[3.0, 4.0, 5.0]\n"
                 "segment2:point2[3.0, 4.0, 5.0]--point3[0.0, 0.0, 0.0]\n"
                 "segment3:point3[0.0, 0.0, 0.0]--point1[1.0, 2.0, 3.0]")
        self.assertEqual(str_1, str_2)

    def test_append(self):
        """
        Test to add segment to list
        """
        p_1 = geometry.Point(geometry.Vector([1, 2, 3]), 'point1')
        p_2 = geometry.Point(geometry.Vector([3, 4, 5]), 'point2')
        s_1 = geometry.Segment(p_1, p_2, 'segment1')
        contour = geometry.Contour(name='contour1')
        contour.append(s_1)
        self.assertEqual(len(contour.segments), 1)
        self.assertEqual(contour.segments[0].uid, s_1.uid)

    def test_delete(self):
        """
        Test to remove a segment from the list
        """
        seg = geometry.Segment()
        contour = geometry.Contour()
        for _ in range(5):
            contour.append(geometry.Segment())
        contour.append(seg)
        self.assertEqual(len(contour.segments), 6)
        contour.delete(seg)
        self.assertEqual(len(contour.segments), 5)
        uids = [e.uid for e in contour.segments]
        self.assertFalse(seg.uid in uids)

    def test_search_by_uid(self):
        """
        Test the search
        """
        seg = geometry.Segment()
        contour = geometry.Contour()
        for _ in range(5):
            contour.append(geometry.Segment())
        contour.append(seg)
        result = contour.search_by_uid(seg.uid)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].uid, seg.uid)
        result = contour.search_by_uid('not a uid')
        self.assertFalse(result)

    def test_search_by_name(self):
        """
        Test the search
        """
        seg = geometry.Segment(name='itsaschmilblick')
        contour = geometry.Contour()
        for i in range(5):
            contour.append(geometry.Segment(name='segment' + str(i)))
        contour.append(seg)
        result = contour.search_by_name('isatschlimbickl')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].uid, seg.uid)
        result = contour.search_by_name('segment')
        self.assertEqual(len(result), 5)

    def test_is_closed(self):
        """
        Test that the check that the contour is closed is working
        """
        p_1 = geometry.Point(geometry.Vector([0, 1, 1]))
        p_2 = geometry.Point(geometry.Vector([0, 1, 2]))
        p_3 = geometry.Point(geometry.Vector([0, 2, 2]))
        p_4 = geometry.Point(geometry.Vector([0, 2, 1]))
        s_1 = geometry.Segment(p_1, p_2)
        s_2 = geometry.Segment(p_2, p_3)
        s_3 = geometry.Segment(p_3, p_4)
        s_4 = geometry.Segment(p_4, p_1)
        c_1 = geometry.Contour()
        c_1.append(s_1)
        c_1.append(s_2)
        c_1.append(s_3)
        self.assertFalse(c_1.is_closed())
        c_1.append(s_4)
        self.assertTrue(c_1.is_closed())

    def test_is_coplanar(self):
        """
        Test that the check that the contour is flat on a plan is working
        """
        p_1 = geometry.Point(geometry.Vector([0, 1, 1]))
        p_2 = geometry.Point(geometry.Vector([0, 1, 2]))
        p_3 = geometry.Point(geometry.Vector([0, 2, 2]))
        p_4 = geometry.Point(geometry.Vector([0, 2, 1]))
        p_5 = geometry.Point(geometry.Vector([1, 3, 4]))
        s_1 = geometry.Segment(p_1, p_2)
        s_2 = geometry.Segment(p_2, p_3)
        s_3 = geometry.Segment(p_3, p_4)
        s_4 = geometry.Segment(p_4, p_5)
        s_5 = geometry.Segment(p_5, p_1)
        c_1 = geometry.Contour()
        c_1.append(s_1)
        c_1.append(s_2)
        self.assertTrue(c_1.is_coplanar())
        c_1.append(s_3)
        self.assertTrue(c_1.is_coplanar())
        c_1.append(s_4)
        self.assertFalse(c_1.is_coplanar())
        c_1.append(s_5)
        self.assertFalse(c_1.is_coplanar())

class ModuleTest(unittest.TestCase):
    """
    Test cases for function of module not in classes
    """
    def test_parallelogram(self):
        """
        Test the parallelogram constructor
        """
        p_1 = geometry.Point(geometry.Vector([0, 1, 1]))
        p_2 = geometry.Point(geometry.Vector([0, 1, 2]))
        p_3 = geometry.Point(geometry.Vector([0, 2, 2]))
        p_4 = geometry.Point(geometry.Vector([0, 2, 1]))
        s_1 = geometry.Segment(p_1, p_2)
        s_2 = geometry.Segment(p_2, p_3)
        s_3 = geometry.Segment(p_3, p_4)
        s_4 = geometry.Segment(p_4, p_1)
        c_1 = geometry.Contour()
        c_1.append(s_1)
        c_1.append(s_2)
        c_1.append(s_3)
        c_1.append(s_4)
        c_2 = geometry.parallelogram(geometry.Point(geometry.Vector([0, 1, 1])),
                                     geometry.Vector([0, 0, 1]),
                                     geometry.Vector([0, 1, 0]))
        self.assertEqual(str(c_1), str(c_2))

if __name__ == '__main__':
    unittest.main()
