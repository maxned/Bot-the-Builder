# Running GUI (Python 2.x )

Libraries Needed:
---
1. `tkinter`
2. `numpy`
3. `matplotlib`
 
 These library can be installed with the *libraryInstall* script in this repo using: <br/>
 `bash libraryInstall.sh` <br/>

 Using `GUI.py`
---
1. Ensure that you have the following files in this directory - `K_5.csv`, `K_10.csv`, `K_15.csv`, `K_20.csv`,
which will be output from running KNN.py in the KNN Classification folder.
2. Type the following command - `python3 GUI.py`.
3. The four graphs in the GUI are dynamically updated, so we can add new `.csv` files and update the plots.
4. In order to use the matplotlib controls in the corner, use the `Pause Animation` button to enable live-updating
of the graphs. Be sure to use the `Resume Animation` button to enable live-updating once you are done using controls.
