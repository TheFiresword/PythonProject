from Services import servicesGlobalVariables as const


def mapping_function(element_type, type_version) -> [str, int]:
    """
    Fonction de mapping version d'un élément -> chemin de fichier
    """
    if type_version in {"null", "occupied"}:
        return [("", 0)]

    if element_type == "grass":
        if type_version == "normal":
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_00272.png", 1)]
        elif type_version == "yellow":
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_00029.png", 1)]
        elif type_version == "buisson":
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_00235.png", 1)]
        elif int(type_version) >= 0:
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_" + type_version + ".png", 1)]
        else:
            # Valeur par défaut
            return [("", 0)]

    elif element_type == "hills":

        if type_version == "big-mountain1":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00079.png", 2)]
        elif type_version == "big-mountain2":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00080.png", 2)]
        elif type_version == "big-mountain3":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00081.png", 2)]
        elif type_version == "big-mountain4":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00082.png", 2)]

        elif type_version == "geant-mountain1":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00083.png", 3)]
        elif type_version == "geant-mountain2":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00084.png", 3)]

        elif type_version == "small-mountain1":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00071.png", 1)]
        elif type_version == "small-mountain2":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00072.png", 1)]
        elif type_version == "small-mountain3":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00073.png", 1)]
        elif type_version == "small-mountain4":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00074.png", 1)]
        elif type_version == "small-mountain5":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00075.png", 1)]
        elif type_version == "small-mountain6":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00076.png", 1)]
        elif type_version == "small-mountain7":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00077.png", 1)]
        elif type_version == "small-mountain8":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00078.png", 1)]
        else:
            return [("", 0)]

    elif element_type == "trees":
        if type_version == "normal":
            return [(const.SPRITE_PATH + "Land/Land1/Arbres/Land1a_00045.png", 1)]
        elif int(type_version) >= 0 and type_version != "00010" and type_version != "00011":
            return [(const.SPRITE_PATH + "Land/Land1/Arbres/Land1a_" + type_version + ".png", 1)]
        else:
            return [("", 0)]

    elif element_type == "roads":
        if type_version == "normal":
            return [(const.SPRITE_PATH + "Land/LandOverlay/Land2a_00093.png", 1)]
        elif type_version == "entry":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00089.png", 1)]
        elif type_version == "exit":
            return [(const.SPRITE_PATH + "Land/Land3/Land3a_00087.png", 1)]
        elif int(type_version) >= 0 and type_version < "00111":
            return [(const.SPRITE_PATH + "Land/LandOverlay/Land2a_" + type_version + ".png", 1)]
        else:
            return [("", 0)]

    elif element_type == "buildings":
        if type_version == "dwell":
            my_array = []
            for level in range(7):
                count_digit = len(str(level))
                if count_digit == 1:
                    my_array.append((const.SPRITE_PATH + "Land/housng/Housng1a_0000"+str(level)+".png", 1))
                if count_digit == 2:
                    my_array.append((const.SPRITE_PATH + "Land/housng/Housng1a_000" + str(level) + ".png", 1))
            return my_array

        elif type_version == "forum":
            return [(const.SPRITE_PATH + "Land\Govt\Govt_00010.png", 2)]
        elif type_version == "senate":
            return [(const.SPRITE_PATH + "Land\Govt\Govt_00003.png", 3)]
        elif type_version == "gov_housing_house":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "gov_housing_villa":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "gov_housing_palace":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "academy":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "library":
            return [(const.SPRITE_PATH + "Education\Education_00003.png", 2)]
        elif type_version == "school":
            return [(const.SPRITE_PATH + "Education\Education_00001.png", 2)]
        elif type_version == "university":
            return [(const.SPRITE_PATH + "Education\Education_00002.png", 3)]
        elif type_version == "garden":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "plaza":
            return [(const.SPRITE_PATH + "Entertainment\entertainment_00105.png", 1)]
        elif type_version == "engineer's_post":
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00001.png", 1)]

        elif type_version == "quai":  # (same picture reverted 4 times) (from 0 to 4)
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00002.png", 2)]
        elif type_version == "quai2":
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00003.png", 2)]
        elif type_version == "quai3":
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00004.png")]
        elif type_version == "quai4":
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00005.png")]

        elif type_version == "dock":  # (same picture reverted 4 times) (from 5 to 8)
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00006.png", 3)]
        elif type_version == "dock2":
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00007.png", 3)]
        elif type_version == "dock3":
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00008.png", 3)]
        elif type_version == "dock4":
            return [(const.SPRITE_PATH + "EngineeringStructures\EngineeringStructures_00009.png", 3)]

        elif type_version == "theatre":
            return [(const.SPRITE_PATH + "Entertainment\entertainment_00013.png", 2)]
        elif type_version == "amphitheatre":
            return [(const.SPRITE_PATH + "Entertainment\entertainment_00001.png", 3)]
        elif type_version == "colosseum":
            return [(const.SPRITE_PATH + "Entertainment\entertainment_00036.png", 5)]
        elif type_version == "actor_colony":
            return [(const.SPRITE_PATH + "Entertainment\entertainment_00081.png", 3)]
        elif type_version == "gladiator_school":
            return [(const.SPRITE_PATH + "Entertainment\entertainment_00051.png", 3)]
        elif type_version == "lion_house":
            return [(const.SPRITE_PATH + "Entertainment\entertainment_00062.png", 3)]
        elif type_version == "barber":
            return [(const.SPRITE_PATH + "Hygiene/Hygiene_00001.png", 1)]

        #first model of a bath
        elif type_version == "baths":
            return [(const.SPRITE_PATH + "Hygiene/Hygiene_00004.png", 2),
                    (const.SPRITE_PATH + "Hygiene/Hygiene_00005.png", 2)]

        elif type_version == "hospital":
            return [(const.SPRITE_PATH + "Hygiene/Hygiene_00002.png", 3)]
        if type_version == "dispensary":
            return [(const.SPRITE_PATH + "Hygiene/Hygiene_00003.png", 1)]

        elif type_version == "foundation_farm":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00012.png", 2)]

        elif type_version == "fruit_farm":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00023.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00024.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00025.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00026.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00027.png", 1)]


        elif type_version == "olive_farm":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00028.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00029.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00030.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00030.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00031.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00032.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00033.png", 1)]


        elif type_version == "pig_farm":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00038.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00039.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00040.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00041.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00042.png", 1)]


        elif type_version == "vegetable_farm":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00019.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00020.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00021.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00022.png", 1)]

        elif type_version == "vine_farm":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00033.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00034.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00035.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00036.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00037.png", 1)]


        elif type_version == "wheat_farm":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00013.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00014.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00015.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00016.png", 1),
                    (const.SPRITE_PATH + "Commerce\Commerce_00017.png", 1)]

        elif type_version == "iron_mine":
            return [(const.SPRITE_PATH + "")]
        elif type_version == "timber_yard":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00072.png", 2)]
        elif type_version == "marble_quarry":
            return [(const.SPRITE_PATH + "")]
        elif type_version == "clay_pit":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00061.png", 2)]
        elif type_version == "furniture_workshop":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00117.png", 2)]
        elif type_version == "oil_workshop":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00099.png", 2)]
        elif type_version == "pottery_workshop":
            return [(const.SPRITE_PATH + "")]
        elif type_version == "weapons_workshop":
            return [(const.SPRITE_PATH + "")]
        elif type_version == "wine_workshop":
            return [(const.SPRITE_PATH + "")]
        elif type_version == "market":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00001.png", 2)]
        elif type_version == "granary":
            return [(const.SPRITE_PATH + "Commerce\Commerce_00141.png", 2)]
        elif type_version == "warehouse":
            return [(const.SPRITE_PATH + "")]
        elif type_version == "wall":
            return [(const.SPRITE_PATH + "")]
        elif type_version == "tower":
            return [(const.SPRITE_PATH + "")]

        # Different aspects of a gatehouse (Same picture reverted)
        elif type_version == "gatehouse_left":
            return [(const.SPRITE_PATH + "Land\LandOverlay\Land2a_00150.png", 2)]
        elif type_version == "gatehouse_right":
            return [(const.SPRITE_PATH + "Land\LandOverlay\Land2a_00151.png", 2)]

        elif type_version == "prefecture":
            return [(const.SPRITE_PATH + "Security\Security_00002.png", 1)]
        elif type_version == "fort":
            return [(const.SPRITE_PATH + "Security\Security_00003.png", 3)]
        elif type_version == "military_academy":
            return [(const.SPRITE_PATH + "Security\Security_00001.png", 3)]

        elif type_version == "reservoir": #empty reservoir
            return [(const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00002.png", 3),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00003.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00004.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00005.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00006.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00007.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00008.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00009.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00010.png", 1)]


        #First type of fountain
        elif type_version == "fountain": #empty fountain
            return [(const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00011.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00012.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00013.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00014.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00015.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00016.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00017.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00018.png", 1)]

        # Second type of fountain
        elif type_version == "fountain2":  # empty fountain
            return [(const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00019.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00020.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00021.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00022.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00023.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00024.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00025.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00026.png", 1)]

        # Third type of fountain
        elif type_version == "fountain3":  # empty fountain
            return [(const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00027.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00028.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00029.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00030.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00031.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00032.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00033.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00034.png", 1)]

        # Fourth type of fountain
        elif type_version == "fountain4":  # empty fountain
            return [(const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00036.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00037.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00038.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00039.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00040.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00041.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00042.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00018.png", 1)]

        elif type_version == "aqueduct":
            return [(const.SPRITE_PATH + "", 1)]
        elif type_version == "well":
            return [(const.SPRITE_PATH + "WaterEquipments\WaterEquipments_00001.png", 1)]
        elif type_version == "barracks":
            return [(const.SPRITE_PATH + "Security\Security_00010.png", 3)]

        # Different aspects of a shipyard (Same picture reverted on 4 positions)
        elif type_version == "shipyard":
            return [(const.SPRITE_PATH + "Security\Security_00006.png", 2)]
        elif type_version == "shipyard2":
            return [(const.SPRITE_PATH + "Security\Security_00007.png", 2)]
        elif type_version == "shipyard3":
            return [(const.SPRITE_PATH + "Security\Security_00008.png", 2)]
        elif type_version == "shipyard4":
            return [(const.SPRITE_PATH + "Security\Security_00009.png", 2)]

        #Temples of gods
        elif type_version == "ceres":
            return [(const.SPRITE_PATH + "Temples\Temples_00001.png", 2),
                        (const.SPRITE_PATH + "Temples\Temples_00002.png", 3)]

        elif type_version == "mars":
            return [(const.SPRITE_PATH + "Temples\Temples_00003.png", 2),
                        (const.SPRITE_PATH + "Temples\Temples_00004.png", 3)]

        elif type_version == "mercure":
            return [(const.SPRITE_PATH + "Temples\Temples_00005.png", 2),
                    (const.SPRITE_PATH + "Temples\Temples_00006.png", 3)]

        elif type_version == "neptune":
            return [(const.SPRITE_PATH + "Temples\Temples_00007.png", 2),
                    (const.SPRITE_PATH + "Temples\Temples_00008.png", 3)]

        elif type_version == "venus":
            return [(const.SPRITE_PATH + "Temples\Temples_00009.png", 2),
                        (const.SPRITE_PATH + "Temples\Temples_00010.png", 3)]

        elif type_version == "oracle":
            return [(const.SPRITE_PATH + "Temples\Temples_00011.png", 2)]

def get_structures_range(element_type, type_version) -> int:
    pass