# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CreerGpx
                                 A QGIS plugin
 Cette extension permet de creer un Gpx pour Garmin
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-03-27
        copyright            : (C) 2020 by David Gauthier - Mffp (DIF)
        email                : david.gauthier@mffp.gouv.qc.ca
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CreerGpx class from file CreerGpx.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Creer_Gpx import CreerGpx
    return CreerGpx(iface)
