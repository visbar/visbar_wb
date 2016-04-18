import vtk
 
# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.SetOffScreenRendering(True)
renWin.AddRenderer(ren)
 
# create source
source = vtk.vtkSphereSource()
source.SetCenter(0,0,0)
source.SetRadius(5.0)
 
# mapper
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(source.GetOutput())
else:
    mapper.SetInputConnection(source.GetOutputPort())
 
# actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
 
# assign actor to the renderer
ren.AddActor(actor)
 
# enable user interface interactor
renWin.Render()
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.Update()
writer = vtk.vtkPNGWriter()
writer.SetFileName("Sphere.png")
if vtk.VTK_MAJOR_VERSION <= 5:
    writer.SetInput(w2if.GetOutput())
else:
    writer.SetInputConnection(w2if.GetOutputPort())
writer.Write()
renWin.Finalize()
ren.RemoveAllLights()
