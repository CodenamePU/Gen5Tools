# Gen5Tools
Tools for hacking Generation 5 of Pokémon.

## Usage

### CheapScript - DS Generation Scripting Made Easy!
See [here](https://github.com/CodenamePU/CheapScript).

### CheapTrainer - DS Generation Trainer Editing Made Easy!
Still in development, not ready for use yet.

### CheapFurniture - DS Generation Event Editing Made Easy!
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
