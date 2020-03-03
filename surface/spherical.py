import numpy as np

from mathutils import Vector

def add_spherical_surface(rad,lrad,N1,N2,nsurf=1,xadd=0,nVerts=0,hole=False,hrad=0):
    """
    nsurf=1 for first surface,
    nsurf=-1 for second surface
    
    xadd has to be set for second surface (only)
    """

    verts = []
    faces = []
    splitverts = []
    
    surfadd=0
    if nsurf == -1:
        surfadd = N2*N1

    sig = 1
    if rad < 0:
        sig = -1
    nhole = not hole
    rad = np.abs(rad)
    ang = np.arcsin(lrad/rad)

    if not hole:
        verts.append(Vector((-xadd,0,0)))
        splitverts.append(0)
        a = ang/N1
        r = rad*np.sin(a)
        hang = 0
    else:
        hang = np.arcsin(hrad/rad)
        r = hrad

    x = rad-np.sqrt(rad**2-r**2)
    for j in range(N2)[::nsurf]:
        b = 2*np.pi*j/N2
        verts.append(Vector((-1.*x*sig*nsurf-xadd,r*np.sin(b),r*np.cos(b))))
        splitverts.append(0)
        if not hole:
            fi1 = nVerts+surfadd
            fi2 = fi1+nsurf*((j+1)%N2+1)
            fi3 = fi1+nsurf*(j+1)
            faces.append([fi1,fi2,fi3])
    for i in range(1,N1):
        a = hang + (ang-hang)/(N1-1)*(i)
        r = rad*np.sin(a)
        x = rad-np.sqrt(rad**2-r**2)
        for j in range(N2)[::nsurf]:
            b = 2*np.pi*j/N2
            verts.append(Vector((-1.*x*sig*nsurf-xadd,r*np.sin(b),r*np.cos(b))))
            if i == N1-1:
                splitverts.append(1)
            else:
               splitverts.append(0)
            fi1 = nVerts+surfadd+nsurf*(j+nhole+i*N2)
            fi2 = nVerts+surfadd+nsurf*((j+1)%N2+nhole+i*N2)
            fi3 = fi2-nsurf*N2
            fi4 = fi1-nsurf*N2
            faces.append([fi4,fi3,fi2,fi1])
            
    return verts, faces, splitverts