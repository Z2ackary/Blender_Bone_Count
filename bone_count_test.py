import bpy

# 设置标准骨骼数量
standard_bone_count = 5  # 你可以根据需要修改这个值



class BoneCountError(Exception):
    pass
def show_error_popup(message):
    bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message), title="骨骼数不符合要求", icon='ERROR')

def check_bone_count_armature(armature):
    # 获取骨架中的骨骼数量
    bone_count = len(armature.pose.bones)
    
    # 检查是否符合标准
    if bone_count == standard_bone_count:
        print(f"骨架 '{armature.name}' 中的骨骼数量符合标准 ({standard_bone_count} 骨骼)。")
        
    else:
        print(f"警告：骨架 '{armature.name}' 中的骨骼数量不符合标准！当前骨骼数量为 {bone_count}，标准为 {standard_bone_count}。")
        # 这里可以添加你的自定义处理逻辑，比如中止导出等

        error_message = f"警告：骨架 '{armature.name}' 中的骨骼数量不符合标准！当前骨骼数量为 {bone_count}，标准为 {standard_bone_count}。"
        print(error_message)
        # 这里可以添加你的自定义处理逻辑，比如中止导出等
        show_error_popup(error_message)

        raise BoneCountError(f"骨架 '{armature.name}' 中的骨骼数量不符合标准！")

def check_hierarchy(obj):
    # 递归遍历层级结构
    if obj.type == 'ARMATURE':
        check_bone_count_armature(obj)
    
    for child in obj.children:
        check_hierarchy(child)

# 在导出之前运行的回调函数
def pre_export_callback(scene):
    # 获取所有骨架


    armatures = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE']
    
    # 检查每个骨架的骨骼数量和层级结构
    for armature in armatures:
        check_hierarchy(armature)

# 注册导出前的回调函数
def register():
    bpy.app.handlers.frame_change_pre.append(pre_export_callback)

# 注销导出前的回调函数
def unregister():
    # bpy.app.handlers.frame_change_pre.remove(pre_export_callback)

    if pre_export_callback in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.remove(pre_export_callback)
    else:
        print("Warning: pre_export_callback not found in handlers, cannot remove.")

# # 在blender中运行register()函数，将回调函数注册到导出前的处理列表
# register()
