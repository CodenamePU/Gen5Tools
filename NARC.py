import struct
import os

# NARC Tool

def NARC_Unpack(narc, output_folder):
    if output_folder != None:
        if ('.' in narc) == True:
            output_folder = narc.split('.')[0] + "_u"
        else:
            output_folder = narc + "_u"
    with open(narc, "rb") as narc_file:
        # Header
        magic, constant, fileSize, headerSize, nSections = struct.unpack("<LLLHH", narc_file.read(struct.calcsize("<LLLHH")))

        print("Getting data...")
        # File Allocation Table Block (FATB)
        fatb_magic, fatb_sectionSize, fatb_nFiles = struct.unpack("<LLL", narc_file.read(struct.calcsize("LLL")))
        fatb_startoffsets = []
        fatb_endoffsets = []
        for x in range(0, fatb_nFiles):
            fatb_startoffsets.append(struct.unpack("L", narc_file.read(struct.calcsize("L"))))
            fatb_endoffsets.append(struct.unpack("L", narc_file.read(struct.calcsize("L"))))

        # File Name Table Block (FNTB)
        fntb_magic, fntb_sectionSize = struct.unpack("<LL", narc_file.read(struct.calcsize("<LL")))
        fntb_directorystartoffset, fntb_firstfileposroot, fntb_nDir = struct.unpack("<LHH", narc_file.read(struct.calcsize("<LHH")))

        fntb_firstoffsets = []
        fntb_firstfilepos = []
        fntb_parentdir = []
        fntb_sizeName = []
        fntb_name = []
        fntb_dirnum = []

        # The Pokémon games do not use nested directories. As a result, the check will always default to fntb_nDir == 1.
        # The directory code has not been tested therefore. You have been warned.
        if (fntb_nDir != 1):
            for x in range(0, fntb_nDir):
                fntb_firstoffsets.append(struct.unpack("<L", narc_file.read(4)))
                print(fntb_firstoffsets[x])
                fntb_firstfilepos.append(struct.unpack("<H", narc_file.read(2)))
                print(fntb_firstfilepos[x])
                fntb_parentdir.append(struct.unpack("<H", narc_file.read(2)))
                print(fntb_parentdir[x])
                fntb_sizeName.append(struct.unpack("<B", narc_file.read(1)))
                print(fntb_sizeName[x])
                if fntb_sizeName[x][0] == 0:
                    fntb_name.append(x)
                else:
                    fntb_name.append(narc_file.read(fntb_sizeName[x][0]).decode('utf-8'))
                print(fntb_name[x])
                fntb_dirnum.append(struct.unpack("<H", narc_file.read(2)))
                print(fntb_dirnum[x])
        elif fntb_nDir == 1:
            for x in range(0, fatb_nFiles):
                fntb_name.append(str(x))
            pass

        # File Images (FIMG)
        fimg_offset = narc_file.tell() + 0x8
        fimg_magic, fimg_sectionSize = struct.unpack("<LL", narc_file.read(8))

        try:
            os.mkdir(output_folder)
        except FileExistsError:
            pass

        # Extract it now
        print("Extracting...")
        for x in range(0, fatb_nFiles):
            narc_file.seek(fimg_offset + fatb_startoffsets[x][0], 0)
            with open(os.path.join(os.getcwd(), output_folder, str(fntb_name[x]) +  ".bin"), "wb") as file:
                file.write(narc_file.read(fatb_endoffsets[x][0] - fatb_startoffsets[x][0]))
        print("Done!")
    return

def NARC_Pack(unpacked_narc, output_folder):
    print("Getting files in folder...")
    files = os.listdir(os.path.join(os.getcwd(), unpacked_narc))
    files_sorted = sorted([int(x[:-4]) for x in files])

    # FIMG creation
    print("Making FIMG...")
    fimg_data = b""
    file_sizes = []
    fimg_end = 0
    with open(unpacked_narc.split("_")[0] + "_fimg.bin", "wb") as fimg:
        fimg.write(struct.pack("<L", 0x46494D47))
        for x in range(0, len(files_sorted)):
            file = open(os.path.join(os.getcwd(), unpacked_narc, str(files_sorted[x]) + ".bin"), "rb")
            file_sizes.append(len(fimg_data))
            fimg_data += file.read()
        fimg.write(struct.pack("<L", len(fimg_data) + 8))
        fimg.write(fimg_data)
        fimg_end = len(fimg_data)

    # FNTB creation
    # 42 54 4E 46 10 00 00 00 04 00 00 00 00 00 01 00
    print("Making FNTB...")
    with open(unpacked_narc.split("_")[0] + "_fntb.bin", "wb") as fntb:
        fntb.write(struct.pack("<L", 0x464E5442))
        fntb.write(struct.pack("<L", 0x10))
        fntb.write(struct.pack("<L", 0x4))
        fntb.write(struct.pack("<H", 0x0))
        fntb.write(struct.pack("<H", 0x1))

    # FATB creation
    print("Making FATB...")
    with open(unpacked_narc.split("_")[0] + "_fatb.bin", "wb") as fatb:
        fatb.write(struct.pack("<L", 0x46415442))
        fatb.write(struct.pack("<L", 0x4 + 0x4 + 0x4 + (0x8 * len(file_sizes))))
        fatb.write(struct.pack("<L", len(file_sizes)))
        for x in range(0, len(file_sizes)):
            try:
                fatb.write(struct.pack("<L", file_sizes[x]))
                fatb.write(struct.pack("<L", file_sizes[x+1]))
            except IndexError:
                fatb.write(struct.pack("<L", fimg_end)) # We have reached the last offset

    # Bring it all together
    print("Making the NARC...")
    narc_data = b""
    with open(unpacked_narc.split("_")[0] + ".narc", "wb") as narc:
        narc.write(struct.pack("<L", 0x4352414E))
        narc.write(struct.pack("<L", 0x0100FFFE))
        fimg = open(os.path.join(os.getcwd(), unpacked_narc.split("_")[0] + "_fimg.bin"), "rb")
        fntb = open(os.path.join(os.getcwd(), unpacked_narc.split("_")[0] + "_fntb.bin"), "rb")
        fatb = open(os.path.join(os.getcwd(),unpacked_narc.split("_")[0] + "_fatb.bin"), "rb")
        narc_data += fatb.read()
        narc_data += fntb.read()
        narc_data += fimg.read()
        size = 0x10 + len(narc_data)
        narc.write(struct.pack("<L", size))
        narc.write(struct.pack("<H", 0x10))
        narc.write(struct.pack("<H", 0x3))
        narc.write(narc_data)
        fatb.close()
        fntb.close()
        fimg.close()

    # Cleanup
    try:
        os.remove(unpacked_narc.split("_")[0] + "_fimg.bin")
        os.remove(unpacked_narc.split("_")[0] + "_fntb.bin")
        os.remove(unpacked_narc.split("_")[0] + "_fatb.bin")
    except FileNotFoundError:
        pass

    # Done!
    print("Done!")
