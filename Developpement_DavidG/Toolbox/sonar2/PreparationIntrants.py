# -*- coding: utf-8 -*-

"""
/***************************************************************************
 CreationplacetteMesurable
                                 A QGIS plugin
 Confection de plans de sondage - DIF
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-07-13
        copyright            : (C) 2021 by MFFP - DIF
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

__author__ = 'MFFP - DIF'
__date__ = '2021-07-13'
__copyright__ = '(C) 2021 by MFFP - DIF'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import *
import os
import processing
from processing.tools import dataobjects
from qgis.PyQt.QtGui import QIcon
import line_profiler
import geopandas as gpd
profile = line_profiler.LineProfiler()

def copyCeToGpkg(ce, gpkg, nomCouche):

    # faire un layer avec la string ce
    if isinstance(ce, str):
        couche = QgsVectorLayer(ce, 'lyr', 'ogr')
    else:
        couche = ce


    # Option de sauvegarde
    options = QgsVectorFileWriter.SaveVectorOptions()

    # J'enleve l'extension
    gpkg = gpkg.replace(".gpkg", "")

    options.driverName = 'GPKG'
    options.layerName = nomCouche

    # Transférer la ce de la gdb vers le GeoPackage
    QgsVectorFileWriter.writeAsVectorFormat(couche, gpkg, options)

    sortie = gpkg + ".gpkg" + '|' + 'layername=' + nomCouche

    return sortie

class PreparationIntrantsAlgorithm(QgsProcessingAlgorithm):
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

    UniteSondage = 'UniteSondage'
    uniteSondage = 'uniteSondage'
    DossierIntrants = 'DossierIntrants'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # Unité de sondage (CE)
        self.addParameter(QgsProcessingParameterFeatureSource(self.UniteSondage, self.tr('Unité de sondage en entrée'),
                                                              [QgsProcessing.TypeVectorAnyGeometry]))

        # parametre de l'unité de sondage
        self.addParameter(
            QgsProcessingParameterString(
                self.uniteSondage,
                ('Unité de sondage'),
                defaultValue="1415CE",
                optional=False)
        )

        # Parametre Dossier Intrants
        self.addParameter(QgsProcessingParameterFile
                          (self.DossierIntrants,'Dossier des intrants',
                                                     behavior=QgsProcessingParameterFile.Folder,
                                                     defaultValue=None))
    @profile
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        feedback.pushInfo("\nDébut du processus\n")

        # unité de sondage
        path_us = self.parameterAsVectorLayer(parameters,  self.UniteSondage, context)

        # numéro de l'unité de sondage
        us = self.parameterAsString(parameters, self.uniteSondage, context)

        # Parametres Dossier Intrants
        wd_intrants = self.parameterAsString(parameters,  self.DossierIntrants, context)

        feedback.pushInfo("\nVous traité l'unité de sondage : {0}\n".format(us))

        # Permet d'ignorer les erreurs de geometries
        noCheckGeom = dataobjects.createContext()
        noCheckGeom.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)

        # Liste des intrants sur le réseau (DDE et autres)
        # path_PeupForestiers_reseau =

        path_PentesNum_reseau = r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Classe_de_pente_numerique/CLASSES_DE_PENTE_NUMERIQUE_S/FGDB_GEO/CPN_PROV/CPN_PROV.gdb|layername=CPN_PROV"

        path_HydroLin_reseau = r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/HYDROGRAPHIE_LINEAIRE_BDTQ_20K_L/FGDB_GEO/HL20_PROV/HL20_PROV.gdb|layername=BDTQ_20K_HYDRO_LO"

        path_VoieFerree_reseau = r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/VOIE_COMM_LINEAIRE_BDTQ_20K_L/FGDB_GEO/VCL_BDTQ_20K/VCL_BDTQ_20K.gdb|layername=BDTQ_20K_VOIE_COMMU_LO"

        path_PEP_reseau = r"//vulcain/raigeop/Depot_Dde/Produits_IEQM/Placettes_echantillons/PEP.gpkg|layername=placette"

        path_ponc_reseau = r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/BATIMENT_PONCTUEL_BDTQ_20K_P/FGDB_GEO/BATP_PROV/BATP_PROV.gdb|layername=BDTQ_20K_BATIM_PO"

        path_BatiLin_reseau=r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/BATIMENT_LINEAIRE_BDTQ_20K_L/FGDB_GEO/BATL_PROV/BATL_PROV.gdb|layername=BDTQ_20K_BATIM_LO"

        path_BatiSur_reseau=r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/BATIMENT_SURFACIQUE_BDTQ_20K_S/FGDB_GEO/BATS_PROV/BATS_PROV.gdb|layername=BDTQ_20K_BATIM_SO"

        path_EquipPonc_reseau=r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/EQUIPEMENT_PONCTUEL_BDTQ_20K_P/FGDB_GEO/EQP_PROV/EQP_PROV.gdb|layername=BDTQ_20K_EQUIP_PO"

        path_EquipLin_reseau=r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/EQUIPEMENT_LINEAIRE_BDTQ_20K_L/FGDB_GEO/EQL_PROV/EQL_PROV.gdb|layername=BDTQ_20K_EQUIP_LO"

        path_EquipSur_reseau=r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Reference_geographique_Quebec/BDTQ_20K_a_jour/EQUIPEMENT_SURFACIQUE_BDTQ_20K_S/FGDB_GEO/EQS_PROV/EQS_PROV.gdb|layername=BDTQ_20K_EQUIP_SO"

        path_AffecPonc_reseau=r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Utilisation_du_territoire/Usage_forestier/USAGE_FORESTIER_PONCTUEL_P/FGDB_CCL/UFP_PROV/UFP_PROV.gdb|layername=DDE_UFZ_USAGE_FORES_VUE_P"

        path_AffecLin_reseau=r"//vulcain/raigeop/Depot_Dde/Catalogue_du_systeme_DDE/Couches_de_donnees/Utilisation_du_territoire/Usage_forestier/USAGE_FORESTIER_LINEAIRE_L/FGDB_CCL/UFL_PROV/UFL_PROV.gdb|layername=DDE_UFZ_USAGE_FORES_VUE_L"

        # path_Feux_reseau=

        # path_PertMaj_reseau=

        # path_Interv_reseau=

        # path_Planif_reseau=


        # liste des intrants
        # listeIntrantsRes = [path_PeupForestiers_reseau,path_PentesNum_reseau,path_HydroLin_reseau,path_VoieFerree_reseau,path_PEP_reseau,
        #                     path_ponc_reseau,path_BatiLin_reseau,path_BatiSur_reseau,path_EquipPonc_reseau,path_EquipLin_reseau,path_EquipSur_reseau,
        #                     path_AffecPonc_reseau,path_AffecLin_reseau,path_Feux_reseau,path_PertMaj_reseau,path_Interv_reseau,path_Planif_reseau]

        listeIntrantsRes = [path_PentesNum_reseau,path_HydroLin_reseau,path_VoieFerree_reseau,path_PEP_reseau,
                            path_ponc_reseau,path_BatiLin_reseau,path_BatiSur_reseau,path_EquipPonc_reseau,path_EquipLin_reseau,path_EquipSur_reseau,
                            path_AffecPonc_reseau,path_AffecLin_reseau]


        # #Ce sont des intrants préparés hors de l'outil
        # path_us             = os.path.join(wd_intrants, "US_{0}.shp".format(us))  #Robin
        # path_ParamBuffers   = os.path.join(wd_intrants,  "Parametres", "BUFFER_template.csv")# SONDAGE
        # path_chemins        = os.path.join(wd_intrants, "CHEMIN_SONAR_{0}.shp".format(us)) # SONDAGE
        # path_geocodes       = os.path.join(wd_intrants, "LIST_GEOC_{0}.shp".format(us)) # PHILIPPE MORIN
        # path_masque         = os.path.join(wd_intrants, "MASQUE_{0}.shp".format(us))# SONDAGE
        # path_SIP            = os.path.join(wd_intrants, "CFETBFEC_08664_SIP.shp")# Pour l'intant on laisse desactivé


        # Liste des intrant local (gpkg)
        # gpkg des intrants
        gpkg = os.path.join(wd_intrants,"SONAR2_Intrants.gpkg")


        path_PeupForestiers = 'ogr:dbname=\'{0}\' table=\"DDE_20K_PEU_FOR_ORI_TRV_VUE_SE_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_PentesNum = 'ogr:dbname=\'{0}\' table=\"DDE_20K_CLA_PEN_VUE_SE_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_HydroLin = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_HYDRO_LO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_VoieFerree = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_VOIE_COMMU_LO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_PEP = 'ogr:dbname=\'{0}\' table=\"DDE_20K_PEP_VUE_PE_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_ponc = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_BATIM_PO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_BatiLin = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_BATIM_LO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_BatiSur = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_BATIM_SO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_EquipPonc = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_EQUIP_PO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_EquipLin = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_EQUIP_LO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_EquipSur = 'ogr:dbname=\'{0}\' table=\"BDTQ_20K_EQUIP_SO_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_AffecPonc = 'ogr:dbname=\'{0}\' table=\"DDE_UFZ_20K_USAGE_FOR_VUE_PE_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_AffecLin = 'ogr:dbname=\'{0}\' table=\"DDE_UFZ_20K_USAGE_FOR_VUE_LE_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_Feux = 'ogr:dbname=\'{0}\' table=\"DDE_20K_FEUX_MAJ_TRV_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_PertMaj = 'ogr:dbname=\'{0}\' table=\"DDE_20K_AUTRE_PERTU_MAJ_TRV_{1}\" (geom) sql='.format(gpkg,us)#OUTIL
        path_Interv = 'ogr:dbname=\'{0}\' table=\"INTERVENTION_{1}\" (geom) sql='.format(gpkg,us)#YVAN
        path_Planif = 'ogr:dbname=\'{0}\' table=\"PLAN_{1}\" (geom) sql='.format(gpkg,us)#YVAN
        path_BufferIn = 'ogr:dbname=\'{0}\' table=\"us_bufin_{1}_2025m\" (geom) sql='.format(gpkg,us)#OUTIL


        # Liste des intrants nécessaire pour l'outil de création de placettes mesurables
        # listeIntratns = [path_PeupForestiers,path_PentesNum,path_HydroLin,path_VoieFerree,path_PEP,path_ponc,path_BatiLin,path_BatiSur,
        #                  path_EquipPonc,path_EquipLin,path_EquipSur,path_AffecPonc,path_AffecLin,path_Feux,path_PertMaj,path_Interv,path_Planif,
        #                  ]

        listeIntrants = [path_PentesNum,path_HydroLin,path_VoieFerree,path_PEP,path_ponc,path_BatiLin,path_BatiSur,
                         path_EquipPonc,path_EquipLin,path_EquipSur,path_AffecPonc,path_AffecLin]

        # couches intermediaires
        path_us_buf_2km = '{0}|layername=us_buf_2km_{1}'.format(gpkg,us)

        # # copie l'us dans le geopackage
        # # Copie des peuplement dans le GPKG
        us_gpkg = 'us'
        copyCeToGpkg(path_us, gpkg, us_gpkg)


        # Faire le dissolve a qgis. Par contre, il faut auparavant que Robin s'assure qu'il n'est pas de trous.
        # Pour ce faire j'ai fait un extent de l'us et un clip dans arcmap et ca regle les problemes.
        # C'est comme si l'extration ce fait avec des tolerances tres petites. C'est pour ca que la couche est pleine de trous dans QGIS
        dissolve_us = processing.run("native:dissolve", {'INPUT':path_us,'FIELD':[],'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})["OUTPUT"]


        # faire la couche path_BufferIn
        buff_25 = processing.run("native:buffer", {'INPUT':dissolve_us,'DISTANCE':-25,
                                         'SEGMENTS':5,'END_CAP_STYLE':0,
                                         'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})["OUTPUT"]

        # faire la différence avec l'us et le buffer interne de 25 m
        processing.run("native:difference", {'INPUT':dissolve_us,'OVERLAY':buff_25,
                                             'OUTPUT': path_BufferIn})

        # faire un buffer de 2000m de l'US
        processing.run("native:buffer", {'INPUT':dissolve_us,'DISTANCE':2000,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,
                                         'DISSOLVE':False,'OUTPUT':'ogr:dbname=\'{0}\' table=\"us_buf_2km_{1}\" (geom) sql='.format(gpkg,us)})

        feedback.pushInfo("\n1. Faire les extractions")

        # récupérer la projection de l'US pour reprojeter les couches extraites
        ESPG = dissolve_us.crs().authid()

        # Faire les extractions
        i=0
        for li in listeIntrantsRes:
            j=i+1
            feedback.pushInfo("\n     1.{1}    Extraction par localisation: {0}".format(li,j))

            extract = processing.run("native:extractbylocation", {'INPUT':li,'PREDICATE':[0],
                                                        'INTERSECT':path_us_buf_2km,'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})["OUTPUT"]

            processing.run("native:reprojectlayer", {'INPUT':extract,'TARGET_CRS':QgsCoordinateReferenceSystem(ESPG),'OUTPUT':listeIntrants[i]})

            i+=1

        return {self.uniteSondage:us}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return '0 - Préparation des intrants'

    def icon(self):
        return QIcon(os.path.dirname(__file__) + '/image/preparation.png')

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
        return PreparationIntrantsAlgorithm()