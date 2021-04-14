import numpy as np

def calculate_fractal_dim(dla_lattice):
    leni, lenj = dla_lattice.shape

    LMIDi = int(leni / 2)
    LMIDj = int(lenj / 2)
    LMID = min(LMIDi, LMIDj)  # let's ensure quadratic boxes which fit on DLAlattice
    size_vs_num = np.zeros((LMID, 2))
    # loop over s which gives b=2*s+1
    for size in range(LMID):
        num = 0
        # loop over lattice
        for x in range(LMIDi - size, LMIDi + size + 1):
            for y in range(LMIDj - size, LMIDj + size + 1):
                num += dla_lattice[x, y]
        if num > 0:
            size_vs_num[size] = np.array([np.log(2 * size + 1), np.log(num)])
    return size_vs_num


if __name__ == "__main__":
    # read big DLA cluster array from data-file and assign array to it
    dla_lattice = np.loadtxt('on_lattice/OnLattice3001.dat').astype('int')
    # to know the size of the array leni x lenj use .shape
    size_vs_num = calculate_fractal_dim(dla_lattice)
    p = np.polyfit(size_vs_num[:, 0], size_vs_num[:, 1], 1)
    print(p)
