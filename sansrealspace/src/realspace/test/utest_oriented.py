"""
    Unit tests for specific oriented models
    @copyright: University of Tennessee, for the DANSE project
"""

import unittest, math, sys

# Disable "missing docstring" complaint
# pylint: disable-msg=C0111
# Disable "too many methods" complaint 
# pylint: disable-msg=R0904 
# Disable "could be a function" complaint 
# pylint: disable-msg=R0201
# pylint: disable-msg=W0702

try:
    import VolumeCanvas
    print "Testing local version"
except:
    print sys.exc_value
    #testing the version that is working on
    print "Testing installed version"
    import sans.realspace.VolumeCanvas as VolumeCanvas
 

class TestSphere(unittest.TestCase):
    """ Tests for oriented (2D) systems """
        
    def setUp(self):
        """
            Set up canvas
        """
        from sans.models.SphereModel import SphereModel
        self.model = VolumeCanvas.VolumeCanvas()
    
        handle = self.model.add('sphere')
        
        radius = 10
        density = .1
        
        ana = SphereModel()
        ana.setParam('scale', 1.0)
        ana.setParam('contrast', 1.0)
        ana.setParam('background', 0.0)
        ana.setParam('radius', radius)
        self.ana = ana
        
        self.model.setParam('lores_density', density)
        self.model.setParam('%s.radius' % handle, radius)
        self.model.setParam('scale' , 1.0)
        self.model.setParam('%s.contrast' % handle, 1.0)
        self.model.setParam('background' , 0.0)
        
        
    def testdefault(self):
        """ Testing sphere """
        # Default orientation
        ana_val = self.ana.runXY([0.1, 0.1])
        sim_val = self.model.getIq2D(0.1, 0.1)
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.1 )
        
class TestCylinder(unittest.TestCase):
    """ Tests for oriented (2D) systems """
        
    def setUp(self):
        """ Set up cylinder model """
        from sans.models.CylinderModel import CylinderModel
        radius = 5
        length = 40
        density = 20
    
        # Analytical model
        self.ana = CylinderModel()
        self.ana.setParam('scale', 1.0)
        self.ana.setParam('contrast', 1.0)
        self.ana.setParam('background', 0.0)
        self.ana.setParam('radius', radius)
        self.ana.setParam('length', length)
    
        # Simulation model
        self.model = VolumeCanvas.VolumeCanvas()
        self.handle = self.model.add('cylinder')
        self.model.setParam('lores_density', density)
        self.model.setParam('%s.radius' % self.handle, radius)
        self.model.setParam('%s.length' % self.handle, length)
        self.model.setParam('scale' , 1.0)
        self.model.setParam('%s.contrast' % self.handle, 1.0)
        self.model.setParam('background' , 0.0)
    
    def testalongY(self):
        """ Testing cylinder along Y axis """
        self.ana.setParam('cyl_theta', math.pi/2.0)
        self.ana.setParam('cyl_phi', math.pi/2.0)
        
        self.model.setParam('%s.orientation' % self.handle, [0,0,0])
        
        ana_val = self.ana.runXY([0.1, 0.2])
        sim_val = self.model.getIq2D(0.1, 0.2)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )
        
    def testalongZ(self):
        """ Testing cylinder along Z axis """
        self.ana.setParam('cyl_theta', 0)
        self.ana.setParam('cyl_phi', 0)
        
        self.model.setParam('%s.orientation' % self.handle, [90,0,0])
        
        ana_val = self.ana.runXY([0.1, 0.2])
        sim_val = self.model.getIq2D(0.1, 0.2)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )
        
    def testalongX(self):
        """ Testing cylinder along X axis """
        self.ana.setParam('cyl_theta', 1.57)
        self.ana.setParam('cyl_phi', 0)
        
        self.model.setParam('%s.orientation' % self.handle, [0,0,90])
        
        ana_val = self.ana.runXY([0.1, 0.2])
        sim_val = self.model.getIq2D(0.1, 0.2)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )
        
class TestEllipsoid(unittest.TestCase):
    """ Tests for oriented (2D) systems """
        
    def setUp(self):
        """ Set up ellipsoid """
        from sans.models.EllipsoidModel import EllipsoidModel
        
        radius_a = 60
        radius_b = 10
        density = 30
        
        self.ana = EllipsoidModel()
        self.ana.setParam('scale', 1.0)
        self.ana.setParam('contrast', 1.0)
        self.ana.setParam('background', 0.0)
        self.ana.setParam('radius_a', radius_a)
        self.ana.setParam('radius_b', radius_b)

       
        canvas = VolumeCanvas.VolumeCanvas()
        canvas.setParam('lores_density', density)
        self.handle = canvas.add('ellipsoid')
        canvas.setParam('%s.radius_x' % self.handle, radius_a)
        canvas.setParam('%s.radius_y' % self.handle, radius_b)
        canvas.setParam('%s.radius_z' % self.handle, radius_b)
        canvas.setParam('scale' , 1.0)
        canvas.setParam('%s.contrast' % self.handle, 1.0)
        canvas.setParam('background' , 0.0)
        self.canvas = canvas        

    def testalongX(self):
        """ Testing ellipsoid along X """
        self.ana.setParam('axis_theta', 1.57)
        self.ana.setParam('axis_phi', 0)
        
        self.canvas.setParam('%s.orientation' % self.handle, [0,0,0])
        
        ana_val = self.ana.runXY([0.1, 0.2])
        sim_val = self.canvas.getIq2D(0.1, 0.2)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )

    def testalongZ(self):
        """ Testing ellipsoid along Z """
        self.ana.setParam('axis_theta', 0)
        self.ana.setParam('axis_phi', 0)
        
        self.canvas.setParam('%s.orientation' % self.handle, [0,90,0])
        
        ana_val = self.ana.runXY([0.1, 0.2])
        sim_val = self.canvas.getIq2D(0.1, 0.2)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )

    def testalongY(self):
        """ Testing ellipsoid along Y """
        self.ana.setParam('axis_theta', math.pi/2.0)
        self.ana.setParam('axis_phi', math.pi/2.0)
        
        self.canvas.setParam('%s.orientation' % self.handle, [0,0,90])
        
        ana_val = self.ana.runXY([0.05, 0.15])
        sim_val = self.canvas.getIq2D(0.05, 0.15)
        #print ana_val, sim_val, sim_val/ana_val
        
        try:
            self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )
        except:
            print ana_val, sim_val, sim_val/ana_val
            raise sys.exc_type, sys.exc_value

class TestCoreShell(unittest.TestCase):
    """ Tests for oriented (2D) systems """
        
    def setUp(self):
        """ Set up zero-SLD-average core-shell model """
        from sans.models.CoreShellModel import CoreShellModel
        
        radius = 15
        thickness = 5
        density = 20
        
        core_vol = 4.0/3.0*math.pi*radius*radius*radius
        self.outer_radius = radius+thickness
        shell_vol = 4.0/3.0*math.pi*self.outer_radius*self.outer_radius*self.outer_radius - core_vol
        self.shell_sld = -1.0*core_vol/shell_vol

        self.density = density
           
        # Core-shell
        sphere = CoreShellModel()
        # Core radius
        sphere.setParam('radius', radius)
        # Shell thickness
        sphere.setParam('thickness', thickness)
        sphere.setParam('core_sld', 1.0)
        sphere.setParam('shell_sld', self.shell_sld)
        sphere.setParam('solvent_sld', 0.0)
        sphere.setParam('background', 0.0)
        sphere.setParam('scale', 1.0)
        self.ana = sphere
       
        canvas = VolumeCanvas.VolumeCanvas()        
        canvas.setParam('lores_density', self.density)
        
        handle = canvas.add('sphere')
        canvas.setParam('%s.radius' % handle, self.outer_radius)
        canvas.setParam('%s.contrast' % handle, self.shell_sld)
       
        handle2 = canvas.add('sphere')
        canvas.setParam('%s.radius' % handle2, radius)
        canvas.setParam('%s.contrast' % handle2, 1.0)
               
        canvas.setParam('scale' , 1.0)
        canvas.setParam('background' , 0.0)
        self.canvas = canvas 
                   
    def testdefault(self):
        """ Testing default core-shell orientation """
        ana_val = self.ana.runXY([0.1, 0.2])
        sim_val = self.canvas.getIq2D(0.1, 0.2)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )

class TestRunMethods(unittest.TestCase):
    """ Tests run methods for oriented (2D) systems """

    def setUp(self):
        """ Set up ellipsoid """
        from sans.models.EllipsoidModel import EllipsoidModel
        
        radius_a = 10
        radius_b = 15
        density = 1
        
        self.ana = EllipsoidModel()
        self.ana.setParam('scale', 1.0)
        self.ana.setParam('contrast', 1.0)
        self.ana.setParam('background', 0.0)
        self.ana.setParam('radius_a', radius_a)
        self.ana.setParam('radius_b', radius_b)

       
        canvas = VolumeCanvas.VolumeCanvas()
        canvas.setParam('lores_density', density)
        self.handle = canvas.add('ellipsoid')
        canvas.setParam('%s.radius_x' % self.handle, radius_a)
        canvas.setParam('%s.radius_y' % self.handle, radius_b)
        canvas.setParam('%s.radius_z' % self.handle, radius_b)
        canvas.setParam('scale' , 1.0)
        canvas.setParam('%s.contrast' % self.handle, 1.0)
        canvas.setParam('background' , 0.0)
        self.canvas = canvas     
           
        self.ana.setParam('axis_theta', 1.57)
        self.ana.setParam('axis_phi', 0)
        
        self.canvas.setParam('%s.orientation' % self.handle, [0,0,0])
        

    def testRunXY_List(self):
        """ Testing ellipsoid along X """
        ana_val = self.ana.runXY([0.1, 0.2])
        sim_val = self.canvas.runXY([0.1, 0.2])
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )

    def testRunXY_float(self):
        """ Testing ellipsoid along X """
        ana_val = self.ana.runXY(0.1)
        sim_val = self.canvas.runXY(0.1)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )

    def testRun_float(self):
        """ Testing ellipsoid along X """
        ana_val = self.ana.run(0.1)
        sim_val = self.canvas.run(0.1)
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )

    def testRun_list(self):
        """ Testing ellipsoid along X """
        ana_val = self.ana.run([0.1, 33.0])
        sim_val = self.canvas.run([0.1, 33.0])
        #print ana_val, sim_val, sim_val/ana_val
        
        self.assert_( math.fabs(sim_val/ana_val-1.0)<0.05 )

          


if __name__ == '__main__':
    unittest.main()        