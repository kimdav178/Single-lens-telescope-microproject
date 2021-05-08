from PIL import Image
import numpy as np

img1 = Image.open("2.jpg").convert('RGB')
data1 = np.asarray(img1)
data = np.array(Image.new('RGB', (data1.shape[0], data1.shape[1])))
#data.setflags(write=1)
data2 = np.zeros((144, 176, 3), dtype=np.float)

k1 = round(255/(1+data2.max() - data2.min()))
updated_data1 = (data2-data1.min()) * k1

#print(data1[:, 176])
#res_img1 = Image.fromarray(updated_data1)
#res_img1.save("2_edited.jpg")
data2[0, 0] = (258, 100, 100)
data2[0, 0, 0] = round(data2[0, 0, 0])
data2[0, 0] += [1, 2, 3]
data[0, 0] = data2[0, 0]
#data.dtype = np.uint8
img = Image.fromarray(data)
print(data[0, 0])
print(data2[0, 0])
for i in range(2):
    print(i)
