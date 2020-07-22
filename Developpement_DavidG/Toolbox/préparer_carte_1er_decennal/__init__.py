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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'David Gauthier'
__date__ = '2020-07-13'
__copyright__ = '(C) 2020 by David Gauthier'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PreparerCarteDecennal class from file PreparerCarteDecennal.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .préparer_carte_1er_decennal import PreparerCarteDecennalPlugin
    return PreparerCarteDecennalPlugin()
