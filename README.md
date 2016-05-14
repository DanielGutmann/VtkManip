# VtkManip
Some general python scripts to manipulate VTK legacy format files

## paraviewVtkSlice.py
A script containing a function that slices legacy VTK files using ParaView, producing a image output. The function takes inputs of:

* An input legacy VTK file name
* An output image file name (assumed lazily to be png, although no errors will crop up if you choose another valid format)
* Slice origin and normal vectors (python lists in the form [x,y,z])
* The camera position, again as a vector (python list in the form [x,y,z])

Note: there are some hard-coded variables, such as the camera zoom, color scale (set in the range 1-15) and the image opacity scale. If you want to make the scipt more general, please feel free to commit changes but try to ensure backwards compatibility.


## VtkManip.py
This is a utility for performing basic arithmetic-like operations on VTK legacy files. Effectively the code treats the VTK file as a column vector.
There are functions to perform {addition, subtraction, multiplication, division} operations, to rotate VTK legacy files about the central axis by 90&deg, as well as the ability to average an arbitrarily long list of VTK legacy files. The output is a new VTK legacy file, and the original files are unchanged. You can use the following python script (without needing to know anything about python):

* For {addition, subtraction, multiplication, division} eg:
  python VtkManip.py --add --vtk1=’/path/to/file1.vtk’ --vtk2=’/path/to/file2.vtk’ --outname="out.vtk"
\t where ~~~--add~~~ can be replaced by {~~~--subtract~~~,~~~--multiply~~~ or ~~~--divide~~~}. In the above examples, you can also replace the second file with a number (in order to perform scalings etc), eg --vtk2=1.44. For a given operator {addition, subtraction, multiplication, division}, the first vtk (vtk1) file acts from the left of the operator and the second vtk file acts from the right of the operator (vtk2).

* Average a list of files (Note: accepts ~~~*~~~ wildcarding):
  python VtkManip.py --average --vtk1='/path/to/file1.vtk,/path/to/multiple*files.vtk,/path/to/file2.vtk' --outname="out.vtk"

* Rotate a file by 90&deg:
  python VtkManip.py --rotate --vtk1=’/path/to/file1.vtk’ --outname="out.vtk"