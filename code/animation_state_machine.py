import os

#TURN = ANIMATION_FOLDER + "/lowrez-short-turn-step.png"
ANIMATION_FOLDER =  "animaties"

TURN = os.path.join(ANIMATION_FOLDER, "turn-framed.png")
WALK = os.path.join(ANIMATION_FOLDER, "walk-framed.png")
STAND = os.path.join(ANIMATION_FOLDER, "stand-framed.png")

ANIMAION_STATE_MACHINE = {
    "states" : ["standing", "facing_left", "facing_right"],
    "first_state": "facing_right",
    "animations": [
        {
            "name": "standing_facing_right",
            "start_state": "facing_right",
            "buttons": set(),
            "end_state": "facing_right",
            "sprite_sheet": STAND,
#            "frame_size": (8, 8),
            "frame_count": 1,
            "mirrored": False
        },
        {
            "name": "standing_facing_left",
            "start_state": "facing_left",
            "buttons": set(),
            "end_state": "facing_left",
            "sprite_sheet": STAND,
#            "frame_size": (8, 8),
            "frame_count": 1,
            "mirrored": True
        },
        {
            "name": "turn_right",
            "start_state": "facing_left",
            "buttons": {"right"},
            "end_state": "facing_right",
            "sprite_sheet": TURN,
#            "frame_size": (8,8),
            "frame_count": 4,
            "mirrored": True
        },
        {
            "name": "turn_left",
            "start_state": "facing_right",
            "buttons": {"left"},
            "end_state": "facing_left",
            "sprite_sheet": TURN,
#            "frame_size": (8,8),
            "frame_count": 4,
            "mirrored": False
        },
        {
            "name": "step_right",
            "start_state": "facing_right",
            "buttons": {"right"},
            "end_state": "facing_right",
            "sprite_sheet": WALK,
#            "frame_size": (8, 8),
            "frame_count": 4,
            "mirrored": False
        },
        {
            "name": "step_left",
            "start_state": "facing_left",
            "buttons": {"left"},
            "end_state": "facing_left",
            "sprite_sheet": WALK,
#            "frame_size": (8, 8),
            "frame_count": 4,
            "mirrored": True
        },
    ]
}
