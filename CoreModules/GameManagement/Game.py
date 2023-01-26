import random

from Services import servicesGlobalVariables as globalVar
from Services.Service_Game_Data import building_dico, road_dico, removing_cost
from CoreModules.GameManagement import Update as updates
from CoreModules.BuildingsManagement import buildingsManagementBuilding as buildings
from CoreModules.WalkersManagement import walkersManagementWalker as walkers

import copy

INIT_MONEY = 1000000000
TIME_BEFORE_REMOVING_DWELL = 3 #seconds
import time

"""
ATTENTION: Building en feu pourrait etre updated
"""
class Game:
    def __init__(self, _map, name="save"):
        self.name = name
        self.map = _map
        self.startGame()

        self.money = INIT_MONEY
        self.food = 0
        self.potery = 0
        self.likeability = 0
        self.gods_favors = [0, 0, 0, 0, 0]
        self.caesar_score = 0
        self.unemployement = 0
        self.isPaused = False
        self.buildinglist = []
        self.walkersAll = []
        self.walkersOut = []
        self.framerate = globalVar.DEFAULT_FPS
        self.updated = []

        # some lists of specific buildings
        self.water_structures_list = []
        self.food_structures_list = []
        self.temple_structures_list = []
        self.education_structures_list = []
        self.fountain_structures_list = []
        self.basic_entertainment_structures_list = []
        self.pottery_structures_list = []
        self.bathhouse_structures_list = []

        #
        self.last_water_structure_removed = None
        self.last_food_structure_removed = None
        self.last_temple_structure_removed = None
        self.last_education_structure_removed = None
        self.last_fountain_structure_removed = None
        self.last_basic_entertainment_structure_removed = None
        self.last_pottery_structure_removed = None
        self.last_bathhouse_structure_removed = None

        # Timer
        self.init_time = time.time()

        # a dic of timers to track dwells with no roads
        # it associates each position of dwell with a timer
        self.timer_track_dwells = {}

    def startGame(self):
        # ---------------------------------#
        _path = self.map.path_entry_to_exit(self.map.roads_layer.get_entry_position(),
                                            self.map.roads_layer.get_exit_position() )
        self.map.roads_layer.build_path_entry_to_exit(_path, [self.map.hills_layer, self.map.trees_layer])

    def change_game_speed(self, step):
        """
        A step of 1 indicates incremental speed
        And -1 indicates decremental speed
        """
        if self.framerate > globalVar.DEFAULT_FPS:
            if step == 1 and self.framerate < 10*globalVar.DEFAULT_FPS:
                self.framerate += globalVar.DEFAULT_FPS
            elif step == -1:
                self.framerate -= globalVar.DEFAULT_FPS
        elif self.framerate < globalVar.DEFAULT_FPS:
            if step == 1:
                self.framerate += 0.1*globalVar.DEFAULT_FPS
            elif step == -1 and self.framerate > 0.1*globalVar.DEFAULT_FPS:
                self.framerate -= 0.1*globalVar.DEFAULT_FPS
        else:
            if step == 1:
                self.framerate += globalVar.DEFAULT_FPS
            elif step == -1:
                self.framerate -= 0.1*globalVar.DEFAULT_FPS

    def foodproduction(self):
        # ---------------------------------#
        pass

    def updatebuilding(self, building: buildings.Building):
        current_state = (building.isBurning, building.isDestroyed,building.risk_level_dico["fire"],building.risk_level_dico["collapse"])
        if not building.isDestroyed:
            building.update_risk("fire")
            building.update_risk("collapse")
        updated_state = (building.isBurning, building.isDestroyed,building.risk_level_dico["fire"],building.risk_level_dico["collapse"])
        dico_change = {"fire": current_state[0] != updated_state[0],
                       "collapse" : current_state[1] != updated_state[1],
                       "fire_level" : (current_state[2] != updated_state[2],building.risk_level_dico["fire"]),
                       "collapse_level"  : (current_state[3] != updated_state[3],building.risk_level_dico["collapse"])
                      }
        return  dico_change

    def updateReligion(self):
        pass


    def print_building_list(self):
        for b in self.buildinglist:
            print(b.dic['version'])
    def update_supply_requirements(self, of_what: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                         'basic_entertainment' or 'pottery' or 'bathhouse'):
        """
        This functions searches for supply structures on the map and for each one look for dwell within the range of
        the structure. If the dwell required a structure of this type, then its position will be added to the list of
        buildings to update.
        return: a set of positions of housings that will be updated, to avoid duplicate values
        """

        buildings_position_to_append_to_update_object = []
        tmp = of_what+'_structures_list'
        structures_list = getattr(self, tmp)
        for structure in structures_list:
            if not structure.is_functional():
                continue
            buildings_position_to_append_to_update_object += list(self.intermediate_update_supply_function(of_what,
                                                                                        structure, evolvable=True))
        return set(buildings_position_to_append_to_update_object)

    def intermediate_update_supply_function(self, of_what: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                           'basic_entertainment' or 'pottery' or 'bathhouse', structure, evolvable=True):

        buildings_position_to_append_to_update_object = []
        if structure:  # None
            if structure.is_functional():
                _range = structure.range
                _position = structure.position

                for building in self.buildinglist:
                    line, column = building.position
                    if -_range + _position[0] <= line < _range + 1 + _position[0] and -_range + _position[1] <= column \
                            < _range + 1 + _position[1] and building.dic['version'] == "dwell":
                        building.update_requirements()
                        status = building.update_with_supply(of_what, evolvable=evolvable)
                        if status:
                            buildings_position_to_append_to_update_object.append((building.position,
                                                                                  building.structure_level))
        return set(buildings_position_to_append_to_update_object)

    def downgrade_supply_requirement(self, of_what: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                           'basic_entertainment' or 'pottery' or 'bathhouse'):
        tmp = 'last_'+of_what + '_structure_removed'
        structure = getattr(self, tmp)
        buildings_position_to_append_to_update_object = list(self.intermediate_update_supply_function(of_what, structure,
                                                                                                      evolvable=False))
        setattr(self, tmp, None)
        return buildings_position_to_append_to_update_object

    def updategame(self):
        """
        This function updates the game
        In fact it updates the buildings of the game
        Differents types of updates can occur: a building evolving, a building burning or a building collapsing
        """

        update = updates.LogicUpdate()

        # Update dwell that just set functional (immigrant live in)
        for building in self.updated:
            update.has_evolved.append((building.position, building.structure_level))
        self.updated.clear()

        #
        update.has_devolved += list(self.downgrade_supply_requirement('water'))
        update.has_devolved += list(self.downgrade_supply_requirement('food'))
        update.has_devolved += list(self.downgrade_supply_requirement('temple'))
        update.has_devolved += list(self.downgrade_supply_requirement('education'))
        update.has_devolved += list(self.downgrade_supply_requirement('fountain'))
        update.has_devolved += list(self.downgrade_supply_requirement('basic_entertainment'))
        update.has_devolved += list(self.downgrade_supply_requirement('pottery'))
        update.has_devolved += list(self.downgrade_supply_requirement('bathhouse'))

        update.has_evolved += list(self.update_supply_requirements('water'))
        update.has_evolved += list(self.update_supply_requirements('food'))
        update.has_evolved += list(self.update_supply_requirements('temple'))
        update.has_evolved += list(self.update_supply_requirements('education'))
        update.has_evolved += list(self.update_supply_requirements('fountain'))
        update.has_evolved += list(self.update_supply_requirements('basic_entertainment'))
        update.has_evolved += list(self.update_supply_requirements('pottery'))
        update.has_evolved += list(self.update_supply_requirements('bathhouse'))

        update.has_evolved = list(set(update.has_evolved))
        update.has_devolved = list(set(update.has_devolved))

        for k in self.buildinglist:
            # Update of the risk speed level
            k.update_risk_speed_with_level()

            pos = k.position

            if k.update_functional_building_animation(self.framerate):
                # animated building update
                update.has_evolved.append((pos, k.structure_level))

            voisins = self.get_voisins_tuples(k)
            has_road = [self.map.roads_layer.is_real_road(v[0],v[1]) for v in voisins]
            # Creation of walkers
            if type(k) == buildings.Dwelling and k.current_population < k.max_population and any(has_road):
                path = self.map.walk_to_a_building(self.map.roads_layer.get_entry_position(),None, k.position,[])[1]
                if path:
                    for i in range(k.max_population - k.current_population):
                        self.create_walker(path.copy(),k)
            elif k.dic['version'] == "prefecture" and not k.functional and any(has_road):
                self.citizenToPrefet(k)
            elif k.dic['version'] == "engineer's_post" and not k.functional and any(has_road):
                self.citizenToEngineer(k)

            if type(k) == buildings.Dwelling and k.isBurning and not k.beingWorkedOn:
                for w in self.walkersAll:
                    if type(w) == walkers.Prefect and w.workingOn is None:
                        w.set_current_path(k)
                        if w.current_path_to_follow:
                            w.workingOn = k
                            k.beingWorkedOn = True
            elif type(k) == buildings.Dwelling and k.isDestroyed and not k.beingWorkedOn:
                for w in self.walkersAll:
                    if type(w) == walkers.Engineer and w.workingOn is None:
                        w.set_current_path(k)
                        if w.current_path_to_follow:
                            w.workingOn = k
                            k.beingWorkedOn = True

            for w in self.walkersAll:
                if type(w) == walkers.Prefect:
                    if w.init_pos in voisins:
                        k.risk_dico["fire"], k.risk_level_dico["fire"] = 0, 0
                        self.updated.append(k)
                if type(w) == walkers.Engineer:
                    if w.init_pos in voisins:
                        k.risk_dico["collapse"], k.risk_level_dico["collapse"] = 0, 0
                        self.updated.append(k)

            # We don't want primitive housing (pannel) to burn or to collapse
            if type(k) == buildings.Dwelling and not k.is_occupied():
                # we check if a road is next to this dwelling, if not we remove it after Xs
                removable = True
                line, column = k.position
                for i in range(-2, 2+1):
                    for j in range(-2, 2+1):
                        if self.map.roads_layer.is_real_road(line + i, column + j):
                            removable = False
                            break
                # update tracktimer of dwells
                built_since = int(time.time() - self.timer_track_dwells[pos]) if pos in self.timer_track_dwells else 0

                if removable and built_since > TIME_BEFORE_REMOVING_DWELL:
                    # to avoid decreasing money
                    self.money += removing_cost
                    self.remove_element(pos)
                    update.removed.append(pos)
                    self.timer_track_dwells.pop(pos)

                elif built_since > TIME_BEFORE_REMOVING_DWELL:
                    self.timer_track_dwells.pop(pos)

            # ---------------------------------------------------------#
            # Update of burnt and collapsed buildings


            building_update = self.updatebuilding(k)
            cases = self.map.buildings_layer.get_all_positions_of_element(pos[0], pos[1])
            if building_update["fire"]:
                # the building is no more functional
                for i in cases:
                    k.functional = False
                    self.map.buildings_layer.array[i[0]][i[1]].isBurning = True
                    update.catchedfire.append(i)

            if building_update["collapse"]:
                # the building is no more functional
                for i in cases:
                    self.map.buildings_layer.array[i[0]][i[1]].isDestroyed = True
                    # the building is no more functional
                    k.functional = False
                    update.collapsed.append(i)

            if building_update["fire_level"][0]:
                update.fire_level_change.append((k.position,building_update["fire_level"][1]))
            if building_update["collapse_level"][0]:
                update.collapse_level_change.append((k.position,building_update["collapse_level"][1]))

        return update
        # ---------------------------------#



    def create_walker(self,path=[],building=None):
        walker = walkers.Immigrant(self.map.roads_layer.get_entry_position()[0],self.map.roads_layer.get_entry_position()[1],
                                   None, 0, self,path,building)
        self.walkersAll.append(walker)
        self.walkersGetOut(walker)

    def citizenToPrefet(self, prefecture):
        voisins = self.get_voisins_tuples(prefecture)
        possible_road = [v for v in voisins if self.map.roads_layer.is_real_road(v[0], v[1])]
        possible_worker = [w for w in self.walkersAll if type(w) == walkers.Citizen]
        if possible_worker:
            prefet = random.choice(possible_worker)
            prefet.change_class(walkers.Prefect)
            prefet.prefecture = prefecture
            prefet.init_pos = possible_road[2]
            self.walkersGetOut(prefet)
            prefecture.set_functional(True)

    def citizenToEngineer(self, engineer_post):
        voisins = self.get_voisins_tuples(engineer_post)
        possible_road = [v for v in voisins if self.map.roads_layer.is_real_road(v[0], v[1])]
        possible_worker = [w for w in self.walkersAll if type(w) == walkers.Citizen]
        if possible_worker:
            engineer = random.choice(possible_worker)
            engineer.change_class(walkers.Engineer)
            engineer.engineers_post = engineer_post
            engineer.init_pos = possible_road[2]
            self.walkersGetOut(engineer)
            engineer_post.set_functional(True)

    def walkersGetOut(self, walker):
        self.walkersOut.append(walker)
        pass

    def walkersOutUpdates(self, exit=False):  # fps = self.framerate
        if exit:
            for walker in self.walkersOut:
                walker.get_out_city()
        else:
            for walker in self.walkersOut:
                walker.current_path_to_follow = self.map.walk_to_a_building(walker.init_pos,walker.dest_pos,(globalVar.TILE_COUNT//2, globalVar.TILE_COUNT // 2 -4 ),[])[1]
                walker.dest_compteur = 0
        pass

    def remove_element(self, pos) -> str | None:
        """
        Cette fonction permet d'enlever un element de la map à une position donnée
        On ne peut pas retirer de l'herbe ou une montagne
        """
        if self.money < removing_cost:
            print("Not enough money")
            return None
        line, column = pos[0], pos[1]
        status, element_type, _element = self.map.remove_element_in_cell(line, column)
        if status:
            self.money -= removing_cost
            if element_type == globalVar.LAYER5:
                if self.buildinglist:
                    """
                    # to remove the time tracker if the building is removed before 3s
                    if pos in self.timer_track_dwells:
                        self.timer_track_dwells.pop(pos)
                    """
                    self.buildinglist.remove(_element)
                    if type(_element) == buildings.WaterStructure:
                        # we must copy the element because if will potentially be  removed or changed in memory
                        self.last_water_structure_removed = copy.copy(_element)
                        self.water_structures_list.remove(_element)
                    del _element
        return element_type

    def remove_elements_serie(self, start_pos, end_pos) -> set:
        """
        Pour clean une surface de la carte
        Elle va renvoyer un ensemble set qui contient les layers qui ont été modifiés
        """
        line1, column1 = start_pos[0], start_pos[1]
        line2, column2 = end_pos[0], end_pos[1]

        # 2 ranges qui vont servir à délimiter la surface de la map à clean
        vrange, hrange = None, None

        # le set
        _set = set()

        if line1 >= line2:
            vrange = range(line1, line2 - 1, -1)
        else:
            vrange = range(line2, line1 - 1, -1)

        if column1 <= column2:
            hrange = range(column2, column1 - 1, -1)
        else:
            hrange = range(column1, column2 - 1, -1)

        for i in vrange:
            for j in hrange:
                result = self.remove_element((i, j))
                if result:
                    _set.add(result)
        return _set

    def add_road(self, line, column) -> bool:
        # Precondition: we must have enough money for adding a road
        if self.money < road_dico['cost']:
            print("Not enough money")
            return False
        status = self.map.roads_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line, column)
        if status:
            self.money -= road_dico['cost']
        return status

    def add_roads_serie(self, start_pos, end_pos, dynamically=False) -> bool:
        # Here we can't precisely calculate the money that will be needed to construct all the roads. we'll estimate
        # that
        estimated_counter_roads = (abs(start_pos[0] - end_pos[0])) + (abs(start_pos[1] - end_pos[1])) + 1
        if self.money < estimated_counter_roads * road_dico['cost']:
            print("Not enough money")
            return False

        status, count = self.map.roads_layer.add_roads_serie(start_pos, end_pos,
                    self.map.collisions_layers, memorize=dynamically)

        if status and not dynamically:
            self.money -= road_dico['cost'] * count
        return status

    def add_building(self, line, column, version) -> bool:
        txt= " ".join(version.split("_"))
        if self.money < building_dico[txt].cost:
            print("Not enough money")
            return False
        # we have to determine the exact class of the building bcause they have not the same prototype
        match version:
            case 'dwell':
                building = buildings.Dwelling(self.map.buildings_layer, globalVar.LAYER5)

            case "well" | "fountain"| "fountain1" | "fountain2" | "fountain3" | "fountain4" | "reservoir":
                building = buildings.WaterStructure(self.map.buildings_layer, globalVar.LAYER5, version)

            case _:
                building = buildings.Building(self.map.buildings_layer, globalVar.LAYER5, version)

        status = self.map.buildings_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line, column,
                                                                               building)
        if status:
            match version:
                case _:
                    self.buildinglist.append(building)

            if version == "dwell":
                # if user just built a dwell we associate a timer so that the dwell can be removed after x seconds
                self.timer_track_dwells[(line, column)] = time.time()


            self.money -= building_dico[txt].cost
            if type(building) == buildings.WaterStructure:
                self.water_structures_list.append(building)
        return status

    def update_likability(self,building):
        voisins = self.get_voisins(building)
        score = 0
        for voisin in voisins:
            version = voisin.dic["version"]
            if version not in ["null"]:
                if version == "dwell":
                    pass


    def get_voisins(self,building):
        voisins = set()
        cases = []
        pos = building.position
        for i in range(0, building.dic['cells_number']):
                    for j in range(0, building.dic['cells_number']):
                        if (i, j) != (0, 0):
                            cases.append(self.map.buildinglayer((pos[0] + i, pos[1] + j)))
        for case in cases:
            for i in range(-2,2):
                for j in range(-2,2):
                                    voisins.add(self.map.buildinglayer.array[case[0] + i][case[1] + j])
        return voisins

    def get_voisins_tuples(self,building):
        pos = building.position
        cases = []
        for i in range(-2,3):
            for j in range(-2,3):
                cases.append((pos[0] + i,pos[1] + j))
        return cases