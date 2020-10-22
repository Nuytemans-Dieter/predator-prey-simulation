import matplotlib.pyplot as plt

class Plotter:

    def drawPlot(self, numPreys, numHunters):
        x = list(range(1, numPreys.__len__() + 1))

        plt.plot(x, numPreys, label="Preys")
        plt.plot(x, numHunters, label="Hunters")

        plt.xlabel("Time step")
        plt.ylabel("Number of agents")
        plt.title("Number of preys and hunters through time")
        plt.legend()

        plt.show()
