import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.pylab as pl
import parameters as p
import mathEquations as e
import numpy as np
from scipy.integrate import solve_ivp
import weightHandler as wh

mpl.rcParams['savefig.dpi'] = 1000
mpl.rcParams['figure.figsize'] = (19, 10)


def plotSigmoidFunction():
  uValues = np.linspace(-1, 1.5, 300)
  fig = plt.figure()
  plt.plot(uValues, e.getSigmoid(uValues))
  return fig


def plotTuningCurve():
  # To replicate Figure 2.
  # K = 8.08
  # A = 2.53 Hz
  # Be^k = 34.8 Hz
  theta_0 = 0
  fig = plt.figure("Paper - Figure 2")
  ax = fig.add_subplot()
  dataY = e.getTuningCurve(theta_0=theta_0)
  dataX = theta_0 - p.thetaSeries
  plt.plot(dataX, dataY)
  plt.suptitle("Activity of a HD cell in the anterior thalamus")
  plt.title(r"K=%d, A=%d, B=%d" % (p.K, p.A, p.B))
  plt.xlabel(r"Difference between head direction versus preferred direction , $\theta - \theta_0$")
  plt.ylabel("Firing rate, f (Hz)")
  plt.tight_layout()

  # Add padding to x and y axis.
  plt.ylim(0, dataY.max()+(dataY.max()*0.1))
  plt.xlim(p.thetaSeries.min(), p.thetaSeries.max())

  # Suffix x-axis labels with degree sign.
  ax.xaxis.set_major_formatter('{x:1.0f}°')

  # Ensure axes ticks match paper.
  ax.set_xticks([-180, -90, 0, 90, 180])

  plt.savefig(p.outputDirectory+'/figures/tuning-curve.svg', dpi=350)
  return fig


def plotSampledNeuroneWeightDistributions(neuronalPopulation):
  fig, ax = plt.subplots(nrows=3, ncols=4, squeeze=True)
  fig.set_tight_layout(True)
  neuroneIdsToSample = np.linspace(
      0, len(neuronalPopulation.neurones)-1, num=12)
  
  rowId = 0
  columnId = 0
  for neurone in neuronalPopulation.neurones[neuroneIdsToSample.astype(int)]:
    ax[rowId, columnId].plot(p.thetaSeries, neurone.getWeights())
    maxYIndex = np.argmax(neurone.getWeights())
    ax[rowId, columnId].axvline(p.thetaSeries[maxYIndex], color='red')
    ax[rowId, columnId].set_title(
        r'$\theta_0=%d°$' "\n" r'Strongest connection to: %d°' % (neurone.theta_0, p.thetaSeries[maxYIndex]))
    ax[rowId, columnId].set_xlabel(
        r'Neurone(s) with preferred head direction, $\theta$')
    ax[rowId, columnId].set_ylabel('Weight to neurone')
    if(columnId == 3):
      rowId = rowId + 1
      columnId = 0
    else:
      columnId += 1

  #plt.xlabel("common X")
  #plt.ylabel("common Y")
  plt.suptitle(
      'Weights of 12 neurones, each with unique preferred head directions')
  plt.tight_layout()
  plt.savefig(p.outputDirectory + '/figures/12-weight-plots.svg', dpi=700)
  return fig

def plotWeightDistribution(weights, hasNoise=False):
  # NOTE: This produces figures that are sensitive to theta_0 (i.e., the preferred head direction).
  # TODO: This function could do with some experimentation, where neuronal population weights are not rolled, but rather set according to varying theta_0.
  fig = plt.figure()
  ax = fig.add_subplot()
  im = ax.imshow(weights)
  ticks = [{
      'location': int(i),
      'label': str(np.ceil(p.thetaSeries[int(i)]))+'°'
  } for i in np.linspace(0, len(p.thetaSeries)-1, 9)]
  #ax.invert_yaxis()

  ax.set_xticks([tick['location'] for tick in ticks],
                [tick['label'] for tick in ticks])
  ax.set_yticks([tick['location'] for tick in ticks],
                [tick['label'] for tick in ticks])
  plt.xlabel(r"HD cell's preferred direction, $\theta$ (degrees)")
  plt.ylabel(r"HD cell's preferred direction, $\theta$ (degrees)")

  fig.colorbar(im)
  if(hasNoise):
    plt.title(r"N=%d, K=%d, A=%d, B=%d, " "$\lambda$" "=%f" %
              (p.numberOfUnits, p.K, p.A, p.B, p.penaltyForMagnitude_0))
    plt.suptitle("Strength of connections (weights) between neurones (noisy)")
    plt.savefig(p.outputDirectory+'/figures/weights-heatmap-noisy.svg', dpi=350)
  else:
    plt.title(r"N=%d, K=%d, A=%d, B=%d" % (p.numberOfUnits, p.K, p.A, p.B))
    plt.suptitle("Strength of connections (weights) between neurones (noiseless)")
    plt.savefig(p.outputDirectory + '/figures/weights-heatmap-noiseless.svg', dpi=350)
  
  return fig


def solveDuDt(neuronalPopulation):
    # Solve for time
  fig = plt.figure()
  ax = fig.gca()

  # Labelling X-Axis
  ax.set_xlabel('Time')

  # Labelling Y-Axis
  ax.set_ylabel('Neurones firing rate (Hz)')
  # Labelling Z-Axis
  #ax.set_zlabel('Time')
  plt.suptitle('Firing activity of neuronal population over time')
  t0 = p.timeSeries[0].astype('float64')
  tf = p.timeSeries[-1].astype('float64')

  if(p.initialCondition == 'noise'):
    firingActivityOfAllNeurones = p.randomGenerator.normal(
        loc=10, scale=3, size=p.numberOfUnits)

  elif(p.initialCondition == 'tuningCurve'):
    firingActivityOfAllNeurones = e.getTuningCurve(theta_0=90)

  elif(p.initialCondition == 'steadyState'):
    firingActivityOfAllNeurones = np.ones(p.numberOfUnits) * e.getF(-0.4635)

  elif(p.initialCondition == 'slightlyAwayFromSteadyState'):
    firingActivityOfAllNeurones = np.ones(p.numberOfUnits) * e.getF(-0.6)

  firingActivityOfAllNeurones = np.abs(firingActivityOfAllNeurones)

  uActivityOfAllNeurones = e.getU(firingActivityOfAllNeurones)
  sol = solve_ivp(e.getDuDt, (t0, tf), uActivityOfAllNeurones, args=[
                  neuronalPopulation.getAllWeights()], t_eval=p.timeSeries)

  usAtTimeT = sol.y.T
  fsAtTimeT = e.getF(usAtTimeT)
  plt.plot(p.timeSeries, fsAtTimeT)

  fig = plt.figure()
  ax = fig.gca(projection="3d")
  # Labelling X-Axis
  ax.set_xlabel('Firing rate $f$ (Hz)')

  # Labelling Y-Axis
  ax.set_zlabel('Time (ms)')
  ax.yaxis.set_major_formatter('{x:1.0f}°')

  # Labelling Z-Axis
  ax.set_ylabel('Population of HD Cells')
  #plt.xlim(0, 40)

  for timeIndex, fAtTimeT in enumerate(fsAtTimeT[0:len(fsAtTimeT):10]):
    x, y, z = p.thetaSeries, fAtTimeT, p.timeSeries[timeIndex*10]
    plt.plot(y, x, z)
  #yValues = p.thetaSeries[np.argmax(fAtTimeT, axis=1)]
  ax.invert_xaxis()
  ax.invert_zaxis()
  plt.savefig(p.outputDirectory +
              '/figures/dudt-over-time.svg', dpi=350)
  return fig