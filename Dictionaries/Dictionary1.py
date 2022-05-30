#FOR STICKMAN
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
PLAY_DICT = {
	"SWING":{
	    "INTER":-1,
	    "FRAME_LEN":10,
	    "INDEX":2,
            "WL":{"SWING2":True}
	},
        "SWING2":{
            "INTER":-1,
	    "FRAME_LEN":10,
	    "INDEX":3,
            "BL":{"CROUCH": True}
        },
        "DEFAULT":{
            "INTER":0,
	    "FRAME_LEN":4,
	    "INDEX":7,
            "BL":{"SWING2":True}
        },
        "RUNNING":{
            "INTER":0,
	    "FRAME_LEN":8,
	    "INDEX":1,
            "RESET":False,
            "LOOP": True,
            "BL":{"SWING2":True},
            "CAN_MOVE": True
        },
        "CROUCH":{
            "INTER":0,
            "FRAME_LEN":8,
            "INDEX":3,
            "RESET": False,
            "LOOP": False,
            "FRAME":7,
            "SPEED":0.75,
            "BL":{"SWING2":True},
            "FUNCT":lambda self: self.crouch(),
            "CAN_MOVE": True
        },
        "JUMP":{
            "INTER":0,
            "FRAME_LEN":7,
            "INDEX":2,
            "FRAME":7,
            "RESET": False,
            "LOOP": False,
            "FUNCT":lambda self: self.jump(),
            "CAN_MOVE": True
        },
        "DIVE":{
            "INTER":-1,
            "FRAME_LEN":8,
            "INDEX": 3,
            "SPEED":0.15,
            "FUNCT":lambda self: self.dive(),
            "CAN_MOVE": False
            ,"WL":{"JUMP":True}
        },
        "AIRDASH":{
            "INTER":-1,
            "FRAME_LEN":8,
            "INDEX": 2,
            "FUNCT":lambda self: self.airDash()
        }
}

