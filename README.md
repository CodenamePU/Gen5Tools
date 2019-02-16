# Gen5Tools
Tools for hacking Generation 5 of Pokémon.

### Requirements:
* [Python 3.4+](https://www.python.org)
* [devkitARM](https://github.com/devkitPro/installer/releases)

### Usage

#### NARCTool (only for Pokémon games).
* To decompile:
```python NARCTool.py extract <NARC> <output directory>```

* To compile:
```python NARCTool.py compile <extracted NARC> <output directory>```

**Please note: all files will be compressed/decompressed when running these operations. Double compression will happen. To prevent this, edit the `lz.cfg` present in the extracted NARC directory, and remove the files which have been compressed. I will implement a solution as soon as I think of one.**

#### CheapScript - DS Generation Scripting Made Easy!
See [here](https://github.com/CodenamePU/CheapScript).

#### CheapTrainer - DS Generation Trainer Editing Made Easy!
Still in development, not ready for use yet.

#### CheapFurniture - DS Generation Event Editing Made Easy!
**Very experimental. The struct is not completely figured out (help on this would be appreciated), and it is not dynamic in terms of sizing (you will have to state a fixed size every time). You have been warned.**

* Extract the overworld NARC a1/2/6.
* Feed the script one of the files: 
  ```python CheapFurniture.py decompile 126_xxx.bin```
* Make your changes.
* Recompile (**Make sure you have the b2w2.s in the same directory.**):
  ```python CheapFurniture.pycompile 126_xxx.s``` 
* Reinsert to NARC, reinsert NARC into ROM.
* Profit!

# Credits
* Kaphotics and pichu2001 - Some scripting research for Generation 5.
* Barubary - DSDecmp
* KazoWAR - Finding the trdata/trpoke structures for Generation 5.

Anyone else I forgot? Let me know!
