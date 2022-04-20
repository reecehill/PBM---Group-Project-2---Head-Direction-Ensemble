import numpy as np
import parameters as p
import mathEquations as e


def generateWeightsForOneNeurone(theta_0):
    # For this function, see: Section 4.3, Synaptic Weight Distribution

    # Get the average firing rates, f, of this neurone, at each head direction, theta.
    firingRatesByTheta = e.getTuningCurve(theta_0)

    # Get the mean net input into this neurone, at each head direction given the respective firing rates.
    # NOTE: Here, we use the principle: inputCurrent(u) -> neuronesOfSharedPreference(sigma) -> outputCurrent(f)
    netInputsByTheta = e.getU(firingRatesByTheta)

    # Transform by Fast Fourier Transformations
    firingRatesByThetaFft = np.fft.fft(firingRatesByTheta)
    netInputsByThetaFft = np.fft.fft(netInputsByTheta)

    # Find squared firing rates (f)
    # TODO: Parrivesh finds abs before squaring, is this necessary?
    firingRatesByThetaFft_squared = firingRatesByThetaFft**2

    # Calculate the amount by which large weights will be penalised.
    penaltyForMagnitude = p.penaltyForMagnitude_0 * \
        firingRatesByThetaFft_squared.max()

    # Compute weight matrix in Fourier ?space.
    # Taken from Section 4.3, Synaptic Weights Distribution, in-text, final equation.
    weightsFft = np.multiply(netInputsByThetaFft, firingRatesByThetaFft) / \
        np.add(penaltyForMagnitude, firingRatesByThetaFft_squared)

    # Convert weights into ?normal domain.
    # TODO: Notice that we get rid of the imaginary part. Is this right? It matches result of Parrivesh, so assume it's a difference in Python.
    weights = np.fft.ifft(weightsFft).real

    return weights


def injectNoise(weightsForAllNeurones):
  meanOfNoise = 0
  stdOfNoise = p.epsilon * np.mean(np.abs(weightsForAllNeurones))
  noise = p.randomGenerator.normal(
      loc=meanOfNoise, scale=stdOfNoise, size=(p.numberOfUnits, p.numberOfUnits))
  weightsForAllNeurones_Noise = weightsForAllNeurones + noise
  return weightsForAllNeurones_Noise
