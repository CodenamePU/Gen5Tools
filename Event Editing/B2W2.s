@ HHHHLLL
.macro furniture script, arg2, arg3, arg4, x, y, z
.hword \script
.hword \arg2
.hword \arg3
.hword \arg4
.word \x
.word \y
.word \z
.endm

@ HHHHHHHHHHHHHHHHHH
.macro npc id, sprite, movement, movement2, flag, script, direction, sight, arg9, arg10, leftrightleash, updownleash, arg13, arg14, x, y, arg17, z
.hword \id
.hword \sprite
.hword \movement
.hword \movement2
.hword \flag
.hword \script
.hword \direction
.hword \sight
.hword \arg9
.hword \arg10
.hword \leftrightleash
.hword \updownleash
.hword \arg13
.hword \arg14
.hword \x
.hword \y
.hword \arg17
.hword \z
.endm

@ HHBBLLHHH
.macro warp map, usewarpcoordsabovemap, arg3, arg4, arg5 x, arg7, y, x_extension, y_extension, arg11
.hword \map
.hword \usewarpcoordsabovemap
.byte \arg3
.byte \arg4
.hword \arg5
.hword \x
.hword \arg7
.hword \y
.hword \x_extension
.hword \y_extension
.hword \arg11
.endm

.macro trigger entity, constant, ref, arg4, arg5, x, y, z, arg9, arg10, arg11
.hword \entity
.hword \constant
.hword \ref
.hword \arg4
.hword \arg5
.hword \x
.hword \y
.hword \z
.hword \arg9
.hword \arg10
.hword \arg11
.endm

.macro extra arg1, arg2
.hword \arg1
.word \arg2
.endm
