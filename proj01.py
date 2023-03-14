from PIL import Image
import numpy as np

def get_homography(px0,py0,px1,py1,px2,py2,px3,py3,qx0,qy0,qx1,qy1,qx2,qy2,qx3,qy3):
    #              a   b  c d e f g h i l1l2l3 
    A = np.array([[px0,py0,1,0,0,0,0,0,0,0,0,0],
                 [0,0,0,px0,py0,1,0,0,0,0,0,0],
                 [0,0,0,0,0,0,px0,py0,1,0,0,0],
                 [px1,py1,1,0,0,0,0,0,0,-qx1,0,0],
                 [0,0,0,px1,py1,1,0,0,0,-qy1,0,0],
                 [0,0,0,0,0,0,px1,py1,1,-1,0,0],
                 [px2,py2,1,0,0,0,0,0,0,0,-qx2,0],
                 [0,0,0,px2,py2,1,0,0,0,0,-qy2,0],
                 [0,0,0,0,0,0,px2,py2,1,0,-1,0],
                 [px3,py3,1,0,0,0,0,0,0,0,0,-qx3],
                 [0,0,0,px3,py3,1,0,0,0,0,0,-qy3],
                 [0,0,0,0,0,0,px3,py3,1,0,0,-1]]
                )
    b = np.array([qx0,qy0,1,0,0,0,0,0,0,0,0,0])
    x = np.linalg.solve(A,b)
    x = x[:-3]
    H = np.reshape(x,(3,3))
    return H

# im1 = Image.open("times-square.jpg")
# im1.show()

if __name__ == '__main__':
    im_q = Image.open("times-square.jpg")
    im_q.show()
    qx0 = 301
    qy0 = 231
    qx1 = 451
    qy1 = 283
    qx2 = 448
    qy2 = 394
    qx3 = 292
    qy3 = 375

    im_p = Image.open("manoel_gomes.jpeg")
    pix_values = im_p.load()
    
    px0 = 0
    py0 = 0
    px1 = im_p.width
    py1 = 0
    px2 = im_p.width
    py2 = im_p.height
    px3 = 0
    py3 = im_p.height
    H = get_homography(px0,py0,px1,py1,px2,py2,px3,py3,qx0,qy0,qx1,qy1,qx2,qy2,qx3,qy3)
    H_inv = np.linalg.inv(H)
    print(H_inv)
    for i in range(0,im_q.width,1):
        for j in range(0,im_q.height,1):
            aux = np.dot(H_inv,np.array([i,j,1]))
            x = int(aux[0]/aux[2])
            y = int(aux[1]/aux[2])
            if x >= 0 and x < im_p.width and y >= 0 and y < im_p.height:
                im_q.putpixel((i,j),pix_values[x,y])

    im_q.show()
    
    