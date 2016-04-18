#===import module===#
import os
import re , sys
import formatconvert as convert
import visualize_isosurface as view
import vtk
import argparse
import multiprocessing as mp
#from multiprocessing import Pool, cpu_count, current_process
try:
    from mpi4py import MPI
    MPI_flag = True
except:
    MPI_flag = False
    
def test(args):
    filenametext,input_dir,boundary_mode,output_dir,Batch_mode = args
    convert.cube_vtk(input_dir,filenametext,boundary_mode)
    view.vtk(output_dir,filenametext,Batch_mode,input_dir)
    return 0

if __name__ == "__main__":
    pwd = os.getcwd()
    files = os.listdir(pwd)

    parser = argparse.ArgumentParser(prog="VisBAR_wave_batch")
    parser.add_argument("input_dir", metavar="[Directry]", type=str , help='Set input directry')
    parser.add_argument("-o", type=str, metavar="[Directry]", help='Select output directry')
    parser.add_argument('-s', default=False, action="store_true", help='Sign correction mode')
    parser.add_argument('-b', default=False, action="store_true", help='Batch mode')
    parser.add_argument('-p', default=False, action="store_true", help='Periodic mode')
    parser.add_argument('-parallel', default=False, action="store_true", help='Parallel mode')
    args = parser.parse_args()
    vars_args = vars(args)
    prog_dir_path = os.path.dirname(sys.argv[0])
    if prog_dir_path == "":
        prog_dir_path = "./"

    input_dir = vars_args["input_dir"]
    if vars_args["o"]:
        output_dir = vars_args["o"]
    else:
        output_dir = vars_args["input_dir"]
    Batch_mode = vars_args["b"]
    sign_correction_mode = vars_args["s"]
    boundary_mode = vars_args["p"]
    Parallel_mode = vars_args["parallel"]
    try:
        Parallel_core = int(os.environ.get("OMP_NUM_THREADS"))
    except:
        Parallel_core = mp.cpu_count()

    if Parallel_mode == True:
        if sign_correction_mode == True:
            print "[error] -parallel and -s cannot use at the same time."
            sys.exit()
        if Batch_mode == False:
            print "[error] -parallel runs only using 'batch mode(-b)'."
            sys.exit()

    print "MPI_flag",MPI_flag
    if MPI_flag == True:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        if rank == 0 :
            print sys.argv[0]
            print os.path.dirname(sys.argv[0])
            files2 = os.listdir(vars_args["input_dir"])
            files = []
            for a in files2:
                if a.find(".cub") >= 0:
                    files += [a]
            sortKey = lambda f: f if not f.startswith('.') else f[1:]
            files.sort(key=sortKey)
            del files2
    else :
        print sys.argv[0]
        print os.path.dirname(sys.argv[0])
        files2 = os.listdir(vars_args["input_dir"])
        files = []
        for a in files2:
            if a.find(".cub") >= 0:
                files += [a]
        sortKey = lambda f: f if not f.startswith('.') else f[1:]
        files.sort(key=sortKey)
        del files2    

    if MPI_flag == True:
        args_list = []
        if rank == 0:
            print "node =" ,size
            print "core =" ,Parallel_core
            for i in xrange(size):
                mpi = []
                for j in xrange(i,len(files),size):
                    mpi += [ (files[j],input_dir,boundary_mode,output_dir,Batch_mode) ]
                args_list += [mpi]
        else :
            files_mpi = []
        comm.Barrier()
        args_list = comm.scatter(args_list, root=0)
    else :
        print "core =" ,Parallel_core
        args_list = []
        for i in xrange(len(files)):
            args_list += [(files[i],input_dir,boundary_mode,output_dir,Batch_mode)]

    if Parallel_mode :
        print "parallel mode"
        p = mp.Pool(Parallel_core)
        p.map(test, args_list )
    else:
        print "single mode"
        if sign_correction_mode == False:
            for f in args_list:
                test(f)
        else :
            print "sign_correction_mode on"
            filenametext,input_dir,boundary_mode,output_dir,Batch_mode = args_list[0]
            check_line = convert.cube_vtk(input_dir,filenametext,boundary_mode)
            view.vtk(output_dir,filenametext,Batch_mode,input_dir) 
            for args in args_list[1:]:
                filenametext,input_dir,boundary_mode,output_dir,Batch_mode = args
                check_line = convert.cube_vtk2(input_dir,filenametext,check_line,boundary_mode)
                view.vtk(output_dir,filenametext,Batch_mode,input_dir)

    #for filename in files_mpi:
        #test(filename,input_dir,boundary_mode,output_dir,Batch_mode)

