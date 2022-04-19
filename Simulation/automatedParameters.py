import numpy as np
from datetime import datetime
from pathlib import Path
import parameters as p


def setSeed():
  seed = 1
  randomGenerator = np.random.default_rng(seed)
  return randomGenerator

def getTheta():
  # NOTE: This differs to Parrivesh's code, where they multiply by pi/180 after linspace to get it in radians.
  linearlySpacedTheta = np.linspace(-180, 180, p.numberOfUnits)
  theta = linearlySpacedTheta
  return theta


def getOutputDirectory():
  # Make the folder.
  cwd = str(Path(__file__).parent)
  outputDirectory = str(cwd) + '/output/' + str(datetime.now()).replace(' ', '_').replace(':', '-')
  # Make outputDirectory
  Path(outputDirectory).mkdir(parents=True, exist_ok=True)
  # Make figures folder.
  Path(outputDirectory+'/figures').mkdir(parents=True, exist_ok=True)
  return outputDirectory, cwd


def generate():
  outputDirectory, cwd = getOutputDirectory()
  theta = getTheta()
  randomGenerator = setSeed()
  return outputDirectory, cwd, randomGenerator, theta