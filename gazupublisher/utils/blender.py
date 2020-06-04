
def blender_print(data):
    """
    Print to display in the Blender console
    """
    import bpy
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "CONSOLE":
                override = {"window": window, "screen": screen, "area": area}
                for line in str(data).split("\n"):
                    bpy.ops.console.scrollback_append(
                        override, text=str(line), type="OUTPUT"
                    )