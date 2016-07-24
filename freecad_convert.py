#!/usr/bin/freecadcmd
#!/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd
'''
Original:
http://jordan.husney.com/archives/2013/07/converting_cad_files_to_stl_us.php

Repaired:
J. R.I.B.-Wein, Open Source Ecology Germany
'''

#$ $(PYTHON) step_stl.py input.step output.stl  #<-- yet another problem as the PYTHON was missing! now repaired, $(PYTHON) usually is simply 'python' or '/usr/bin/python' if not on the SYSTEM PATH.

#You can even use it in a more general way, freecad is very powerful:
#$ python freecad_convert.py path/to/infile.<source_ending> path/to/outfile.<target_ending>

'''
#Original instructions stated to overwrite this Variable:
$ export DYLD_FALLBACK_LIBRARY_PATH=\
/Applications/FreeCAD.app/Contents/Frameworks/lib:\
$DYLD_FALLBACK_LIBRARY_PATH

But it failed, because the script did not use the Variable. Now it's repaired. See below:
'''



#Rewritten by OSE Germany, J.R.I.B.-Wein:
FREECAD_LIB_PATH = '/usr/lib/freecad/lib'# path to your FreeCAD.so or FreeCAD.dll file


# Can be overwritten or added to from the command line via:
#($ stands for 'bash', eff. command line, and has to be omitted!)

# ADD ANOTHER PATH:
# $ export FREECAD_LIB_PATH = '<path_to_lib_FreeCAD.so_or_.dll>':$FREECAD_LIB_PATH

# OVERWRITE:
# $ export FREECAD_LIB_PATH = '<path_to_lib_FreeCAD.so_or_.dll>'


# CAN ALSO BE GIVEN WHILE EXECUTING THIS SCRIPT:
# $ python <path/to/script_for_bash_conversion>.py





import sys
sys.path.append(FREECAD_LIB_PATH)#<-- added, otherwise FreeCAD is not found
import os
import FreeCAD
import Part
import Mesh

#import Blender                 #<-- kept as a reminder for how well those two open source gems interact


# The original author wrote this script. The syntax was figured out by recording and evaluating some macros in FreeCAD. Thanks open source movement.


in_f, out_f = sys.argv[1], sys.argv[2]  #<-- repaired, out of bounds
in_fn,in_ext = os.path.splitext(in_f)
out_fn,out_ext = os.path.splitext(out_f)
print(in_ext, " -> ", out_ext)

mesh_formats = ['.dae', '.stl', '.obj']

def main():
    shape = Part.Shape()
    #shape_formats = ['.brp', '.igs', '.stp']
    if in_ext in mesh_formats:
        print("Opening mesh file: ", in_f)
        Mesh.open(in_f)
        o = FreeCAD.getDocument("Unnamed").findObjects()[0]
        #print("dir: ", dir(o))
        if out_ext in mesh_formats:
            print("Exporting to mesh file: ", out_f)
            Mesh.export([o], out_f)
        else:
            # TODO This is not optimizing the resulting amount of faces!
            # see http://www.freecadweb.org/wiki/index.php?title=Mesh_to_Part
            shape.makeShapeFromMesh(o.Mesh.Topology, 0.05)  # tolerance for sewing
            exportParametric(shape, out_f, out_ext)
    elif out_ext in mesh_formats:
        print("Opening parametric file: ", in_f)
        Part.open(in_f)
        o = FreeCAD.getDocument("Unnamed").findObjects()[0]
        print("Exporting to mesh file: ", out_f)
        Mesh.export([o], out_f)
    else:
        # Parametric -> Parametric
        print("Opening parametric file: ", in_f)
        shape.read(in_f)
        exportParametric(shape, out_f, out_ext)



def exportParametric(shape, out_f, out_ext):
    print("Exporting to parametric file: ", out_f)
    if out_ext == '.brp':
        shape.exportBrep(out_f)
    elif out_ext == '.igs':
        shape.exportIges(out_f)
    elif out_ext == '.stl':
        shape.exportStl(out_f)
    elif out_ext == '.stp':
        shape.exportStep(out_f)
    else:
        print("Export to '%s' not supported." % (out_ext))


main()

'''
def import_fcstd(filename):
   try:
       import FreeCAD
   except ValueError:
       Blender.Draw.PupMenu('Error%t|FreeCAD library not found. Please check the FREECADPATH variable in the import script is correct')
   else:
       scene = Blender.Scene.GetCurrent()
       import Part
       doc = FreeCAD.open(filename)
       objects = doc.Objects
       for ob in objects:
           if ob.Type[:4] == 'Part':
               shape = ob.Shape
               if shape.Faces:
                   mesh = Blender.Mesh.New()
                   rawdata = shape.tessellate(1)
                   for v in rawdata[0]:
                       mesh.verts.append((v.x,v.y,v.z))
                   for f in rawdata[1]:
                       mesh.faces.append.append(f)
                   scene.objects.new(mesh,ob.Name)
       Blender.Redraw()
'''

def main():
   pass
#   Blender.Window.FileSelector(import_fcstd, 'IMPORT FCSTD',
#                       Blender.sys.makename(ext='.fcstd'))

# This lets you import the script without running it
if __name__=='__main__':
   main()


#It's used like this:

#$(PYTHON) step_stl.py input.step output.stl  #<-- yet another problem as the PYTHON was missing! now repaired, $(PYTHON) usually is simply 'python' or '/usr/bin/python' if not on the SYSTEM PATH.

