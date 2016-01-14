# physicalbody.py
#
# Implements the physical body class that stores the mass and moment of inertia
# of the body
#

from numpy import float_, zeros, array

from armech.graphics.graphicalbody import GraphicalBody


class PhysicalBody(GraphicalBody):

    def __init__(self):
        """
        Create a physical body object that has a mass and a moment of inertia
        :return obj: PhysicalBody object
        """
        
        # Initialize super class
	super(PhysicalBody, self).__init__()
        
        # Initialize values
        self.is_physical = False
        self.mass = float_(None)
        self.center_of_mass = zeros(3, 1)
        self.inertia_matrix = zeros(3, 3)

    def set_physics(self, mass, center_of_mass, 
                    momements_of_inertia, products_of_inertia):
       """
       Sets the physical properties of the body
       :param mass: Mass of the body (kg)
       :param center_of_mass: distance from the body origin to the center
       of mass
       :param moments_of_inertia: 3 element array of the x, y and bz moments
       of inertia (Ixx, Iyy, Izz)
       :param products_of_inertia: 3 element array of the products of inertia
       (Iyz, Ixz, Ixy)
       """
  
       # Set values
       self.mass = mass
       self.center_of_mass = center_of_mass
       self.inertia_matrix = array([
           [moment_of_inertia[0], product_of_inertia[0], product_of_inertia[1]],
           [product_of_inertia[0], moment_of_inertia[1], product_of_inertia[2]],
           [product_of_inertia[1], product_of_inertia[2], moment_of_inertia[3]],
       ])

      # Enable dynamics
      self.is_physical = True



