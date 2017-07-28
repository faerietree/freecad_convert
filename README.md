# FreeCAD convert python script


## Example usage
```
for fi in `find ~ -iname '*.stp'`; do if ! [ -f "${fi%.*}.stl" ]; then echo "Converting to: "${fi%.*}".stl"; python2 ~/freecad_convert/freecad_convert.py $fi ${fi%.*}.stl; fi; done
```
