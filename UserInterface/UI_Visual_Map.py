import arcade
from Services import servicesGlobalVariables as constantes
from Services import Service_Static_functions as fct
from Services import Service_Game_Data as gdata
from pyglet.math import Vec2


class VisualMap:

    def __init__(self):
        self.grass_layer = None
        self.hills_layer = None
        self.trees_layer = None
        self.roads_layer = None
        self.fire_layer = None
        self.fire_count = 0
        self.destoyed_layer = None
        self.collapse_layer = None
        self.buildings_layer = None
        self.walker_to_render = None
        self.map_scaling = constantes.SPRITE_SCALING
        self.red_sprite = arcade.Sprite()
        self.red_sprite.visible = False
        self.destroyed = constantes.SPRITE_PATH + "Land/LandOverlay/Land2a_00112.png"
        pass
    
    def setup(self, game):
        self.grass_layer = arcade.SpriteList(use_spatial_hash=True)
        self.hills_layer = arcade.SpriteList()
        self.trees_layer = arcade.SpriteList()
        self.roads_layer = arcade.SpriteList()
        self.buildings_layer = arcade.SpriteList()
        self.walker_to_render = arcade.SpriteList()
        self.fire_layer = arcade.SpriteList()
        self.destroyed_layer = arcade.SpriteList()
        self.create_ground(game)
        self.update_layers(self.hills_layer, game.map.hills_layer.array)
        self.update_layers(self.trees_layer, game.map.trees_layer.array)
        self.update_layers(self.roads_layer, game.map.roads_layer.array)
        self.update_layers(self.buildings_layer, game.map.buildings_layer.array)
        self.update_walker_list(game.walkersOut)
        pass


    def create_ground(self, _game):
        layer = self.grass_layer
        array = _game.map.grass_layer.array

        layer.clear()
        k = 0
        for i in range(0, len(array)):  # I=On parcout le tableau logique du bas vers le haut
            line = array[i]
            for j in range(0, len(line)):
                file_names = array[i][j].file_paths
                first_path = file_names[0][0]
                if first_path != "":
                    _sprite = arcade.Sprite(first_path, self.map_scaling)
                else:
                    _sprite = arcade.Sprite()

                overflowing_height = (_sprite.height - constantes.TILE_HEIGHT * self.map_scaling)

                # Calcul des coordonnées du sprite en cartésien --
                _sprite.center_x = constantes.TILE_WIDTH * self.map_scaling * j
                _sprite.center_y = (constantes.TILE_HEIGHT * self.map_scaling * i)

                # Conversion en isométrique des coordonnées
                _isometric_x = (_sprite.center_x + _sprite.center_y) - (constantes.TILE_WIDTH * self.map_scaling *
                                                                        k / 2)
                _isometric_y = (-_sprite.center_x + _sprite.center_y) / 2 + (
                        constantes.TILE_HEIGHT * self.map_scaling * k / 2) + overflowing_height/2

                _sprite.center_x, _sprite.center_y = _isometric_x, _isometric_y

                k += 1
                k = k % constantes.TILE_COUNT

                # On ajoute le sprite au layer (spriteList)
                layer.append(_sprite)
        layer.reverse()

    def update_layers(self, layer, array):
        if layer == self.buildings_layer:
            self.fire_layer.clear()
            self.destroyed_layer.clear()
        layer.clear()
        k = constantes.TILE_COUNT**2 -1
        for i in range(0, len(array)):  # I=On parcout le tableau logique du bas vers le haut
            line = array[i]
            for j in range(0, len(line)):
                file_names = [ file_name[0] for file_name in array[i][j].file_paths]
                first_path = file_names[0]

                if first_path == "":
                    _sprite = arcade.Sprite()
                else:
                    if layer != self.buildings_layer:
                        _sprite = arcade.Sprite(first_path, self.map_scaling)
                    else:
                        # For buildings layer
                        # we must save all textures in the sprite
                        textures = [arcade.load_texture(path) for path in file_names]
                        _sprite = arcade.Sprite()
                        for texture in textures:
                            _sprite.append_texture(texture)
                            _sprite.set_texture(0)
                            _sprite.scale = self.map_scaling

                count = array[i][j].dic['cells_number']
                overflowing_height = (_sprite.height - constantes.TILE_HEIGHT * self.map_scaling * count)

                _sprite.center_x, _sprite.center_y = self.grass_layer[k].center_x, self.grass_layer[k].center_y

                _sprite.center_x += (count-1)*constantes.TILE_WIDTH/2*self.map_scaling
                _sprite.center_y += overflowing_height/2
                
                if hasattr(array[i][j],"isBurning") and hasattr(array[i][j],"isDestroyed"):
                    if array[i][j].isBurning or array[i][j].isDestroyed:
                        _sprite.visible = False
                    if array[i][j].isBurning:
                        firesprite = self.fire_sprite(_sprite.position)
                        firesprite.center_x, firesprite.center_y = self.grass_layer[k].center_x, self.grass_layer[k].center_y
                        self.fire_layer.append(firesprite)

                    if array[i][j].isDestroyed:
                        destroyedsprite = self.destroyed_sprite(_sprite.position)
                        destroyedsprite.center_x, destroyedsprite.center_y = self.grass_layer[k].center_x, self.grass_layer[k].center_y
                        self.destroyed_layer.append(destroyedsprite)
                k -= 1
                layer.append(_sprite)
        layer.reverse()

    def update_walker_list(self, walkersout):
        self.walker_to_render.clear()
        for walker in walkersout:
            support_sprite = (self.get_sprite_associated(walker.init_pos))
            walker_pos_x,walker_pos_y = support_sprite.center_x,support_sprite.center_y+10
            walker_pos_x += walker.offset_x
            walker_pos_y += walker.offset_y
            if walker.head == "up":
                walker_sprite=arcade.Sprite(filename=walker.paths_up[walker.compteur % len(walker.paths_up)],
                                            center_x=walker_pos_x,center_y=walker_pos_y,scale=self.map_scaling)
            elif walker.head == "right":
                walker_sprite=arcade.Sprite(filename=walker.paths_right[walker.compteur % len(walker.paths_right)],
                                            center_x=walker_pos_x,center_y=walker_pos_y,scale=self.map_scaling)
            elif walker.head == "down":
                walker_sprite = arcade.Sprite(filename=walker.paths_down[walker.compteur % len(walker.paths_down)],
                                              center_x=walker_pos_x, center_y=walker_pos_y, scale=self.map_scaling)
            elif walker.head == "left":
                walker_sprite = arcade.Sprite(filename=walker.paths_left[walker.compteur % len(walker.paths_left)],
                                              center_x=walker_pos_x, center_y=walker_pos_y, scale=self.map_scaling)

            self.walker_to_render.append(walker_sprite)
        pass

    def draw_layers(self, game):
        layers = [(self.grass_layer, game.map.grass_layer.activate), (self.roads_layer, game.map.roads_layer.activate),
                  (self.hills_layer, game.map.hills_layer.activate), (self.trees_layer, game.map.trees_layer.activate)
                  ,(self.fire_layer,True),(self.destroyed_layer,True),(self.buildings_layer, game.map.buildings_layer.activate)]
        for k in layers:
            if k[1]: k[0].draw()

    def rescale_the_map(self, new_scale, game):
        """
        There is an arcade function that might be useful: arcade.SpriteList().rescale()
        This function rescales all the sprites of a spriteList.
        But the problem is that the rendering is not correct.
        The map is deformed.
        So I did it  other way.
        Empty the map and recreate it with the right scaling.
        :param new_scale:
        :return:
        """

        self.map_scaling = new_scale
        self.setup(game)

    def get_map_center(self):
        center_tile = self.grass_layer[int(len(self.grass_layer) // 2 + constantes.TILE_COUNT // 2)]
        return Vec2(center_tile.center_x, center_tile.center_y)

    def get_sprite_at_screen_coordinates(self, pos):
        """
        Cette fonction va retourner la position logique (line, column) du sprite qui se trouve aux coordonnées x,y
        en px
        """
        self.red_sprite.center_x, self.red_sprite.center_y = pos
        (nearest_sprite, d) = arcade.get_closest_sprite(self.red_sprite, self.grass_layer)
        self.red_sprite.center_x, self.red_sprite.center_y = nearest_sprite.center_x, nearest_sprite.center_y

        index = self.grass_layer.index(nearest_sprite)

        line, column = fct.convert_sprite_list_index_to_logic_position(index)
        return line, column
    
    def get_visual_sprite(self,pos):
        self.red_sprite.center_x, self.red_sprite.center_y = pos
        (nearest_sprite, d) = arcade.get_closest_sprite(self.red_sprite, self.grass_layer)
        return nearest_sprite.center_x,nearest_sprite.center_y
    
    def get_sprite_associated(self, position):
        index = position[0] * 40 + position[1]
        return self.grass_layer[constantes.TILE_COUNT**2 - index -1]
        
    
    def get_logic_element_associated(self, _sprite, _sprite_list):
        index = _sprite_list.index(_sprite)
        line = int(index / constantes.TILE_COUNT)
        column = int(index % constantes.TILE_COUNT)
        if _sprite_list == self.visualmap.grass_layer:
            return self.game.map.grass_layer.array[line][column]
        elif _sprite_list == self.visualmap.hills_layer:
            return self.game.map.hills_layer.array[line][column]
        elif _sprite_list == self.visualmap.trees_layer:
            return self.game.map.trees_layer.array[line][column]
        elif _sprite_list == self.visualmap.roads_layer:
            return self.game.map.roads_layer.array[line][column]
        elif _sprite_list == self.visualmap.buildings_layer:
            return self.game.map.buildings_layer.array[line][column]

    def fill_temporary_build(self,list,sprite_list:arcade.SpriteList,type,mode):
        for pos in list:
            support_sprite = (self.get_sprite_associated(pos))
            sprite_pos_x,sprite_pos_y = support_sprite.center_x,support_sprite.center_y
            if mode == "build":
                sprite = arcade.Sprite(filename=(gdata.building_dico[type]).spritepath,center_x= sprite_pos_x,center_y=sprite_pos_y,scale=self.map_scaling)
            else:
                sprite = arcade.Sprite(filename=constantes.SPRITE_PATH + "Land/LandOverlay/Land2a_00001.png",center_x= sprite_pos_x,center_y=sprite_pos_y,scale=self.map_scaling)
            sprite_list.append(sprite)

    def update_one_sprite(self,layer:arcade.SpriteList,position,update_type,new_texture_path=[]):
        index = fct.get_sprite_list_index(position)
        support_sprite = (self.get_sprite_associated(position))
        sprite_pos_x,sprite_pos_y = support_sprite.center_x,support_sprite.center_y
        sprite = layer[constantes.TILE_COUNT**2 - index -1]
        sprite.position = sprite_pos_x,sprite_pos_y
        if not sprite.visible:
            sprite.visible = True
        if update_type == "building_destroy":
            firesprite= self.look_sprite_list(support_sprite.center_x,support_sprite.center_y,self.fire_layer)
            if firesprite:
                firesprite.visible = False
            sprite.visible = False
            collapsedsprite= self.destroyed_sprite((sprite_pos_x,sprite_pos_y))
            self.destroyed_layer.append(collapsedsprite)
        if update_type == "building_fire":
            sprite.visible = False
            firesprite= self.look_sprite_list(support_sprite.center_x,support_sprite.center_y,self.fire_layer)
            if firesprite:
                firesprite.visible = not firesprite.visible
            else:
                firesprite= self.fire_sprite((sprite_pos_x,sprite_pos_y))
                self.fire_layer.append(firesprite)
        if update_type == "change_content":
            sprite.textures = []
            for k in new_texture_path:
                sprite.append_texture(arcade.load_texture(k))
            sprite.append_texture(arcade.load_texture(self.destroyed))
            sprite.set_texture(0)
        if update_type == "stat_inc":
            ind = sprite.textures.index(sprite.texture)
            if sprite.textures[ind+1] == sprite.textures[-1]:
                sprite.set_texture(0)
            else :
                sprite.set_texture(ind+1)
        if update_type == "delete":
            sprite.visible = False
        sprite.scale = self.map_scaling
    
    def fire_sprite(self,pos):
        textures =  [arcade.load_texture(constantes.SPRITE_PATH + "Land/LandOverlay/Land2a_00"+str(i) +".png") for i in range(188,196)]
        sprite = arcade.Sprite()
        sprite.center_x = pos[0]
        sprite.center_y = pos[1]
        for textu in textures:
            sprite.append_texture(textu)
        sprite.set_texture(1)
        sprite.scale = self.map_scaling
        return sprite
    
    def destroyed_sprite(self,pos):
        sprite = arcade.Sprite()
        sprite.center_x = pos[0]
        sprite.center_y = pos[1]
        sprite.texture = arcade.load_texture(self.destroyed)
        sprite.scale = self.map_scaling
        return sprite
    
    def look_sprite_list(self,x,y,spritelist:arcade.SpriteList):
        for sprite in spritelist:
            if sprite.position == (x,y):
                return sprite