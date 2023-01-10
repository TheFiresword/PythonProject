import random

from CoreModules.MapManagement import mapManagementLayer as overlay
import CoreModules.BuildingsManagement.buildingsManagementBuilding as building
import CoreModules.BuildingsManagement.buildingsManagementRoad as roadoverlay
import CoreModules.TileManagement.tileManagementElement as element
import Services.servicesGlobalVariables as globalVar


class MapLogic:
    def __init__(self):
        # Booléen qui dit si la map est affichée ou pas
        self.active = True

        # Remplissage de chaque layer de la map
        """
        !!!!!!!!!! IMPORTANT """  # POUR PLACER UN ELEMENT DANS UN LAYER, IL FAUT LE CREER ET PAS JUSTE COPIER UN
        # ELEMENT PRECEDEMMENT CREE !!!!!!!!!! L'opérateur = en python est un monstre impitoyable qui m'a arraché les
        # cheveux

        # -------------------------------------------------------------------------------------------------------------#
        # GRASS
        self.grass_layer = overlay.Layer(globalVar.LAYER1)

        possible_grass = ["00079", "yellow", "00082", "normal", "yellow", "00091", "buisson", "00114", "00094",
                          "00027", "00070", "00221", "00274", "00239", "00081", "00244"]

        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                random_version = random.choice(possible_grass)
                my_grass = element.Element(self.grass_layer, globalVar.LAYER1, random_version)
                self.grass_layer.set_cell(i, j, my_grass)

        # -------------------------------------------------------------------------------------------------------------#
        # HILLS
        self.hills_layer = overlay.Layer(globalVar.LAYER2)

        possible_1_cell_hills = ["small-mountain1", "small-mountain2", "small-mountain3", "small-mountain4",
                                 "small-mountain5", "small-mountain6", "small-mountain7", "small-mountain8"]

        possible_2_cell_hills = ["big-mountain1", "big-mountain2", "big-mountain3"]

        possible_3_cell_hills = ["geant-mountain1", "geant-mountain2"]

        for i in range(0, int(globalVar.TILE_COUNT * 2 / 5)):
            random_1_cell_version = random.choice(possible_1_cell_hills)
            random_2_cell_version = random.choice(possible_2_cell_hills)
            random_3_cell_version = random.choice(possible_3_cell_hills)

            second_random_version = random.choice([random_1_cell_version, random_2_cell_version, random_3_cell_version])
            if second_random_version == random_1_cell_version:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            elif second_random_version == random_2_cell_version:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            else:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)

            self.hills_layer.set_cell(i, globalVar.TILE_COUNT - 3, my_hill)

        for i in range(int(globalVar.TILE_COUNT * 2 / 5), int(globalVar.TILE_COUNT * 3 / 5)):

            random_1_cell_version = random.choice(possible_1_cell_hills)
            random_2_cell_version = random.choice(possible_2_cell_hills)
            random_3_cell_version = random.choice(possible_3_cell_hills)

            second_random_version = random.choice([random_1_cell_version, random_2_cell_version,
                                                   random_3_cell_version])
            if second_random_version == random_1_cell_version:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            elif second_random_version == random_2_cell_version:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            else:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)

            status = self.hills_layer.set_cell(i, globalVar.TILE_COUNT - (i % 7), my_hill)

        for i in range(int(globalVar.TILE_COUNT * 3 / 5), int(globalVar.TILE_COUNT * 4 / 5)):
            for j in range(globalVar.TILE_COUNT - 10, globalVar.TILE_COUNT):
                random_1_cell_version = random.choice(possible_1_cell_hills)
                random_2_cell_version = random.choice(possible_2_cell_hills)
                random_3_cell_version = random.choice(possible_3_cell_hills)

                second_random_version = random.choice([random_1_cell_version, random_2_cell_version,
                                                       random_3_cell_version])
                if second_random_version == random_1_cell_version:
                    my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
                elif second_random_version == random_2_cell_version:
                    my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
                else:
                    my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)

                self.hills_layer.set_cell(i, j, my_hill)

        # -------------------------------------------------------------------------------------------------------------#
        # TREES
        self.trees_layer = overlay.Layer(globalVar.LAYER3)

        possible_trees = ["normal", "00033", "00012", "00043"]
        for i in range(int(globalVar.TILE_COUNT / 4), int(globalVar.TILE_COUNT * 3 / 4)):
            random_version = random.choice(possible_trees)
            my_normal_tree = element.Element(self.trees_layer, globalVar.LAYER3, random_version)
            self.trees_layer.set_cell(i, 5, my_normal_tree)

            my_normal_tree = element.Element(self.trees_layer, globalVar.LAYER3, random_version)
            self.trees_layer.set_cell(i, 7, my_normal_tree)

        # -------------------------------------------------------------------------------------------------------------#
        # ROADS
        self.roads_layer = roadoverlay.RoadLayer()
        middle = int(globalVar.TILE_COUNT * 1 / 2)
        for i in range(0, 2 * middle):
            self.roads_layer.set_cell_constrained_to_bottom_layer([self.hills_layer, self.trees_layer],
                                                                  i, middle)
        # -------------------------------------------------------------------------------------------------------------#
        # BUILDINGS
        self.buildings_layer = overlay.Layer(globalVar.LAYER5)

        for i in range(0, 10):
            my_dwelling = building.Dwelling(self.buildings_layer, globalVar.LAYER5)
            self.buildings_layer.set_cell_constrained_to_bottom_layer([self.hills_layer, self.trees_layer,
                                                                       self.roads_layer], globalVar.TILE_COUNT - 3,
                                                                      2 + i, my_dwelling)
        for i in range(0, 20, 4):
            my_dwelling = building.Dwelling(self.buildings_layer, globalVar.LAYER5)
            my_wheat_farm = building.Farm(self.buildings_layer, globalVar.LAYER5)
            self.buildings_layer.set_cell_constrained_to_bottom_layer([self.hills_layer, self.trees_layer,
                                                                       self.roads_layer], 3, i, my_wheat_farm)

        # liste de Walker()
        self.walkers_list = []
        # A list of layers to check for collision
        self.collisions_layers = [self.buildings_layer, self.hills_layer, self.trees_layer, self.roads_layer]
        # -------------------------------------------------------------------------------------------------------------#
        # Test logiques
        # self.buildings_layer.print_currents_elements()
