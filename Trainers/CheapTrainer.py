import os
import struct

def decompile_trainer(file)
    with open(file, "rb") as trainer:
        pokeformat, trainerclass, battle_type, nPokes = struct.unpack("<BBBB", trainer.read(4))
        unk1 = struct.unpack("<B", struct.read(1)) + (struct.unpack("<B", struct.read(1)) * 100)
        unk2 = struct.unpack("<B", struct.read(1)) + (struct.unpack("<B", struct.read(1)) * 100)
        unk3 = struct.unpack("<B", struct.read(1)) + (struct.unpack("<B", struct.read(1)) * 100)
        unk4 = struct.unpack("<B", struct.read(1)) + (struct.unpack("<B", struct.read(1)) * 100)
        unk5 = struct.unpack("<B", struct.read(1)) + (struct.unpack("<B", struct.read(1)) * 100)
        prizemoney = struct.unpack("<B", struct.read(1))

        with open(os.path.splitext(file)[0], "w") as trainer_decomp:
            trainer_decomp.write(["trainer", pokeformat, trainerclass, battle_type, nPokes, unk1, unk2, unk3, unk4, unk5, prizemoney])
