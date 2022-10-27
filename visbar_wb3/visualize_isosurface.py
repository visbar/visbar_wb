# Interaction with an Isosurface visualization
#import module
import os,sys
import re
from vtk import*
import library as lib
import math,shutil




#########################################
def setting_read():
    files = os.listdir(prog_dir_path)
    for filenametxt in files :
        if filenametxt.find("visbar_wb_setting_default.txt") >= 0:
            try:
                setting_file_name = prog_dir_path + "/visbar_wb_setting_default.txt"
            except:
                setting_file_name = prog_dir_path + "\visbar_wb_setting_default.txt"

    ###############################################
            f = open(setting_file_name,'r')
            a=1
            cnt=0
            dic={}
            while True:
                findsharp=-1
                line = f.readline()
                #line = f.read()
                if line.find("--end_setting--") >=0 :
                    break
            ####################################
                all_line=[]
                line = line.replace("\t"," ")
                line = line.rstrip()
                line = re.sub("\n","",line)
                #line = re.split(" *",line)
                line = line.split()
                #print(line)
            ####################################
                if len(line) == 0:
                    continue
                if line[0].find("#") >=0:
                    continue
            ####################################
                all_line += line
                del all_line[0]
                for i in range(0,len(all_line)):
                        if all_line[i].find("#") >=0:
                            findsharp=i
                if findsharp >=0:
                    del all_line[findsharp:]
                    if len(all_line) ==0:
                        print("Dictionary isn't possible" +" "+ "["+line[0]+"]")
                        continue
            ###################################
                para=[]
                para += all_line
                dic[line[0]]=para
            f.close()
            pwd = os.getcwd()
            pwd_files = os.listdir(pwd)
            if "visbar_wb_setting.txt" in pwd_files >= 0:
                setting_file_name = "visbar_wb_setting.txt"
    ###############################################
                f = open(setting_file_name,'r')
                a=1
                cnt=0
                dic2={}
                while True:
                    findsharp=-1
                    line = f.readline()
                    #line = f.read()
                    if line.find("--end_setting--") >=0 :
                        break
                ####################################
                    all_line=[]
                    line = line.replace("\t"," ")
                    line = line.rstrip()
                    line = re.sub("\n","",line)

                    #line = re.split(" *",line)
                    line = line.split()
                ####################################
                    if len(line) == 0:
                        continue
                    if line[0].find("#") >=0:
                        continue
                ####################################
                    all_line += line
                    del all_line[0]
                    for i in range(0,len(all_line)):
                        if all_line[i].find("#") >=0:
                            findsharp=i
                    if findsharp >=0:
                        del all_line[findsharp:]
                        if len(all_line) ==0:
                            print("Dictionary isn't possible" +" "+ "["+line[0]+"]")
                            continue
                ###################################
                    para=[]
                    para += all_line
                    dic2[line[0]]=para
                    dic.update(dic2)
                del files,para,findsharp,all_line,pwd,pwd_files,a,cnt,setting_file_name
                return dic
#########################################################
def setting_bond():
    try:
        f = open(prog_dir_path + "/bond_length.txt",'r')
    except:
        f = open(prog_dir_path + "\bond_length.txt",'r')
    a=1
    cnt=0
    dic={}
    while True:
            findsharp=-1
            line = f.readline()
            #line = f.read()
            if line.find("--end_setting--") >=0 :
                break
            all_line=[]
            line = line.replace("\t"," ")
            line = line.rstrip()
            line = re.sub("\n","",line)
            #line = re.split(" *",line)
            line = line.split()
            ####################################
            if len(line) == 0:
                continue
            if line[0].find("#") >=0:
                continue
            ####################################
            all_line += line
            del all_line[0:2]
            for i in range(0,len(all_line)):
                if all_line[i].find("#") >=0:
                    findsharp=i
            if findsharp >=0:
                del all_line[findsharp:]
                if len(all_line) ==0:
                    print("Dictionary isn't possible" +" "+ "["+line[0]+"]")
                    continue
            ###################################
            dic[line[0],line[1]]=line[2]
    #f.close()
            #del all_line,findsharp,a,cnt,line
            del all_line,findsharp,line
    del a,cnt
    return dic
##############################################################

prog_dir_path = os.path.dirname(sys.argv[0])
if prog_dir_path == "":
    prog_dir_path = "./"
read=setting_read()
read_bond=setting_bond()
save_step = 0
##############################################################
with open("visbar_wb_setting_default.txt") as setting:
    value_seting = setting.read()
    value_seting = value_seting.split()
    #print(value_setting)
##############################################################
isovalue=float(value_seting[2])
stableiso=float(value_seting[2])
isovalueminus=float(value_seting[4])
stableisominus=float(value_seting[4])
PositiveLevel=0
NegativeLevel=0
def vtk(output_dir,filenametext,Batch_mode,Input_dir):
   ###########################################
         ######if you push "u" save png screen shot#################
    save_step = 0
    def userMethod(obj, arg):
        global save_step
        print("Save Figure")
        isosurface.SetValue(0,stableiso)
        isosurfaceminus.SetValue(0,stableisominus)
        renWin.Render()
        windowToImageFilter=vtkWindowToImageFilter()
        windowToImageFilter.SetInput(renWin)
        windowToImageFilter.Update()
        pngWriter=vtkPNGWriter()
        if VTK_MAJOR_VERSION <= 5:
            pngWriter.SetInput(windowToImageFilter.GetOutput())
        else:
            pngWriter.SetInputData(windowToImageFilter.GetOutput())
        pngWriter.SetFileName("image"+ str(save_step) +".png")
        pngWriter.Write()
        save_step += 1
  ##########################################################
######if you push "c" save this setting now############
    def setting_write():
        print("Output Setting File")
        isosurface.SetValue(0,stableiso)
        isosurfaceminus.SetValue(0,stableisominus)
        renWin.Render()
        out = open("visbar_wb_setting_output.txt",'w')
        out.write('#---IsoValue---#' + '\n')
        out.write('IsoValuePositive' +' '+ str(isovalue*(1.01**PositiveLevel)) + '\n')
        out.write('IsoValueNegative'+' '+ str(isovalueminus*(1.01**NegativeLevel)) + '\n')
        out.write('IsoOpacityPositive'+' '+ str(isosurfaceActor.GetProperty().GetOpacity()) + '\n')
        out.write('IsoOpacityNegative'+' '+ str(isosurfaceminusActor.GetProperty().GetOpacity()) + '\n')
        out.write('DrawIsoInWirePositive'+' '+ "Off" + '\n')
        out.write('DrawIsoInWireNegative'+' '+ "Off" + '\n')
        out.write('\n' + '#---Color---#' + '\n')
        out.write('IsoColorPositive'+' '+ str(value_seting[15])
                                    +' '+ str(value_seting[16])
                                    +' '+ str(value_seting[17])+ '\n')
        out.write('IsoColorNegative'+' '+ str(value_seting[19])
                                    +' '+ str(value_seting[20])
                                    +' '+ str(value_seting[21])+ '\n')
        out.write('OutLineColor'+' '+ str( outlineActor.GetProperty().GetAmbientColor()[0])\
                                +' '+ str( outlineActor.GetProperty().GetAmbientColor()[1])\
                                +' '+ str( outlineActor.GetProperty().GetAmbientColor()[2])+ '\n')
        out.write('BackGroundColor'+' '+str(ren.GetBackground()[0])
                                   +' '+str(ren.GetBackground()[1])
                                   +' '+str(ren.GetBackground()[2])+ '\n')
        out.write('\n' + '#---WindowSize---#' + '\n')
        out.write('WindowSize'  +' '+ str(renWin.GetSize()[0])\
                                +' '+ str(renWin.GetSize()[1])+ '\n')
        """
        out.write('isominusR'   +' '+str(isominusR)+ '\n')
        out.write('isominusG'   +' '+str(isominusG)+ '\n')
        out.write('isominusB'   +' '+str(isominusB)+ '\n')
        out.write('isoplusR'    +' '+str(isoplusR)+ '\n')
        out.write('isoplusG'    +' '+str(isoplusG)+ '\n')
        out.write('isoplusB'    +' '+str(isoplusB)+ '\n')
        """
        out.write('\n' + '#---Camera---#' + '\n')
        out.write('FocalPoint'+' '+str(camera.GetFocalPoint()[0])
                              +' '+str(camera.GetFocalPoint()[1])
                              +' '+str(camera.GetFocalPoint()[2])+ '\n')
        out.write('CameraPosition'  +' '+str(camera.GetPosition()[0])
                                    +' '+str(camera.GetPosition()[1])
                                    +' '+str(camera.GetPosition()[2])+ '\n')
        out.write('ParallelScale'+' '+str(camera.GetParallelScale())+ '\n')
        out.write('ViewUp'    +' '+str(camera.GetViewUp()[0])
                              +' '+str(camera.GetViewUp()[1])
                              +' '+str(camera.GetViewUp()[2])+ '\n')
        out.write('ClippingRange'+' '+str(camera.GetClippingRange()[0])
                                 +' '+str(camera.GetClippingRange()[1])+ '\n')
        out.write('\n' + '#---Label---#' + '\n')
        out.write('#NumberOnly:1' + '\n' +'#ElementOnly:2' + '\n' +'#EachNumber+Element:3' + '\n' +'#SerialNumber+Element:4' + '\n' + 'LabelType 4' + '\n')

        out.write('\n' + '#---DrawObject---#' + '\n')
        all_parts=["DrawBond","DrawAtom","DrawWaveFunction","DrawOutLine","DrawAxis","DrawText","DrawAtomLabel","WatchParallelView"]
        isosurface.SetValue(0,stableiso)
        isosurfaceminus.SetValue(0,stableisominus)
        renWin.Render()
        for parts in all_parts:
            out.write(parts + " " + "On" +"\n")
        out.write('--end_setting--'+ '\n')
        out.close()




  ##########################################################


    ############################################

  # A reader
    input_filenametext = os.path.join(Input_dir,filenametext)
    output_filenametext = os.path.join(output_dir,filenametext)
    reader = vtkStructuredPointsReader()
    reader.SetFileName(input_filenametext[:-5] + '/VTK_out.vtk')

  # Create an outline of the dataset
    outline = vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())

    outlineMapper = vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())

    outlineActor = vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(float(value_seting[23]),
                                        float(value_seting[24]),
                                        float(value_seting[25]))   #OutLineColor


  # Color lookup table
    isominusR=float(value_seting[15])   #IsoColorPositive
    isominusG=float(value_seting[16])
    isominusB=float(value_seting[17])
    isoplusR=float(value_seting[19])   #IsoColorNegative
    isoplusG=float(value_seting[20])
    isoplusB=float(value_seting[21])



    #lut=vtkColorTransferFunction()
    #lut.AddRGBPoint(-0.1,isominusR,isominusG,isominusB)
    #lut.AddRGBPoint(-0.075,isominusR,isominusG,isominusB)
    #lut.AddRGBPoint(-0.05,isominusR,isominusG,isominusB)
    #lut.AddRGBPoint(-0.025,isominusR,isominusG,isominusB)
    #lut.AddRGBPoint(-0.001,isominusR,isominusG,isominusB)
    #lut.AddRGBPoint(0,1,0,0)
    #lut.AddRGBPoint(0.001,isoplusR,isoplusG,isoplusB)
    #lut.AddRGBPoint(0.025,isoplusR,isoplusG,isoplusB)
    #lut.AddRGBPoint(0.05,isoplusR,isoplusG,isoplusB)
    #lut.AddRGBPoint(0.075,isoplusR,isoplusG,isoplusB)
    #lut.AddRGBPoint(0.1,isoplusR,isoplusG,isoplusB)
  ############################################
  #VESTA_ver_color(lightblue&yellow)
    lut=vtkColorTransferFunction()
    lut.AddRGBPoint(-0.1,1,1,0.4)
    lut.AddRGBPoint(-0.075,1,1,0.4)
    lut.AddRGBPoint(-0.05,1,1,0.4)
    lut.AddRGBPoint(-0.025,1,1,0.4)
    lut.AddRGBPoint(-0.001,1,1,0.4)
    lut.AddRGBPoint(0,1,0,0)
    lut.AddRGBPoint(0.001,0.4,0.8,0.8)
    lut.AddRGBPoint(0.025,0.4,0.8,0.8)
    lut.AddRGBPoint(0.05,0.4,0.8,0.8)
    lut.AddRGBPoint(0.075,0.4,0.8,0.8)
    lut.AddRGBPoint(0.1,0.4,0.8,0.8)
  #############################################








  # Define initial iso value
    global isovalue
    global isovalueminus


  # The contour filter1
    isosurface = vtkContourFilter()
    isosurface.SetInputConnection(reader.GetOutputPort())
    isosurface.SetValue(0,isovalue)

    isosurfaceMapper = vtkPolyDataMapper()
    isosurfaceMapper.SetLookupTable(lut)
    isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())

    isosurfaceActor = vtkActor()
    isosurfaceActor.SetMapper(isosurfaceMapper)
    isosurfaceActor.GetProperty().SetOpacity(float(value_seting[6]))  #IsoOpacityPositive
    if value_seting[10] == "On":   #DrawIsoInWirePositive
        isosurfaceActor.GetProperty().SetRepresentationToWireframe()


  # The contour filter2(minus)
    isosurfaceminus = vtkContourFilter()
    isosurfaceminus.SetInputConnection(reader.GetOutputPort())
    isosurfaceminus.SetValue(0,isovalueminus)

    isosurfaceminusMapper = vtkPolyDataMapper()
    isosurfaceminusMapper.SetLookupTable(lut)
    isosurfaceminusMapper.SetInputConnection(isosurfaceminus.GetOutputPort())

    isosurfaceminusActor = vtkActor()
    isosurfaceminusActor.SetMapper(isosurfaceminusMapper)
    isosurfaceminusActor.GetProperty().SetOpacity(float(value_seting[8]))   #IsoOpacityNegative

    if value_seting[12] == "On":    #DrawIsoInWireNegative
        isosurfaceminusActor.GetProperty().SetRepresentationToWireframe()

  # Renderer and render window
    ren = vtkRenderer()
    ren.SetBackground(float(value_seting[27]),
                      float(value_seting[28]),
                      float(value_seting[29]))    #BackGroundColor




  #ren.SetBackground(.8, .8, .8)



  #read file & list in atomdata
  #============================================
    try:
        f=open(input_filenametext[:-5] + '/make_atom.xyz.txt','r')
    except:
        f=open(input_filenametext[:-5] + '\make_atom.xyz.txt','r')
    atom_list=[]
    number=f.readline()
    comment=f.readline()
    for j in range(0,int(number)):
        atom = f.readline()
        atom = atom.rstrip()
        atom = re.sub("\n","",atom)
        #atom = re.split(" *",atom)
        atom = atom.split()
        atom_list +=[atom]
    #print(atom_list)
    f.close()
  #============================================


  #add the some atom
  #============================================
    for k in range(0,int(number)):
      # create source
        source0 = vtkSphereSource()
        source0.SetCenter(float(atom_list[k][1]),float(atom_list[k][2]),float(atom_list[k][3]))
        source0.SetRadius(float(lib.library[atom_list[k][0]][1]))
        source0.SetThetaResolution(15)
        source0.SetPhiResolution(15)

      # mapper
        mapper0 = vtkPolyDataMapper()
        if VTK_MAJOR_VERSION <= 5:
            mapper0.SetInput(source0.GetOutput())
        else:
            mapper0.SetInputConnection(source0.GetOutputPort())
      # actor
        actor0 = vtkActor()
        actor0.SetMapper(mapper0)
        actor0.GetProperty().SetColor(lib.library[atom_list[k][0]][2][0]/255,lib.library[atom_list[k][0]][2][1]/255,lib.library[atom_list[k][0]][2][2]/255)
      # assign actor to the renderer
        if value_seting[63] == "On":   #DrowAtom
            ren.AddActor(actor0)

####----------label--------####
    pd = vtkPolyData()
    pts = vtkPoints()
    orient = vtkDoubleArray()
    orient.SetName('orientation')
    label = vtkStringArray()
    label.SetName('label')
    for k in range(0,int(number)):
        pts.InsertNextPoint(float(atom_list[k][1]),float(atom_list[k][2]),float(atom_list[k][3]))
        label.InsertNextValue(str(atom_list[k][4]))
    pd.SetPoints(pts)
    pd.GetPointData().AddArray(label)
    pd.GetPointData().AddArray(orient)
    hier = vtkPointSetToLabelHierarchy()

    if VTK_MAJOR_VERSION <= 5:
        hier.SetInput(pd)
    else:
        hier.SetInputData(pd)

    hier.SetOrientationArrayName('orientation')
    hier.SetLabelArrayName('label')
    hier.GetTextProperty().SetColor(0.0, 0.0, 0.0)
    lmapper = vtkLabelPlacementMapper()
    lmapper.SetInputConnection(hier.GetOutputPort())
    lmapper.SetShapeToRoundedRect()
    lmapper.SetBackgroundColor(1.0, 1.0, 0.7)
    lmapper.SetBackgroundOpacity(0.8)
    lmapper.SetMargin(3)
    lactor = vtkActor2D()
    lactor.SetMapper(lmapper)
    if value_seting[73] == "On":   #DrawAtomLabel
        ren.AddActor(lactor)
#==============================================











  #add the some bond
#==============================================
    all_atom=atom_list
    del atom_list
    for i in range(0,int(number)-1):
        for j in range(i+1,int(number)):
            all_atom[i][1]=float(all_atom[i][1])
            all_atom[i][2]=float(all_atom[i][2])
            all_atom[i][3]=float(all_atom[i][3])
            all_atom[j][1]=float(all_atom[j][1])
            all_atom[j][2]=float(all_atom[j][2])
            all_atom[j][3]=float(all_atom[j][3])
###########################################
            length =  ((all_atom[j][1] - all_atom[i][1])**2.0\
                      +(all_atom[j][2] - all_atom[i][2])**2.0\
                      +(all_atom[j][3] - all_atom[i][3])**2.0)**0.5
            #print(read_bond[all_atom[i][0],all_atom[j][0]])
            if length <= float(read_bond[all_atom[i][0],all_atom[j][0]]):
                radius=0.1
                res=10
                axis=[all_atom[i][1]-all_atom[j][1],all_atom[i][2]-all_atom[j][2],all_atom[i][3]-all_atom[j][3]]
      #print axis
                pos=[(all_atom[i][1]+all_atom[j][1])/2.0,(all_atom[i][2]+all_atom[j][2])/2.0,(all_atom[i][3]+all_atom[j][3])/2.0]
      #print pos
                height=math.sqrt(axis[0]**2+axis[1]**2+axis[2]**2)
                theta = math.acos(axis[1] / height)
      #print theta
                v=[axis[2], 0, -axis[0]]
                cylinder = vtkCylinderSource()
                cylinder.SetResolution(res)
                cylinder.SetHeight(height)
                cylinder.SetRadius(radius)
                mapper = vtkPolyDataMapper()
                if VTK_MAJOR_VERSION <= 5:
                    mapper.SetInput(cylinder.GetOutput())
                else:
                    mapper.SetInputConnection(cylinder.GetOutputPort())

                actor = vtkActor()
                actor.SetMapper(mapper)
                actor.RotateWXYZ(theta / math.pi * 180, v[0], v[1], v[2])
      #print "AAA",theta / math.pi * 180, v[0], v[1], v[2]
                actor.SetPosition(pos)
                if value_seting[61] == "On":  #DrawBond
                    ren.AddActor(actor)
    del all_atom


  #Camera---------------------------------------#
    camera=vtkCamera()
    camera.SetFocalPoint(float(value_seting[36]),
                         float(value_seting[37]),
                         float(value_seting[38]))
    camera.SetPosition(float(value_seting[40]),
                       float(value_seting[41]),
                       float(value_seting[42]))
    camera.ComputeViewPlaneNormal
    camera.SetParallelScale(float(value_seting[44]))
    camera.SetViewUp(float(value_seting[46]),
                     float(value_seting[46]),
                     float(value_seting[46]))
    camera.UseHorizontalViewAngleOff
    camera.SetClippingRange(float(value_seting[50]),
                            float(value_seting[51]))
    ren.SetActiveCamera(camera)
    if value_seting[75] == "On":   #WatchParallelView
        ren.GetActiveCamera().ParallelProjectionOn()

  #create a text actor######################################
  #print comment
    txt = vtkTextActor()
    txt.SetInput(comment)
    txtprop=txt.GetTextProperty()
    txtprop.SetFontFamilyToArial()
    #txtprop.SetBold(1)
    #txtprop.SetItalic(1)
    txtprop.SetFontSize(16)
    txtprop.SetColor(0,0,0)
    txt.SetDisplayPosition(30,450)
    #txt.SetDisplayPosition(80,470)
    #txt.SetDisplayPosition(10,470)
    #ren.AddActor(txt)
  #----------------------------
    comment2=filenametext
    txt2 = vtkTextActor()
    txt2.SetInput(comment2)
    txtprop2=txt2.GetTextProperty()
    txtprop2.SetFontFamilyToArial()
    txtprop2.SetFontSize(10)
    txtprop2.SetColor(0,0,0)
    #txt2.SetDisplayPosition(60,470)
    #txt.SetDisplayPosition(10,470)
    ren.AddActor(txt2)
    #===text_wiget===#
    text_representation = vtkTextRepresentation()
    text_representation.GetPositionCoordinate().SetValue(0.05, 0.85)
    text_representation.GetPosition2Coordinate().SetValue(0.8, 0.1)
    text_widget = vtkTextWidget()
    text_widget.SetRepresentation(text_representation)



  ###########################################################

  # Add the actors
    if value_seting[67] == "On":   #DrawOutline
        ren.AddActor(outlineActor)
    ###############################
    if value_seting[65] == "On":   #DrawWaveFunction
        ren.AddActor(isosurfaceActor)
        ren.AddActor(isosurfaceminusActor)
    ###############################
    renWin = vtkRenderWindow()
    if Batch_mode:
        renWin.SetOffScreenRendering(True)
    else:
        renWin.SetOffScreenRendering(False)

    renWin.SetWindowName("VisBAR wave batch")
    #renWin.SetSize(float(read["Window_size"][0]),
    #               float(read["Window_size"][1]))
    renWin.SetSize(int(value_seting[32]),
                   int(value_seting[33]))   #WindowSize

    renWin.AddRenderer(ren)

  ####Python function for the keyboard interface###
    def Keypress(obj, event):
        global isovalue,isovalueminus,PositiveLevel,NegativeLevel,stableiso,stableisominus
        key = obj.GetKeySym()
        if key == "4":
            PositiveLevel += 1
            stableiso = isovalue*(1.01**PositiveLevel)
            print("-----------------------------------")
            print("[PositiveLevel,PositiveValue =" ,PositiveLevel,",",stableiso,"]")
            print("[NegativeLevel,NegativeValue =" ,NegativeLevel,",",stableisominus,"]")
        elif key == "5":
            PositiveLevel -= 1
            stableiso = isovalue*(1.01**PositiveLevel)
            print("-----------------------------------")
            print("[PositiveLevel,PositiveValue =" ,PositiveLevel,",",stableiso,"]")
            print("[NegativeLevel,NegativeValue =" ,NegativeLevel,",",stableisominus,"]")
        elif key == "6":
            NegativeLevel += 1
            stableisominus = isovalueminus*(1.01**NegativeLevel)
            print("-----------------------------------")
            print("[PositiveLevel,PositiveValue =" ,PositiveLevel,",",stableiso,"]")
            print("[NegativeLevel,NegativeValue =" ,NegativeLevel,",",stableisominus,"]")
        elif key == "7":
            NegativeLevel -= 1
            stableisominus = isovalueminus*(1.01**NegativeLevel)
            print("-----------------------------------")
            print("[PositiveLevel,PositiveValue =" ,PositiveLevel,",",stableiso,"]")
            print("[NegativeLevel,NegativeValue =" ,NegativeLevel,",",stableisominus,"]")
        elif key == "1":
            PositiveLevel += 1
            NegativeLevel += 1
            stableiso = isovalue*(1.01**PositiveLevel)
            stableisominus = isovalueminus*(1.01**NegativeLevel)
            print("-----------------------------------")
            print("[PositiveLevel,PositiveValue =" ,PositiveLevel,",",stableiso,"]")
            print("[NegativeLevel,NegativeValue =" ,NegativeLevel,",",stableisominus,"]")
        elif key == "2":
            PositiveLevel -= 1
            NegativeLevel -= 1
            stableiso = isovalue*(1.01**PositiveLevel)
            stableisominus = isovalueminus*(1.01**NegativeLevel)
            print("-----------------------------------")
            print("[PositiveLevel,PositiveValue =" ,PositiveLevel,",",stableiso,"]")
            print("[NegativeLevel,NegativeValue =" ,NegativeLevel,",",stableisominus,"]")
        elif key == "0":
            PositiveLevel = 0
            NegativeLevel = 0
            stableiso = isovalue
            stableisominus = isovalueminus
            print("-----------------------------------")
            print("[PositiveLevel,PositiveValue =" ,PositiveLevel,",",stableiso,"]")
            print("[NegativeLevel,NegativeValue =" ,NegativeLevel,",",stableisominus,"]")
        elif key == "C":
            print(camera)
        elif key == "x":
            camera.SetPosition(45.0,0.0,0.0)
            camera.SetViewUp(0.0,1.0,0.0)
            camera.SetFocalPoint(0.0,-0.0382357,0.0)
            renWin.Render()
        elif key == "y":
            camera.SetPosition(0.0,45.0,0.0)
            camera.SetViewUp(0.0,0.0,-1.0)
            camera.SetFocalPoint(0.0,-0.0382357,0.0)
            renWin.Render()
        elif key == "z":
            camera.SetPosition(0.0,0.0,45.0)
            camera.SetViewUp(0.0,1.0,0.0)
            camera.SetFocalPoint(0.0,-0.0382357,0.0)
            renWin.Render()
        elif key == "c":
            setting_write()
        elif key == "Q":
            exit()

        elif key == "h":
            print("-----------------------------------")
            print("<<< How to Use VisBAR Wave Batch>>>")
            print("-----------------------------------")
            print()
            print("< Exit >")
            print("[Shift + q] Exit VisBAR Wave Batch")
            print("[e or q] Close current Window")
            print()
            print("< Mouse >")
            print("[Left Click] Rotate Object")
            print("[Right Click or Mouse wheel]  Zooming")
            print("[Press Mouse wheel] Parallel translation")
            print()
            print("< KeyBoard >")
            print("[j] Joystick mode, [t] Trackball mode")
            print("[w] Wireframe mode, [s] Surface mode")
            print("[r] Reset Scaling")
            print("[u] Save current figure to .png")
            print("[a] Select individual object")
            print("[x] Set camera direction to X axis")
            print("[y] Set camera direction to Y axis")
            print("[z] Set camera direction to Z axis")
            print()
            print("< Customize >")
            print("Press [c] Output Customize file. Filename is [visbar_wb_setting_output.txt]")
            print("Edit this file. And then, File rename [visbar_wb_setting.txt].  Restart VisBAR Wave Batch.")
            print()
            print("< Isovalue >")
            print("[1] PositiveLevel + 1 ,NegativeLevel + 1")
            print("[2] PositiveLevel - 1 ,NegativeLevel - 1")
            print("[4] PositiveLevel + 1")
            print("[5] PositiveLevel - 1")
            print("[6] NegativeLevel + 1")
            print("[7] NegativeLevel - 1")
            print("[0] Reset to the default Isovalue")
        elif key == "n" :  # Possibly change "p" to another key?
            print('n key pressed, show next')
            renWin.Finalize()  # Close the window.
            iren.ExitCallback()  # End interactive mode
            return  # quit from Keypress() before renWin.Render() is called.

        isosurface.SetValue(0,stableiso)
        isosurfaceminus.SetValue(0,stableisominus)
        renWin.Render()

  ##################################################




    if Batch_mode == False : #20150310
        w2if = vtkWindowToImageFilter()
        w2if.SetInput(renWin)
        w2if.Update()
        writer = vtkPNGWriter()
        if VTK_MAJOR_VERSION <= 5:
            writer.SetInput(w2if.GetOutput())
        else:
            writer.SetInputConnection(w2if.GetOutputPort())
        dst = os.path.splitext(output_filenametext)[0]
        dst = dst + ".png"
        writer.SetFileName( dst )
        renWin.Render()
        writer.Write()
        iren = vtkRenderWindowInteractor()
        iren.AddObserver("UserEvent", userMethod)
        iren.SetRenderWindow(renWin)
        iren.AddObserver("KeyPressEvent", Keypress)
        if value_seting[69] == "On":   #DrawAxis
            transform = vtkTransform()
            transform.Scale(5,5,5)
            transform.Translate(0.0,0.0,0.0)
            axes = vtkAxesActor()
            axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.0,0.0,0.0)
            axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.0,0.0,0.0)
            axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.0,0.0,0.0)
            axes.SetUserTransform(transform)
            axesWidget = vtkOrientationMarkerWidget()
            axesWidget.SetOrientationMarker(axes)
            axesWidget.SetInteractor(iren)
            axesWidget.EnabledOn()
            axesWidget.InteractiveOn()



        text_widget = vtkTextWidget()
        text_widget.SetRepresentation(text_representation)
        text_widget.SetInteractor(iren)
        text_widget.SetTextActor(txt)
        text_widget.SelectableOff()

        if value_seting[71] == "On":   #DrawText
            text_widget.On()




        iren.Initialize()
        iren.Start()

    elif Batch_mode == True :
        if value_seting[71] == "On":   #DrawText
            ren.AddActor(txt)
        w2if = vtkWindowToImageFilter()
        w2if.SetInput(renWin)
        writer = vtkPNGWriter()
        if VTK_MAJOR_VERSION <= 5:
            writer.SetInput(w2if.GetOutput())
        else:
            writer.SetInputConnection(w2if.GetOutputPort())
        dst = os.path.splitext(output_filenametext)[0]
        dst = dst + ".png"
        print(dst)
        writer.SetFileName( dst )
        writer.Write()
        renWin.Render()

        del w2if,dst

        renWin.Finalize()
        ren.RemoveAllLights()


        print("Batch_mode")

    else :
        print(" An unforeseen error")

    shutil.rmtree(input_filenametext[:-5])

if __name__ == "__main__":
    print("input_dir filename mode")
    argv = sys.argv
    input_dir = argv[1]
    files = os.listdir(input_dir)
    for f in files:
        if f.find(".cub") >= 0:
            vtk(input_dir,f,True)

