import unreal

def get_selected_content_browser_assets():
    editor_utility = unreal.EditorUtilityLibrary()
    selected_assets = editor_utility.get_selected_assets()
    
    return selected_assets

def generate_new_name_for_asset(asset):
    
    rename_config = {
        "prefixes_per_type" : [
            { "type": unreal.MaterialInstance, "prefix": "MI_" },
            { "type": unreal.Material, "prefix": "M_" },
            { "type": unreal.Texture, "prefix": "T_" },
            { "type": unreal.NiagaraSystem, "prefix": "NS_" }
        ]
    }
    
    name = asset.get_name()
    
    for prefix_per_type in rename_config["prefixes_per_type"]:
        prefix = prefix_per_type["prefix"]
        asset_type = prefix_per_type["type"]
        
        if isinstance(asset, asset_type) and not name.startswith(prefix):
            return prefix + name
    
    return name

def get_assets_incorrectly_named(assets):
    assets_to_rename = []
    for asset in assets:
        old_name = asset.get_name()
        new_name = generate_new_name_for_asset(asset)
        
        if (old_name == new_name):
            continue
        
        assets_to_rename.append(asset)
    return assets_to_rename

def rename_assets(assets):
    for asset in assets:
        old_name = asset.get_name()
        asset_old_path = asset.get_path_name()
        asset_folder = unreal.Paths.get_path(asset_old_path)
        
        new_name = generate_new_name_for_asset(asset)
        new_path = asset_folder + "/" + new_name
        
        print(f"{old_name} -> {new_name}")
        
        rename_success = unreal.EditorAssetLibrary.rename_asset(asset_old_path, new_path)
        if not rename_success:
            unreal.log_error("Could not rename: " + asset_old_path)
            
def run():
    selected_assets = get_selected_content_browser_assets()
    assets_to_rename = get_assets_incorrectly_named(selected_assets)
    
    if (len(assets_to_rename) == 0):
        unreal.EditorDialog.show_message("Asset Prefix Renaming", "The assets selected have the correct prefixes.", unreal.AppMsgType.OK)
        return
    
    window_name = "Warning: Asset Prefix Renaming"
    window_text = "The following assets have been found to have the incorrect prefix:\n"
    
    for asset in assets_to_rename:
        window_text += "\n" + asset.get_name()
        
    window_text += "\n\nWould you like to rename these files to have the correct prefix?"
    
    warning_dialogue = unreal.EditorDialog.show_message(window_name, window_text, unreal.AppMsgType.YES_NO)
    chosen_response = str(warning_dialogue)
    
    if("YES" in chosen_response):
        rename_assets(assets_to_rename)      
            
run()