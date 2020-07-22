# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PreparerCarteDecennal
                                 A QGIS plugin
 Préparer carte 1er décennal
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-07-13
        copyright            : (C) 2020 by David Gauthier
        email                : david.gauthier@mffp.gouv.qv.ca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'David Gauthier'
__date__ = '2020-07-13'
__copyright__ = '(C) 2020 by David Gauthier'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from .préparer_carte_1er_decennal_algorithm import PreparerCarteDecennalAlgorithm
import os
from qgis.PyQt.QtGui import QIcon

class PreparerCarteDecennalProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(PreparerCarteDecennalAlgorithm())
        # add additional algorithms here
        # self.addAlgorithm(MyOtherAlgorithm())

    def icon(self):
        return QIcon(os.path.dirname(__file__) + '/image/map.png')


    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'Préparer carte 1er décennal'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('Préparer carte 1er décennal')

    # def icon(self):
    #     """
    #     Should return a QIcon which is used for your provider inside
    #     the Processing toolbox.
    #     """
    #     return QgsProcessingProvider.icon(self)

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
