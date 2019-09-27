#
# IP: HILICS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from solid import square, text, translate, \
    linear_extrude, polygon, cube, resize,\
    rotate, mirror, scad_render_to_file, hull
import subprocess

from pathlib import Path

# Configuration
ids = range(0,10) # start number, stop number + 1

name_str = 'HILICS $ID' #use $ID to place the 3 digit ID

text_font = 'Ruler Stencil Heavy:style=Regular'
text_size = 9  
text_spacing = 1.0
text_height = 16
text_width = 105

# text_font = 'Coulson'
# text_size = 9
# text_spacing = 1.0
# text_height = 16
# text_width = 100

xlen = 117.6  # mm
ylen = 25.3  # mm
zlen = 3.2  # mm

def nameplate(id):
    #create the plate
    bottom = cube([xlen, ylen, 0.01], center=True)
    top = cube([xlen-zlen-zlen, ylen-zlen, 0.1], center=True)
    top = translate([0, zlen/2, zlen-0.1])(top)

    plate = hull()([bottom, top])

    # define the text
    id_str = name_str.replace('$ID',f'{id:03d}')
    msg = text(id_str,
               size=text_size,
               font=text_font,
               spacing = text_spacing,
               halign='center',
               valign='center')
    msg = linear_extrude(zlen+1)(msg)
    msg = resize([text_width,text_height,0])(msg)
    msg = translate([0, zlen/2, -0.5])(msg)
    
    #add text to the plate
    plate = plate - msg

    #generate output files
    scad_file = Path.cwd() / 'scad_files' / f'plate_{id:03d}.scad'
    if scad_file.parent.exists() is False:
        scad_file.parent.mkdir()
    scad_render_to_file(plate, str(scad_file))

    stl_file = Path.cwd() / 'stl_files' / f'plate_{id:03d}.stl'
    if stl_file.parent.exists() is False:
        stl_file.parent.mkdir()
    subprocess.run(['openscad', '-o', str(stl_file), str(scad_file)])

if __name__ == '__main__':
    for id in ids:
        nameplate(id)
        print(f'Finished processing name plate {id:03d}')