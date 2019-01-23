# Bob's Discount Map Object editor for B2W2

import struct
import sys
import subprocess
import os

# devkitARM setup
devkitPATH = 'C://devkitPro/devkitARM/bin/'
PREFIX = 'arm-none-eabi-'
AS = (devkitPATH + PREFIX + 'as')
ASFLAGS = '-mthumb'
OBJCOPY = (devkitPATH + PREFIX + 'objcopy')
overworld = open(sys.argv[2], "rb")

def get_counts(type):
	types = {
		"furniture" : 0x4,
		"npc" : 0x5,
		"warp" : 0x6,
		"trigger" : 0x7
	}
	overworld.seek(types[type.lower()], 0)
	return struct.unpack("<B", overworld.read(1))

def get_filesize():
	overworld.seek(0x0, 0)
	return struct.unpack("<L", overworld.read(4))

nFurniture = get_counts("furniture")
nNPC = get_counts("npc")
nWarps = get_counts("warp")
nTriggers = get_counts("trigger")
fileSize = get_filesize()

furniture = []
npc = []
warp = []
trigger = []
extra = []

def extract_furniture():
	overworld.seek(0x8, 0)
	for x in range(0, nFurniture[0]):
		furniture.append(struct.unpack("<HHHHLLL", overworld.read(0x14)))
	return

def extract_npc():
	overworld.seek(0x8 + (nFurniture[0] * 0x14), 0)
	for x in range(0, nNPC[0]):
		npc.append(struct.unpack("<HHHHHHHHHHHHHHHHHH", overworld.read(0x24)))
	return

def extract_warp():
	overworld.seek(0x8 + (nFurniture[0] * 0x14) + (nNPC[0] * 0x24), 0)
	for x in range(0, nWarps[0]):
		warp.append(struct.unpack("<HHBBHHHHHHH", overworld.read(0x14)))
	return

def extract_trigger():
	overworld.seek(0x8 + (nFurniture[0] * 0x14) + (nNPC[0] * 0x24) + (nWarps[0] * 0x14), 0)
	for x in range(0, nTriggers[0]):
		trigger.append(struct.unpack("<HHHHHHHHHHH", overworld.read(0x16)))
	return

def get_extra(): # ???
	isEnd = False
	overworld.seek(0x8 + (nFurniture[0] * 0x14) + (nNPC[0] * 0x24) + (nWarps[0] * 0x14) + (nTriggers[0] * 0x16), 0)
	while isEnd != True:
		try:
			extra.append(struct.unpack("<HL", overworld.read(0x6)))
		except struct.error:
			isEnd = True
	return

def overworld_to_asm():
	extract_furniture()
	extract_npc()
	extract_warp()
	extract_trigger()
	if (nTriggers[0] > 0):
		get_extra()

	with open(os.path.splitext(os.path.basename(sys.argv[2]))[0] + ".s", "w") as output:
		output.write(".align 4\n\n.include \"b2w2.s\"\n")
		output.write(".word " + hex(fileSize[0]) + " @fileSize\n")
		output.write(".byte " + hex(nFurniture[0]) + " @nFurniture\n")
		output.write(".byte " + hex(nNPC[0]) + " @nNPC\n")
		output.write(".byte " + hex(nWarps[0]) + " @nWarps\n")
		output.write(".byte " + hex(nTriggers[0]) + " @nTriggers\n")
		output.write("\n")

		if (nFurniture[0] > 0):
			output.write("@ Furniture\n")
			output.write("Furniture:\n")
			for x in range(0, nFurniture[0]):
				output.write("	furniture " + str(furniture[x][0]) + ", " + str(furniture[x][1]) + ", " + str(furniture[x][2]) + ", " + str(furniture[x][3]) + ", " + str(furniture[x][4]) + ", " + str(furniture[x][5]) + ", " + str(furniture[x][6]) + "\n")
			output.write("\n")

		if (nNPC[0] > 0):
			output.write("@ NPCs\n")
			output.write("NPCs:\n")
			for x in range(0, nNPC[0]):
				output.write("	npc " + str(npc[x][0]) + ", " + str(npc[x][1]) + ", " + str(npc[x][2]) + ", " + str(npc[x][3]) + ", " + str(npc[x][4]) + ", " + str(npc[x][5]) + ", " + str(npc[x][6]) + ", " + str(npc[x][7]) + ", " + str(npc[x][8]) + ", " + str(npc[x][9]) + ", " + str(npc[x][10]) + ", " + str(npc[x][11]) + ", " + str(npc[x][12]) + ", " + str(npc[x][13]) + ", " + str(npc[x][14]) + ", " + str(npc[x][15]) + ", " + str(npc[x][16]) + ", " + str(npc[x][17]) + "\n")
			output.write("\n")

		if (nWarps[0] > 0):
			output.write("@ Warps\n")
			output.write("Warps:\n")
			for x in range(0, nWarps[0]):
				output.write("	warp " + str(warp[x][0]) + ", " +  str(warp[x][1]) + ", " + str(warp[x][2]) + ", " + str(warp[x][3]) + ", " +  str(warp[x][4])+ ", " +  str(warp[x][5])+ ", " +  str(warp[x][6])+ ", " +  str(warp[x][7])+ ", " +  str(warp[x][8]) + ", " +  str(warp[x][9])+ ", " +  str(warp[x][10])+ "\n")
			output.write("\n")

		if (nTriggers[0] > 0):
			output.write("@ Triggers\n")
			output.write("Triggers:\n")
			for x in range(0, nTriggers[0]):
				output.write("	trigger " + str(trigger[x][0]) + ", " + str(trigger[x][1]) + ", " + str(trigger[x][2]) + ", " + str(trigger[x][3]) + ", " + str(trigger[x][4]) + ", " + str(trigger[x][5]) + ", " + str(trigger[x][6]) + ", " + str(trigger[x][7]) + ", " + str(trigger[x][8]) + ", " + str(trigger[x][9]) + ", " + str(trigger[x][10]) + str(trigger[x][11]) + str(trigger[x][12]) + "\n")
			output.write("\n")

		if (len(extra) > 0):
			output.write("\n@ Extra Data (Triggers?)\n")
			output.write("ExtraData:\n")
			for x in range(0, len(extra)):
				output.write("	extra " + str(extra[x][0]) + ", " + str(extra[x][1]) + "\n")
	return

def asm_to_overworld(file):
	cmd = [AS] + [ASFLAGS] + ['-c', file, '-o', os.path.splitext(os.path.basename(file))[0] + '.o']
	subprocess.run(cmd)
	cmd = [OBJCOPY, '-O', 'binary', os.path.splitext(os.path.basename(file))[0] + '.o', os.path.splitext(os.path.basename(file))[0] + '.bin']
	subprocess.run(cmd)
	return

def main():
	if sys.argv[1].lower() == "decompile":
		overworld_to_asm()
	elif sys.argv[1].lower() == "compile":
		asm_to_overworld(sys.argv[2])
	else:
		print("invalid option")
	return

main()
