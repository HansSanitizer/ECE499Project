import numpy as np

def rhoTheta(indices, centerSmall):
    x = indices[1][0] - centerSmall[0]
    y = indices[0][0] + centerSmall[1]
    contoursXY = np.array([x, y])
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    if theta < 0:
        theta = theta + 2*np.pi
    print(len(indices[:]))
    contoursThetaRho = np.array([theta, rho])
    print("Printing Theta Rho:")
    print(contoursThetaRho)
    for i in range(1, len(indices[0])):
        x = indices[1][i] - centerSmall[0]
        y = centerSmall[1] - indices[0][i]
        rho = np.sqrt(x**2 + y**2)
        theta = (np.arctan2(y, x))
        if theta < 0:
            theta = theta + 2*np.pi
        b = np.array([theta, rho])
        # keep adding new rows
        contoursThetaRho = np.column_stack((contoursThetaRho.T, b)).T
        b = np.array([x, y])
        contoursXY = np.column_stack((contoursXY.T, b)).T
    # sort our theta data, don't ask me to explain what this is doing
    print("sorting")
    contoursThetaRhoSorted = np.lexsort((contoursThetaRho[:, 1], contoursThetaRho[:, 0]))
    contoursThetaRhoSorted = contoursThetaRho[contoursThetaRhoSorted]
    return contoursXY, contoursThetaRhoSorted

