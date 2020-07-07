# -*- coding: utf-8 -*-

"""
/***************************************************************************
 FaireRaccDif
                                 A QGIS plugin
 Faire un racc dif
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-03-24
        copyright            : (C) 2020 by David Gauthier - MFFP (DIF)
        email                : david.gauthier@mffp.gouv.qc.ca
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

__author__ = 'David Gauthier - MFFP (DIF)'
__date__ = '2020-03-24'
__copyright__ = '(C) 2020 by David Gauthier - MFFP (DIF)'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import *


import shutil
import os

import processing
from QGIS_commun import conversionFormatVersGDB, conversionFormatVersGDBCMD,identifyNarrowPolygon


class FaireRaccDifAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    # Vous pouvez donner les noms que vous voulez.
    # Il faut les utiliser ici bas dans  "def initAlgorithm" et "processAlgorithm"

    INPUT_perm5pre = 'INPUT_perm5pre'
    INPUT_FOR = 'INPUT_FOR'
    RAC_DIF = 'RAC_DIF'



    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # parametre 1 INPUT FeatureSource
        self.addParameter(QgsProcessingParameterFeatureSource( self.INPUT_perm5pre,  self.tr('Périmetre préliminaire (perm5pre.shp)'),
                [QgsProcessing.TypeVectorAnyGeometry]))

        # parametre 2 INPUT FeatureSource
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT_FOR,self.tr('Classe dentité du fuseau forestier'),
                [QgsProcessing.TypeVectorAnyGeometry]))

        # parametre 2 OUTPUT VectorDestination
        self.addParameter(QgsProcessingParameterVectorDestination(self.RAC_DIF,
                self.tr('Racc_dif.shp')))

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """


        # Parametres
        # mettre le premier parametre (vector layer) comme input dans un object
        perm5pre = self.parameterAsVectorLayer(parameters, self.INPUT_perm5pre, context)

        # mettre le deuxieme parametre (vector layer) comme input dans un object
        ce_for = self.parameterAsVectorLayer(parameters, self.INPUT_FOR, context)

        # mettre le troisieme parametre (output Layer) comme output dans un object
        Racc_dif = self.parameterAsOutputLayer(parameters, self.RAC_DIF, context)

        # Dossier temp
        retrav = os.getenv('TEMP')

        # Faire un dossier pour les .shp qui seront transférés dans le dossier trm_pre
        trm_pre_tansfert = os.path.join(retrav, "trm_pre_transfert")

        if not os.path.exists(trm_pre_tansfert):
            os.mkdir(trm_pre_tansfert)
        else:
            pass


        # path du raccdif vide avec la bonne structure
        pathStrucShpVide = r"\\Sef1271a\F1271g\OutilsProdDIF\outils\ADG\Preparation_Contrats\prerequis"

        list_racc_dif = [os.path.join(pathStrucShpVide, "Racc_dif.dbf"),
                         os.path.join(pathStrucShpVide, "Racc_dif.prj"),
                         os.path.join(pathStrucShpVide, "Racc_dif.sbn"),
                         os.path.join(pathStrucShpVide, "Racc_dif.sbx"),
                         os.path.join(pathStrucShpVide, "Racc_dif.shp"),
                         os.path.join(pathStrucShpVide, "Racc_dif.shx")]

        for li in list_racc_dif:
            shutil.copy(li, trm_pre_tansfert)

        # liste des couches
        Rac_Dif_vide = os.path.join(trm_pre_tansfert, "Racc_dif.shp")



        ##### RAC_DIFF  #####################
        # faire la zone du Racc_dif, donc un buffer de 500 metre

        feedback.pushInfo("\n1- Faire le buffer de 500m\n")

        perm5pre_buff = processing.run("native:buffer",
                       {'INPUT': perm5pre, 'DISTANCE': 500, 'SEGMENTS': 5,
                        'END_CAP_STYLE': 1, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': False,
                        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT}, feedback=feedback)["OUTPUT"]

        feedback.pushInfo("\n2- Selection par location dans le fuseau forestier\n")

        # faire une selection location intersect  sur ForS5 pour générer le Racc_dif
        processing.run("native:selectbylocation",
                       {'INPUT': ce_for,
                        'PREDICATE': [0], 'INTERSECT': perm5pre_buff, 'METHOD': 0}, feedback=feedback)


        # copier la selection en memoire
        ce_for_select = processing.run("native:saveselectedfeatures", {'INPUT': ce_for, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT},
                                       feedback=feedback)["OUTPUT"]

        feedback.pushInfo("\n3- Dissolve de la selection\n")
        # Un dissolve de ma selection et apres je vais suppirmer les trous a l'interieur du dissolve.
        dissolve = processing.run("native:dissolve", {'INPUT': ce_for_select, 'FIELD': [], 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT},
                                  feedback=feedback)["OUTPUT"]

        feedback.pushInfo("\n4- Bouche les trous de du dissolve\n")
        # suppirmer les trous a l'interieur du dissolve
        newperm5trm = processing.run("native:deleteholes", {'INPUT':dissolve,'MIN_AREA':999999999,'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT},
                                     feedback=feedback)["OUTPUT"]

        feedback.pushInfo("\n5- Refaire la selection par location dans le fuseau forestier avec le nouveau perimetre (dissolve)\n")
        # refaire une selection WITHIN avec le nouveau perimetre pas de trou
        processing.run("native:selectbylocation", {'INPUT': ce_for, 'PREDICATE': [6],'INTERSECT': newperm5trm, 'METHOD': 0},
                       feedback=feedback)

        # Mettre un output dans un object pour l'utiliser par la suite
        output = processing.run("native:saveselectedfeatures", {'INPUT': ce_for, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT},
                                 feedback=feedback)["OUTPUT"]

        feedback.pushInfo("\n6- Copier la selection dans une couche vide\n")
        # Faire un append dans une couche vide avec la bonne structure
        processing.run("Append dans une classe dentité:Append",
                       {'SOURCE_LAYER':output,
                        'SOURCE_FIELD':None,'TARGET_LAYER':Rac_Dif_vide,
                        'TARGET_FIELD':None,'ACTION_ON_DUPLICATE':0},feedback=feedback)



        # trouver le path d'une couche en Input dans QGIS (c une string)
        path_INPUT_perm5pre = self.parameterDefinition('INPUT_perm5pre').valueAsPythonString(
            parameters['INPUT_perm5pre'], context)

        # Enleve "/Perm5pre.shp" de la string pour avoir seulement le path du shp
        path_INPUT_perm5pre = path_INPUT_perm5pre.replace("/Perm5pre.shp'", "")

        fus = os.path.basename(path_INPUT_perm5pre)
        # fus = fus.replace("'","")

        feedback.pushInfo("\n7- Reprojection du Racc_dif dans le fuseau {}".format(fus))
        if fus == '04':
            crs = 'EPSG:32184'
        elif fus == '05':
            crs = 'EPSG:32185'
        elif fus == '06':
            crs = 'EPSG:32186'
        elif fus == '07':
            crs = 'EPSG:32187'
        elif fus == '08':
            crs = 'EPSG:32188'
        elif fus == '09':
            crs = 'EPSG:32189'
        elif fus == '10':
            crs = 'EPSG:32110'
        else:
           raise QgsProcessingException("\nLe dossier parent du Perm5pre.shp ne contient pas de # de fuseau\n")


        processing.run("native:reprojectlayer", {'INPUT':Rac_Dif_vide,
                                                 'TARGET_CRS':QgsCoordinateReferenceSystem(crs),
                                                 'OUTPUT':Racc_dif},feedback=feedback)




        return {self.RAC_DIF: Racc_dif}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '5 - Faire un Racc dif (optionnel)'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return FaireRaccDifAlgorithm()
