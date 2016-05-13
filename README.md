# VtkManip
Some general python scripts to manipulate VTK legacy format files

## paraviewVtkSlice.py
A script containing a function that slices legacy VTK files using ParaView, producing a image output. The function takes inputs of:

* An input legacy VTK file name
* An output image file name (assumed lazily to be png, although no errors will crop up if you choose another valid format)
* Slice origin and normal vectors (python lists in the form [x,y,z])
* The camera position, again as a vector (python list in the form [x,y,z])

Note: there are some hard-coded variables, such as the camera zoom, color scale (set in the range 1-15) and the image opacity scale. If you want to make the scipt more general, please feel free to commit changes but try to ensure backwards compatibility.