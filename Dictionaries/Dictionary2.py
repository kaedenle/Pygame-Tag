#FOR SS2
#---------------------------------POSSIBLE COMMANDS---------------------------------
#INTER: Can interrupt current state with anything?
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
#FUNCT: Associated function to run (defined in class, will repeat every call)
#LOCK: Lock movement and turning
    #default is TRUE
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
            "BL":{"SWING2":True},
        },
        "RUN":{
            "INTER":True,
	    "FRAME_LEN":6,
	    "INDEX":3,
            "LOOP": True,
            "BL":{"SWING2":True},
            "FUNCT":lambda self: self.run(),
            "LOCK": False
        },
        "JUMP":{
            "INTER":False,
	    "FRAME_LEN":6,
	    "INDEX":0,
            "WL":{"DEFAULT": True},
            "BL":{"RUN": True, "SWING":True},
            "FUNCT":lambda self: self.jump(),
            "LOCK": False
        },
        "CROUCH":{
            "INTER":False,
	    "FRAME_LEN":3,
	    "INDEX":4,
            "WL":{"JUMP": True, "SLIDE": True},
            "BL":{"RUN": True},
            "FUNCT":lambda self: self.crouch(),
            "LOCK": True,
            "SPEED": 0.5
        },
        "SLIDE":{
            "INTER":False,
	    "FRAME_LEN":6,
	    "INDEX":2,
            "WL":{"JUMP": True},
            "FUNCT":lambda self: self.slide(),
            "LOCK": True,
            "SPEED": 0.25
        }
}

