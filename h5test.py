import h5py
import numpy as np

filename = "data/knee.h5"

with h5py.File(filename, "r") as f:
    print("keys %s" % f.keys())
    
    key = list(f.keys())[0]
    dataset = f[key]
    print(dataset.keys())
    data = dataset["data"][0]

    # np.savetxt("write.txt", data[2])

    print(data[0][0], "\n\n", data[0][0].shape)
    print(data[2], "\n\n", data[2].shape)
    
    
