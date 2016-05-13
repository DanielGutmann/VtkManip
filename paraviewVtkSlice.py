from paraview import simple as pvs

#________________________
#---- Some parameters

_colourScale = [1, 1, 0.52549, 0.709804,
               8.4698, 0.956863, 0.18314, 0.623529,
               15, 0.494118, 0.305882, 0.752941]

_opacityScale = [1.0, 0, 0.5, 0,
                3.44295, 0.6625, 0.5, 0,
                6.63758, 0.8975, 0.5, 0,
                15., 1, 0.5, 0]

_zoom = 1.3 #<--- Camera zoom

#________________________
def ProcessVtk(vtkFileName, #<--- Input VTK file name
               pngFileName, #<--- Output png** file name (**actually can be any supported format)
               origin    = [0, 0, 0],
               normal    = [1, 0, 0],
               cameraPos = [-1, 0 ,0]):


    #---- Read the vtk file
    vtkreader = pvs.LegacyVTKReader(FileNames = [vtkFileName])
    print "Got vtk",vtkFileName
    
    #---- make the slice
    slicer = pvs.Slice(Input=vtkreader, SliceType="Plane")
    slicer.SliceType.Origin = origin
    slicer.SliceType.Normal = normal
    
    #---- position camera
    view = pvs.GetActiveView()
    if not view:
        #---- When using the ParaView UI, the View will be present, not otherwise.
        view = pvs.CreateRenderView()
    view.CameraViewUp = [0, 1, 0]
    view.CameraFocalPoint = [0, 0, 0]
    view.CameraViewAngle = 45
    view.CameraPosition = cameraPos
    
    #---- Draw the object
    pvs.Show(slicer)
    
    #---- Edit props
    view.Background = [1,1,1]  #---- white
    view.OrientationAxesVisibility = 0
    pvs.ResetCamera()
    
    #---- Set colour scale
    dp = pvs.GetDisplayProperties(slicer)
    #r = vtkreader.PointData["volume_scalars"].GetRange() #<--- This is how you would get the full voxel data range
    dp.LookupTable = pvs.GetLookupTableForArray('volume_scalars', 1,
                                                RGBPoints = _colourScale,
                                                ColorSpace = 'Diverging')
    dp.ColorArrayName = 'volume_scalars'
    dp.LookupTable.LockDataRange = 1
    dp.LookupTable.EnableOpacityMapping = 1
    
    #---- Set opacity scale
    op = pvs.GetOpacityTransferFunction('volume_scalars')
    op_points = op.GetProperty('Points')
    op.SetPropertyWithName('Points',_opacityScale)
    
    #---- To render the result, do this:
    camera = pvs.GetActiveCamera()
    camera.Zoom(_zoom)
    pvs.Render()
    
    #---- Write output
    pvs.WriteImage(pngFileName)
    
    #---- Clean up on behalf of ParaView
    Delete(slicer)
    Delete(vtkreader)
    del slicer
    del vtkreader
