import sys
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np
import uproot
import seaborn as sns

# FLUKA_PYG4OMETRY_RESULTS = "data/cylinder_fluka/fluka_cylinder_data.csv"
FLUKA_PYG4OMETRY_RESULTS = "data/cylinder_fluka/pyg4ometry_cylinder_data.csv"

def main():
    plotPyg4ometryFluka()
    plotPyg4ometryUpRoot()
    plt.legend()
    plt.show()

def plotPyg4ometryFluka():
    x0, eta = getFlukaPyg4ometryResults()
    # flukaColor = "blue"
    # sns.regplot(x=eta, y=x0, x_bins=50, color=flukaColor, fit_reg=False)
    plt.plot(eta, x0, label="Geant4 converted to FLUKA")

def plotPyg4ometryUpRoot():
    with uproot.open("data/geant4_root_files/geant4_material_tracks.root") as file:
        x0 = np.array(file["material-tracks/t_X0"].array())
        eta = np.array(file["material-tracks/v_eta"].array())
    plt.rcParams["figure.autolayout"] = True
    # sns.regplot(x=eta, y=x0, x_bins=20, marker='o', fit_reg=False)
    sns.regplot(x=eta, y=x0, x_bins=50, color="orange", fit_reg=False, label="Geant4")
    # plt.plot(eta, x0)

def getFlukaPyg4ometryResults():
    df = pd.read_csv(FLUKA_PYG4OMETRY_RESULTS)
    return (df.X0, df.Eta)


if __name__ == '__main__':
    sys.exit(main())