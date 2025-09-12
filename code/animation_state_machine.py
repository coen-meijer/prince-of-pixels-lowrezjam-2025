import os

#TURN = ANIMATION_FOLDER + "/lowrez-short-turn-step.png"
ANIMATION_FOLDER =  "animaties"

TURN = os.path.join(ANIMATION_FOLDER, "turn-framed-c.png")
WALK = os.path.join(ANIMATION_FOLDER, "walk-framed-c.png")
STAND = os.path.join(ANIMATION_FOLDER, "stand-framed-c.png")

ANIMAION_STATE_MACHINE = {
    "states" : ["standing", "facing_left", "facing_right"],
    "first_state": "facing_right",
    "animations": [

        {
            "name": "standing",
            "start_state": "facing_right",
            "buttons": set(),
            "end_state": "facing_right",
            "sprite_sheet": STAND,
        },
        {
            "name": "turn",
            "start_state": "facing_right",
            "buttons": {"left"},
            "end_state": "facing_left",
            "sprite_sheet": TURN,
        },
        {
            "name": "step",
            "start_state": "facing_right",
#            "buttons": {"right"},
            "end_state": "facing_right",
            "sprite_sheet": WALK,
        },
    ]
}
