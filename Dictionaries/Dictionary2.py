#FOR SS2
#---------------------------------POSSIBLE COMMANDS---------------------------------
#INTER: What frame can you change state (actionable)?
    #always (0)
    #never (-1)
    #Integer from [0, FRAME_LEN]
#FRAME_LEN: How many total frames is this animation?
#INDEX: What row is the animation taken from the sprite sheet
#BL: Prevents changing to listed states from current state
    #Optional
    #useless if INTER is 1
#WL: Overrides INETER to allow listed states to interrupt current state
    #Optional
    #useless if INTER is 0
    #WL overrides BL
#LOOP: Should the animation loop (TRUE) or stop after the first play (FALSE)?
    #default is TRUE
    #useless if RESET is TRUE or state isn't attatched to hold input
#RESET: Once an animation loop finishes, should state be reset to default state (TRUE) or keep on current state (FALSE)
    #Default is TRUE
#FRAME: What frame from row should be picked if FRAME_LEN < 1
    #Default is 0
    #indexed
#SPEED: How fast each frame should pass (0, 1]
    #Default is 0.15
    #closer to 0 is slowest, 1 is fastest, above 1 potentially skips frames
    #Try to limit use of SPEED, try to build animation to fit the default of 0.15
#FUNCT: Associated function to run (defined in class, will repeat every call)
#CAN_MOVE: Can you move while in state
    #Default is False
STATE_DICT = {
	"SWING":{
	    "INTER":False,
	    "FRAME_LEN":6,
	    "INDEX":0,
            "WL":{"SWING2":True}
	},
        "SWING2":{
            "INTER":False,
	    "FRAME_LEN":10,
	    "INDEX":3,
            "BL":{"CROUCH": True}
        },
        "DEFAULT":{
            "INTER":True,
	    "FRAME_LEN":1,
	    "INDEX":4,
            "BL":{"SWING2":True}
        },
        "RUN_LEFT":{
            "INTER":True,
	    "FRAME_LEN":6,
	    "INDEX":3,
            "LOOP": True,
            "BL":{"SWING2":True},
            "FUNCT":lambda self: self.run_left()
        },
        "RUN_RIGHT":{
            "INTER":True,
	    "FRAME_LEN":6,
	    "INDEX":3,
            "LOOP": True,
            "BL":{"SWING2":True},
            "FUNCT":lambda self: self.run_right()
        },
        "JUMP":{
            "INTER":False,
	    "FRAME_LEN":6,
	    "INDEX":0,
            "FUNCT":lambda self: self.jump()
        }
}

