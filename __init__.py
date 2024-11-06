bl_info = {
    "name": "Grease Pencil Stroke Highlighter",
    "blender": (4, 2, 0),
    "category": "Grease Pencil",
    "author": "Boonsak Watanavisit",
    "version": (1, 0),
    "description": "Highlight strokes in the previous keyframe of a Grease Pencil object.",
}

import bpy

# Store original material indices for reverting later
original_material_indices = {}
last_highlighted_index = -1  # Track the last highlighted stroke

# Function to highlight strokes in the previous keyframe by cycling through each stroke
def highlight_previous_keyframe_stroke(operator, material_name):
    global last_highlighted_index

    def get_previous_keyframe(frame_numbers, current_frame):
        previous_frames = [f for f in frame_numbers if f < current_frame]
        return max(previous_frames) if previous_frames else None

    if bpy.context.object and bpy.context.object.type == "GPENCIL":
        gpencil = bpy.context.object.data
        layer = gpencil.layers.active
        keyframe_numbers = [frame.frame_number for frame in layer.frames]
        original_frame = bpy.context.scene.frame_current
        previous_keyframe = get_previous_keyframe(keyframe_numbers, original_frame)

        if previous_keyframe is not None:
            # Find the previous keyframe by frame number
            prev_keyframe_frame = next((frame for frame in layer.frames if frame.frame_number == previous_keyframe), None)
            if not prev_keyframe_frame:
                operator.report({'WARNING'}, "Previous keyframe not found.")
                return

            total_strokes = len(prev_keyframe_frame.strokes)
            if total_strokes == 0:
                operator.report({'WARNING'}, "No strokes found in the keyframe.")
                return

            # Determine the next stroke index to highlight
            current_index = bpy.context.scene.gpencil_current_highlighted_stroke
            next_index = (current_index + 1) % total_strokes  # Cycle through strokes

            # Find the material index for the selected material name
            material_index = next((idx for idx, mat in enumerate(gpencil.materials) if mat.name == material_name), -1)
            if material_index == -1:
                operator.report({'WARNING'}, "Selected material not found.")
                return

            # Store original material indices if not already stored
            if previous_keyframe not in original_material_indices:
                original_material_indices[previous_keyframe] = [stroke.material_index for stroke in prev_keyframe_frame.strokes]

            # Revert the last highlighted stroke to its original material
            if last_highlighted_index != -1 and last_highlighted_index < total_strokes:
                prev_keyframe_frame.strokes[last_highlighted_index].material_index = original_material_indices[previous_keyframe][last_highlighted_index]

            # Highlight the next stroke in the sequence
            prev_keyframe_frame.strokes[next_index].material_index = material_index
            bpy.context.scene.gpencil_current_highlighted_stroke = next_index
            last_highlighted_index = next_index  # Update last highlighted index
            bpy.context.scene.gpencil_total_strokes = total_strokes

            # Restore original frame without changing the frame in UI
            layer.active_frame = next((f for f in layer.frames if f.frame_number == original_frame), None)
            operator.report({'INFO'}, f"Highlighted stroke {next_index + 1} out of {total_strokes}.")
        else:
            operator.report({'WARNING'}, "No previous keyframe found.")
    else:
        operator.report({'WARNING'}, "Active object is not a Grease Pencil object.")

# Revert all strokes in the previous keyframe to their original materials
def revert_strokes_to_original(operator):
    gpencil = bpy.context.object.data
    layer = gpencil.layers.active
    original_frame = bpy.context.scene.frame_current

    # Get the previous keyframe
    keyframe_numbers = [frame.frame_number for frame in layer.frames]
    previous_keyframe = next((f for f in reversed(keyframe_numbers) if f < original_frame), None)

    if previous_keyframe is not None and previous_keyframe in original_material_indices:
        prev_keyframe_frame = next((frame for frame in layer.frames if frame.frame_number == previous_keyframe), None)
        if prev_keyframe_frame:
            for i, stroke in enumerate(prev_keyframe_frame.strokes):
                stroke.material_index = original_material_indices[previous_keyframe][i]
            layer.active_frame = next((f for f in layer.frames if f.frame_number == original_frame), None)
            operator.report({'INFO'}, "All strokes reverted to original materials.")
    else:
        operator.report({'WARNING'}, "No previous keyframe or original materials found.")

# Operator class
class HighlightPreviousKeyframeOperator(bpy.types.Operator):
    """Cycle through strokes in previous keyframe"""
    bl_idname = "gpencil.highlight_previous_keyframe_strokes"
    bl_label = "Highlight Stroke"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        material_name = context.scene.gpencil_highlight_material
        highlight_previous_keyframe_stroke(self, material_name)
        return {'FINISHED'}

class ResetStrokeOperator(bpy.types.Operator):
    """Reset highlighted stroke index and revert materials"""
    bl_idname = "gpencil.reset_stroke"
    bl_label = "Reset Index"

    def execute(self, context):
        context.scene.gpencil_current_highlighted_stroke = -1  # Set to -1 to start from the first stroke on next cycle
        global last_highlighted_index
        last_highlighted_index = -1  # Reset last highlighted index as well
        revert_strokes_to_original(self)  # Revert materials
        return {'FINISHED'}

class RevertMaterialsOperator(bpy.types.Operator):
    """Revert all strokes in previous keyframe"""
    bl_idname = "gpencil.revert_materials"
    bl_label = "Revert All"

    def execute(self, context):
        revert_strokes_to_original(self)
        return {'FINISHED'}

class HighlightPreviousKeyframePanel(bpy.types.Panel):
    bl_label = "Stroke Highlighter"
    bl_idname = "GPENCIL_PT_highlight_strokes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Grease Pencil'

    def draw(self, context):
        layout = self.layout

        # Create a box to emphasize the highlight button
        box = layout.box()
        box.label(text="Highlight Operation", icon="MODIFIER")
        box.prop(context.scene, "gpencil_highlight_material", text="Material")
        box.operator("gpencil.highlight_previous_keyframe_strokes", text="Highlight Stroke", icon="GREASEPENCIL")

        # Display stroke info and other options
        layout.label(text=f"Total strokes in previous keyframe: {context.scene.gpencil_total_strokes}")
        layout.label(text=f"Currently highlighted: {context.scene.gpencil_current_highlighted_stroke + 1}")
        layout.operator("gpencil.reset_stroke", text="Reset Index")
        layout.operator("gpencil.revert_materials", text="Revert All")

# Dynamic material list for dropdown
def update_material_list(self, context):
    obj = context.object
    if obj and obj.type == "GPENCIL":
        return [(mat.name, mat.name, "") for mat in obj.data.materials]
    return []

# Register properties, operators, and panel
def register():
    bpy.utils.register_class(HighlightPreviousKeyframeOperator)
    bpy.utils.register_class(ResetStrokeOperator)
    bpy.utils.register_class(RevertMaterialsOperator)
    bpy.utils.register_class(HighlightPreviousKeyframePanel)

    bpy.types.Scene.gpencil_highlight_material = bpy.props.EnumProperty(
        name="Material",
        description="Select material to highlight strokes",
        items=update_material_list
    )
    bpy.types.Scene.gpencil_total_strokes = bpy.props.IntProperty(
        name="Total Strokes",
        default=0
    )
    bpy.types.Scene.gpencil_current_highlighted_stroke = bpy.props.IntProperty(
        name="Current Stroke",
        default=-1  # Start from -1 to begin highlighting from the first stroke on first click
    )

def unregister():
    bpy.utils.unregister_class(HighlightPreviousKeyframeOperator)
    bpy.utils.unregister_class(ResetStrokeOperator)
    bpy.utils.unregister_class(RevertMaterialsOperator)
    bpy.utils.unregister_class(HighlightPreviousKeyframePanel)

    del bpy.types.Scene.gpencil_highlight_material
    del bpy.types.Scene.gpencil_total_strokes
    del bpy.types.Scene.gpencil_current_highlighted_stroke

if __name__ == "__main__":
    register()