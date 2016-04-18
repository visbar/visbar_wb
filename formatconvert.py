#  import module and file open
import os
import re,sys
import library as lib
import visualize_isosurface as view

prog_dir_path = os.path.dirname(sys.argv[0])
if prog_dir_path == "":
    prog_dir_path = "./"

def mkdir2(outdir):
    if os.path.isdir(outdir):
        sys.stderr.write("output directory " + outdir + " already exists\n")
    else :
        os.mkdir(outdir)
#===first_loop===#
def cube_vtk(input_dir,filenametext,boundary_mode):
    filenametext = os.path.join(input_dir,filenametext)
    f = open(filenametext,'r')
    mkdir2(filenametext[:-5])
    out = open(filenametext[:-5] + '/make_atom.xyz.txt','w')


    #======In cube file data spilit=========
    cube_list=[]
    for j in xrange(0,6):
        cube_read = f.readline()
        cube_read += " " + cube_read
        cube_read = cube_read.rstrip()
        cube_read = re.sub("\n","",cube_read)
        cube_read = re.split(" *",cube_read)
        cube_list +=[cube_read]

    #=======================================
    #  Out cube to xyz
    new_cube = int(cube_list[2][1])*-1
    out.write(str(new_cube) + '\n')
    comment0=len(cube_list[0])
    comment1=len(cube_list[1])
    out.write("'")
    for com0 in xrange(0,comment0):
        out.write(str(cube_list[0][com0])+' ')
    for com1 in xrange(0,comment1):
        out.write(str(cube_list[1][com1])+' ')
    out.write("'"+'\n')
    #======In cube file atom data split=====
    all_atom=[]
    for j in xrange(0,new_cube):
        atomxyz = f.readline()
        atomxyz = atomxyz.rstrip()
        atomxyz = re.sub("\n","",atomxyz)
        atomxyz = re.split(" *",atomxyz)
        if atomxyz[0] != "":
            atomxyz = [" "] + atomxyz
        all_atom +=[atomxyz]
    #=======================================

    #========periodic_calc=================
    #print cube_list
    #print all_atom
    if boundary_mode == True:  #20150310
        for i in xrange(0,new_cube):
            if float(all_atom[i][3]) > float(cube_list[2][2])*(-1):
                kyori=(float(all_atom[i][3])-float(cube_list[2][2]))/(float(cube_list[2][2])*(-2))
                all_atom[i][3]=str(float(all_atom[i][3])+float(cube_list[2][2])*int(kyori)*2)




            elif float(all_atom[i][3]) < float(cube_list[2][2]):
                kyori=(float(all_atom[i][3])+float(cube_list[2][2]))/(float(cube_list[2][2])*(-2))
                all_atom[i][3]=str(float(all_atom[i][3])+float(cube_list[2][2])*int(kyori)*2)




            if float(all_atom[i][4]) > float(cube_list[2][3])*(-1):
                kyori=(float(all_atom[i][4])-float(cube_list[2][3]))/(float(cube_list[2][3])*(-2))
                all_atom[i][4]=str(float(all_atom[i][4])+float(cube_list[2][3])*int(kyori)*2)

            elif float(all_atom[i][4]) < float(cube_list[2][3]):
                kyori=(float(all_atom[i][4])+float(cube_list[2][3]))/(float(cube_list[2][3])*(-2))
                all_atom[i][4]=str(float(all_atom[i][4])+float(cube_list[2][3])*int(kyori)*2)

            if float(all_atom[i][5]) > float(cube_list[2][4])*(-1):
                kyori=(float(all_atom[i][5])-float(cube_list[2][4]))/(float(cube_list[2][4])*(-2))
                all_atom[i][5]=str(float(all_atom[i][5])+float(cube_list[2][4])*int(kyori)*2)

            elif float(all_atom[i][5]) < float(cube_list[2][4]):
                kyori=(float(all_atom[i][5])+float(cube_list[2][4]))/(float(cube_list[2][4])*(-2))
                all_atom[i][5]=str(float(all_atom[i][5])+float(cube_list[2][4])*int(kyori)*2)





    #======Out cube to xyz atomdata ========# #20150312
    elem_num_list = []
    elem_label = []
    read=view.setting_read()
    atom_lib = lib.library.items()
    for k in xrange(0,int(cube_list[2][1])*-1):
        for m in xrange(0,117):
            if atom_lib[m][1][0] == int(float(all_atom[k][1])):
                elem_num_list += atom_lib[m][0]
    for i,elem in enumerate(elem_num_list) :
        if read["LabelType"][0] == "1":
            elem_label += [str(i+1)]
        elif read["LabelType"][0] == "2":
            elem_label += [elem ]
        elif read["LabelType"][0] == "3":
            elem_label += [str(elem_num_list[0:i].count(elem)+1) + elem]
        elif read["LabelType"][0] == "4":
            elem_label += [str(i+1)+ elem ]
        else :
            elem_label += [str(i+1)+ elem ]

    for k in xrange(0,int(cube_list[2][1])*-1):
        for m in xrange(0,117):
            if atom_lib[m][1][0] == int(float(all_atom[k][1])):
                out.write(atom_lib[m][0]+' ')
            else: pass
        for l in xrange (3,7):
            if l==6:
                out.write(elem_label[k]+'\n')
            else:
                out.write(all_atom[k][l]+' ')


    #=======================================
    #file close
    out.close()
    f.close()








    #  file open
    f = open(filenametext,'r')
    out = open(filenametext[:-5] + '/convert_wave_function.vtk.txt','w')

    #======counter and skip data============
    for n in xrange(0,7+int(cube_list[2][1])*-1):
        f.readline()
    #=======================================



    #========Loop line & Mod line===========
    if int(cube_list[5][1])%6 == 0 :
        L = int(cube_list[5][1]) / 6

    elif int(cube_list[5][1])%6 != 0:
        L = int(cube_list[5][1]) / 6 + 1

    for xy in xrange(0, int(cube_list[3][1]) * int(cube_list[4][1])):
        for line_num_in_xy in xrange(0, L):
            line = f.readline()
            line = line.strip()
            if line == "":
                line = f.readline()
                line = line.strip()
            line = " ".join(map(lambda s: str(float(s)), re.split(" *", line)))  # Convert numerical format.
            out.write(line + " ")
        out.write("\n")
    out.close()
    f.close()




    #======Open file & wave function list in=======
    f = open(filenametext[:-5] + '/convert_wave_function.vtk.txt','r')
    out = open(filenametext[:-5] + '/VTK_out.vtk','w')
    total_line=[]
    for i in xrange (0,int(cube_list[3][1])):
        all_line=[]
        for j in xrange(0,int(cube_list[4][1])):
            line = f.readline()
            line = line.rstrip()
            line = re.sub("\n","",line)
            line = re.split(" ",line)
            all_line += [line]
        total_line += [all_line]
    #======================================

    #======Out file & wave function convert to VTKformat=======
    out.write('# vtk DataFile Version 2.0'+'\n')
    out.write('Probability density for the 3d electron position in a hydrogen atom'+'\n')
    out.write('ASCII'+'\n')
    out.write('DATASET STRUCTURED_POINTS'+'\n')
    out.write('DIMENSIONS'+' '+cube_list[3][1]+' '+cube_list[4][1]+' '+cube_list[5][1]+'\n')
    out.write('ORIGIN'+' '+cube_list[2][2]+' '+cube_list[2][3]+' '+cube_list[2][4]+'\n')
    out.write('SPACING'+' '+cube_list[3][2]+' '+cube_list[4][3]+' '+cube_list[5][4]+'\n')
    out.write('POINT_DATA'+' '+str(int(cube_list[3][1])*int(cube_list[4][1])*int(cube_list[5][1]))+' '+'\n')
    out.write('SCALARS probability_density float'+'\n')
    out.write('LOOKUP_TABLE default'+'\n')
    for k in xrange (0,int(cube_list[5][1])):
        for j in xrange (0,int(cube_list[4][1])):
            for i in xrange (0,int(cube_list[3][1])):
                if i==(int(cube_list[3][1])-1):
                    out.write(total_line[i][j][k]+'\n')
                else:
                    out.write(total_line[i][j][k]+' ')
    out.close()
    f.close()

    print "convert end"
    del line,all_line,elem_label,elem,elem_num_list
    del cube_list,cube_read,atomxyz,read
    return total_line
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################



#===since_second_loop===#
def cube_vtk2(input_dir,filenametext,check_line,boundary_mode):
    filenametext = os.path.join(input_dir,filenametext)
    f = open(filenametext,'r')
    mkdir2(filenametext[:-5])
    out = open(filenametext[:-5] + '/make_atom.xyz.txt','w')


    #======In cube file data spilit=========
    cube_list=[]
    for j in range(0,6):
        cube_read = f.readline()
        cube_read = cube_read.rstrip()
        cube_read = re.sub("\n","",cube_read)
        cube_read = re.split(" *",cube_read)
        cube_list +=[cube_read]

    #=======================================
    #  Out cube to xyz
    new_cube = int(cube_list[2][1])*-1
    out.write(str(new_cube) + '\n')
    comment0=len(cube_list[0])
    comment1=len(cube_list[1])
    out.write("'")
    for com0 in range(0,comment0):
        out.write(str(cube_list[0][com0])+' ')
    for com1 in range(0,comment1):
        out.write(str(cube_list[1][com1])+' ')
    out.write("'"+'\n')
    #======In cube file atom data split=====
    all_atom=[]
    for j in range(0,new_cube):
        atomxyz = f.readline()
        atomxyz = atomxyz.rstrip()
        atomxyz = re.sub("\n","",atomxyz)
        atomxyz = re.split(" *",atomxyz)
        if atomxyz[0] != "":
            atomxyz = [" "] + atomxyz
        all_atom +=[atomxyz]
    #=======================================

    if boundary_mode == "True":

        for i in range(0,new_cube):
            if float(all_atom[i][3]) > float(cube_list[2][2])*(-1):
                kyori=(float(all_atom[i][3])-float(cube_list[2][2]))/(float(cube_list[2][2])*(-2))
                all_atom[i][3]=str(float(all_atom[i][3])+float(cube_list[2][2])*int(kyori)*2)





            elif float(all_atom[i][3]) < float(cube_list[2][2]):
                kyori=(float(all_atom[i][3])+float(cube_list[2][2]))/(float(cube_list[2][2])*(-2))
                all_atom[i][3]=str(float(all_atom[i][3])+float(cube_list[2][2])*int(kyori)*2)




            if float(all_atom[i][4]) > float(cube_list[2][3])*(-1):
                kyori=(float(all_atom[i][4])-float(cube_list[2][3]))/(float(cube_list[2][3])*(-2))
                all_atom[i][4]=str(float(all_atom[i][4])+float(cube_list[2][3])*int(kyori)*2)

            elif float(all_atom[i][4]) < float(cube_list[2][3]):
                kyori=(float(all_atom[i][4])+float(cube_list[2][3]))/(float(cube_list[2][3])*(-2))
                all_atom[i][4]=str(float(all_atom[i][4])+float(cube_list[2][3])*int(kyori)*2)

            if float(all_atom[i][5]) > float(cube_list[2][4])*(-1):
                kyori=(float(all_atom[i][5])-float(cube_list[2][4]))/(float(cube_list[2][4])*(-2))
                all_atom[i][5]=str(float(all_atom[i][5])+float(cube_list[2][4])*int(kyori)*2)

            elif float(all_atom[i][5]) < float(cube_list[2][4]):
                kyori=(float(all_atom[i][5])+float(cube_list[2][4]))/(float(cube_list[2][4])*(-2))
                all_atom[i][5]=str(float(all_atom[i][5])+float(cube_list[2][4])*int(kyori)*2)






    #======Out cube to xyz atomdata ========0 #20150312
    elem_num_list = []
    elem_label = []
    read=view.setting_read()
    for k in range(0,int(cube_list[2][1])*-1):
        for m in range(0,117):
            if lib.library.items()[m][1][0] == int(float(all_atom[k][1])):
                elem_num_list += lib.library.items()[m][0]
    for i,elem in enumerate(elem_num_list) :
        if read["LabelType"][0] == "1":
            elem_label += [str(i+1)]
        elif read["LabelType"][0] == "2":
            elem_label += [elem ]
        elif read["LabelType"][0] == "3":
            elem_label += [str(elem_num_list[0:i].count(elem)+1) + elem]
        elif read["LabelType"][0] == "4":
            elem_label += [str(i+1)+ elem ]
        else :
            elem_label += [str(i+1)+ elem ]


    for k in range(0,int(cube_list[2][1])*-1):
        for m in range(0,117):
            if lib.library.items()[m][1][0] == int(float(all_atom[k][1])):
                out.write(lib.library.items()[m][0]+' ')
            else: continue
        for l in range (3,7):
            if l==6:
                out.write(elem_label[k]+'\n')
            else:
                out.write(all_atom[k][l]+' ')


    #=======================================
    #file close
    out.close()
    f.close()








    #  file open
    f = open(filenametext,'r')
    out = open(filenametext[:-5] + '/convert_wave_function.vtk.txt','w')

    #======counter and skip data============
    check = 0
    check2 = 1
    for n in range(0,7+int(cube_list[2][1])*-1):
        f.readline()
    #=======================================

    #========Loop line & Mod line===========
    if int(cube_list[5][1])%6 == 0 :
        L = int(cube_list[5][1]) / 6

    elif int(cube_list[5][1])%6 != 0:
        L = int(cube_list[5][1]) / 6 + 1

    for xy in range(0, int(cube_list[3][1]) * int(cube_list[4][1])):
        for line_num_in_xy in range(0, L):
            line = f.readline()
            line = line.strip()
            if line == "":
                line = f.readline()
                line = line.strip()
            line = " ".join(map(lambda s: str(float(s)), re.split(" *", line)))  # Convert numerical format.
            out.write(line + " ")
        out.write("\n")
    out.close()
    f.close()



    #======Open file & wave function list in=======
    f = open(filenametext[:-5] + '/convert_wave_function.vtk.txt','r')
    out = open(filenametext[:-5] + '/VTK_out.vtk','w')
    total_line=[]
    mirror = []
    for j in range (0,int(cube_list[3][1])):
        all_line=[]
        for i in range(0,int(cube_list[4][1])):
            line = f.readline()
            line = line.rstrip()
            line = re.sub("\n","",line)
            line = re.split(" ",line)
            all_line += [line]
        total_line += [all_line]
    #======================================


    sum_wave = 0
    for i in range(0,int(cube_list[3][1])):
        for j in range(0,int(cube_list[4][1])):
            for k in range(0,int(cube_list[5][1])):
                total=total_line[i][j][k]
                check_wave=check_line[i][j][k]
                total=float(total)
                check_wave=float(check_wave)
                sum_wave += total*check_wave
    if sum_wave >= 0:
        print "plus",sum_wave
    elif sum_wave < 0:
        print "minus",sum_wave
        for i in range(0,int(cube_list[3][1])):
            for j in range(0,int(cube_list[4][1])):
                for k in range(0,int(cube_list[5][1])):
                    dammy=total_line[i][j][k]
                    dammy=float(dammy)*-1
                    total_line[i][j][k]=str(dammy)
    else :
        print "NG"

    #======Out file & wave function convert to VTKformat=======
    out.write('# vtk DataFile Version 2.0'+'\n')
    out.write('Probability density for the 3d electron position in a hydrogen atom'+'\n')
    out.write('ASCII'+'\n')
    out.write('DATASET STRUCTURED_POINTS'+'\n')
    out.write('DIMENSIONS'+' '+cube_list[3][1]+' '+cube_list[4][1]+' '+cube_list[5][1]+'\n')
    out.write('ORIGIN'+' '+cube_list[2][2]+' '+cube_list[2][3]+' '+cube_list[2][4]+'\n')
    out.write('SPACING'+' '+cube_list[3][2]+' '+cube_list[4][3]+' '+cube_list[5][4]+'\n')
    out.write('POINT_DATA'+' '+str(int(cube_list[3][1])*int(cube_list[4][1])*int(cube_list[5][1]))+' '+'\n')
    out.write('SCALARS probability_density float'+'\n')
    out.write('LOOKUP_TABLE default'+'\n')
    for k in range (0,int(cube_list[5][1])):
        for j in range (0,int(cube_list[4][1])):
            for i in range (0,int(cube_list[3][1])):
                if i==(int(cube_list[3][1])-1):
                    out.write(total_line[i][j][k]+'\n')
                else:
                    out.write(total_line[i][j][k]+' ')
    out.close()
    f.close()

    print "convert end"
    return total_line

if __name__ == "__main__":
    print "input_dir filename mode"
    argv = sys.argv
    input_dir = argv[1]
    files = os.listdir(input_dir)
    for f in files:
        if f.find(".cub") >= 0:
            cube_vtk(input_dir,f,False)

