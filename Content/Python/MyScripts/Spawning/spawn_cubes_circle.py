import unreal
import math

def spawn_single_cube(location = unreal.Vector(), rotation = unreal.Rotator()):
    
    # Get the system to control actors
    editor_actor_subs = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # We then want to creattor
    actor_class = unreal.StaticMeshActor
    
    # Place it in the level
    static_mesh_actor = editor_actor_subs.spawn_actor_from_class(actor_class, location, rotation)
    
    # Load and add the cube to it
    static_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    static_mesh_actor.static_mesh_component.set_static_mesh(static_mesh)
    
def run():
    
    cube_count = 30
    circle_radius = 1000
    circle_centre = unreal.Vector(0, 0, 0)
    
    for i in range(cube_count):
        circle_x_position = circle_radius * math.cos(math.radians(i * 360 / cube_count))
        circle_y_position = circle_radius * math.sin(math.radians(i * 360 / cube_count))
        
        location = unreal.Vector(circle_x_position, circle_y_position)
        location_to_circle_centre = location - circle_centre
        
        rotation = location_to_circle_centre.quaternion().rotator()
        
        spawn_single_cube(location, rotation)
        
# This tells unreal everything in the with block is part of the transaction "Place cubes
#  in a circle". This means that everything in the with can be undone.
with unreal.ScopedEditorTransaction("Place cubes in a circle") as trans:
    run()