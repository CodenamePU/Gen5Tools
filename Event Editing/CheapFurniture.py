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

def get_counts(type, ow_file):
	overworld = open(ow_file, "rb")
	types = {
		"furniture" : 0x4,
		"npc" : 0x5,
		"warp" : 0x6,
		"trigger" : 0x7
	}
	overworld.seek(types[type.lower()], 0)
	return struct.unpack("<B", overworld.read(1))

def get_filesize(ow_file):
	overworld = open(ow_file, "rb")
	overworld.seek(0x0, 0)
	return struct.unpack("<L", overworld.read(4))

furniture = []
npc = []
warp = []
trigger = []
extra = []

def extract_furniture(ow_file):
	overworld = open(ow_file, "rb")
	overworld.seek(0x8, 0)
	for x in range(0, nFurniture[0]):
		furniture.append(struct.unpack("<HHHHLLL", overworld.read(0x14)))
	return

def extract_npc(ow_file):
	overworld = open(ow_file, "rb")
	overworld.seek(0x8 + (nFurniture[0] * 0x14), 0)
	for x in range(0, nNPC[0]):
		npc.append(struct.unpack("<HHHHHHHHHHHHHHHHHH", overworld.read(0x24)))
	return

def extract_warp(ow_file):
	overworld = open(ow_file, "rb")
	overworld.seek(0x8 + (nFurniture[0] * 0x14) + (nNPC[0] * 0x24), 0)
	for x in range(0, nWarps[0]):
		warp.append(struct.unpack("<HHBBHHHHHHH", overworld.read(0x14)))
	return

def extract_trigger(ow_file):
	overworld = open(ow_file, "rb")
	overworld.seek(0x8 + (nFurniture[0] * 0x14) + (nNPC[0] * 0x24) + (nWarps[0] * 0x14), 0)
	for x in range(0, nTriggers[0]):
		trigger.append(struct.unpack("<HHHHHHHHHHH", overworld.read(0x16)))
	return

def get_extra(ow_file): # ???
	overworld = open(ow_file, "rb")
	isEnd = False
	overworld.seek(0x8 + (nFurniture[0] * 0x14) + (nNPC[0] * 0x24) + (nWarps[0] * 0x14) + (nTriggers[0] * 0x16), 0)
	while isEnd != True:
		try:
			extra.append(struct.unpack("<HL", overworld.read(0x6)))
		except struct.error:
			isEnd = True
	return

def overworld_to_asm(overworld):
	nFurniture = get_counts("furniture", overworld)
	nNPC = get_counts("npc", overworld)
	nWarps = get_counts("warp", overworld)
	nTriggers = get_counts("trigger", overworld)
	fileSize = get_filesize(overworld)
	extract_furniture(overworld)
	extract_npc(overworld)
	extract_warp(overworld)
	extract_trigger(overworld)
	if (nTriggers[0] > 0):
		get_extra(overworld)

	with open(overworld, "w") as output:
		output.write(".align 4\n.include \"B2W2.s\"\n")
		output.write(".byte " + hex(nFurniture[0]) + " @ Amount of Furniture\n")
		output.write(".byte " + hex(nNPC[0]) + " @ Amount of NPCs\n")
		output.write(".byte " + hex(nWarps[0]) + " @ Amount of Warps\n")
		output.write(".byte " + hex(nTriggers[0]) + " @ Amount of Triggers\n")
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
			output.write("Extra_Data:\n")
			for x in range(0, len(extra)):
				output.write("	extra " + str(extra[x][0]) + ", " + str(extra[x][1]) + "\n")
	return

def asm_to_overworld(file):
	cmd = [AS] + [ASFLAGS] + ['-c', file, '-o', os.path.splitext(file)[0] + '.o']
	subprocess.run(cmd)
	cmd = [OBJCOPY, '-O', 'binary', os.path.splitext(file)[0] + '.o', os.path.splitext(file)[0] + '.bin']
	subprocess.run(cmd)
	size = os.path.getsize(os.path.splitext(file)[0] + '.bin')
	with open(os.path.splitext(file)[0] + '.bin', "ab") as ow:
		ow.seek(0, 0)
		ow.write(struct.pack("<L", size - 4))
		ow_data.close()
	return

def main():
	if os.path.splitext(sys.argv[1]) == ".s":
		asm_to_overworld(sys.argv[2])
	elif os.path.splitext(sys.argv[1]) == ".bin":
		overworld_to_asm(sys.argv[2])
	else:
		print("invalid option")
	return

main()
