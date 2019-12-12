# config ######################################################################
OUTDIR = 'out/ycbcr'
INDIR = 'out/img/outgame/unitdetail'

###############################################################################
import os
from PIL import Image



extracted = {}
def ycbcr(base_file_name):
    global inprefix
    if base_file_name in extracted:
        return
    extracted[base_file_name] = 1

    global DST
    if os.path.exists(base_file_name+"_Y.png"):
        tmp = Image.open(base_file_name + "_Y.png")
    elif os.path.exists(base_file_name+"_y.png"):
        tmp = Image.open(base_file_name + "_y.png")
    else:
        return
    size = tmp.size
    (z,z,z,y) = tmp.convert('RGBA').split()
    if os.path.exists(base_file_name+"_Cb.png"):
        u = Image.open(base_file_name + "_Cb.png").convert('L').resize(size, Image.LANCZOS)
    elif os.path.exists(base_file_name+"_cb.png"):
        u = Image.open(base_file_name + "_cb.png").convert('L').resize(size, Image.LANCZOS)
    else:
        return
    if os.path.exists(base_file_name+"_Cr.png"):
        v = Image.open(base_file_name + "_Cr.png").convert('L').resize(size, Image.LANCZOS)
    elif os.path.exists(base_file_name+"_cr.png"):
        v = Image.open(base_file_name + "_cr.png").convert('L').resize(size, Image.LANCZOS)
    else:
        return
    alpha_file_name = base_file_name + "_alpha.png"

    basedir = os.path.dirname(base_file_name)
    if os.path.splitext(basedir)[1] == '.mat':
        base_file_name = basedir[:-4]
    print(base_file_name)

    merged = Image.merge("YCbCr", (y,u,v)).convert('RGB')

    if os.path.exists(alpha_file_name):
        #(r,g,b,z) = Image.open(fname).convert('RGBA').split()
        (r,g,b) = merged.split()
        s = Image.open(alpha_file_name).resize(size, Image.LANCZOS).split()
        if len(s) == 4:
            a = s[3]
        elif len(s) == 3:
            a = s[0]
        else:
            raise
        merged = Image.merge("RGBA", (r,g,b,a))

        if DST:
            fname = DST+'/'+base_file_name[inprefix:]+"_rgba.png"
        else:
            fname = base_file_name+"_rgba.png"
    else:
        if DST:
            fname = DST+'/'+base_file_name[inprefix:]+"_rgb.png"
        else:
            fname = base_file_name+"_rgb.png"
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    merged.save(fname)


def main():
    global OUTDIR, INDIR
    global SRC, DST
    global inprefix
    if 'OUTDIR' not in globals():
        OUTDIR = None
    if 'INDIR' not in globals():
        INDIR = None
    ROOT = os.path.dirname(os.path.realpath(__file__))
    #SRC = os.path.join(ROOT, INDIR)
    SRC = INDIR
    DST = os.path.join(ROOT, OUTDIR)
    inprefix = len(SRC)+1

    for root, dirs, files in os.walk(SRC, topdown=False):
        #print(root)
        if '.git' in root:
            continue
        for f in files:
            extension = os.path.splitext(f)[1]
            #src = os.path.realpath(os.path.join(root, f))
            src = os.path.join(root, f)
            if extension == '.png':
                e = src.rfind('_')
                bfn = src[:e]
                ycbcr(bfn)

if __name__ == "__main__":
    main()
    #base_file_name = "unitdetail/amulet/400002_01/400002_01"
    #ycbcr(base_file_name)

