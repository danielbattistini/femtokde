'''
Script to create a tree dataset from binned dataset
'''
from functools import reduce
from os import system
import numpy as np
import argparse
from sys import exit

from utils.io import GetObjectFromFile
from utils.handle import GetFemtoDreamPairId

from ROOT import TFile, TTree, gRandom, TH1D

def CreateFakeDataset(reducedDataset=False, **kwargs):
    """
    Create a fake tree dataset using a histogram as input.

    Parameters
    ----------
    inFilePath : str
        path of input datafile
    inHistPath : str
        path of histogram to sample inside the input file
    oFilePath : str
        path of output file
    oTreeName : str
        name of the output tree
    reducedDataset : bool
        reduce by a factor 1000 the size of datasample
    Returns
    -------
    int
        Description of return value

    """

    inFile = TFile(kwargs['inFilePath'])

    pairCombs = GetFemtoDreamPairId('sc')

    regions = {'sgn': '', 'sbl': 'SBLeft_', 'sbr': 'SBRight_'}
    
    for regKey, regVal in regions.items():
        directory = f'HM_CharmFemto_{regVal}Dpion_Results0'
        
        # load histograms
        hSE = {}
        hME = {}
        for pairKey, pairComb in pairCombs.items():
            print(f'{directory}/{directory}/{pairComb}/SEDist_{pairComb}')
            hSE[pairComb] = GetObjectFromFile(inFile, f'{directory}/{directory}/{pairComb}/SEDist_{pairComb}')
            hME[pairComb] = GetObjectFromFile(inFile, f'{directory}/{directory}/{pairComb}/MEDist_{pairComb}')
    inFile.Close()

    oFile = TFile(kwargs['oFilePath'], 'recreate')
    for regKey, regVal in regions.items():
        directory = f'HM_CharmFemto_{regVal}Dpion_Results0'

        # Generate se and me distributions
        kStar = np.empty((1), dtype='d')
        for pairKey, pairComb in pairCombs.items():
            # sample SE
            nSamplSE = gRandom.Poisson(hSE[pairComb].GetEntries())
            if reducedDataset:
                nSamplSE=int(nSamplSE/1000)
            print(nSamplSE, hSE[pairComb].GetEntries())
            treeSE = TTree(f'treeDpi_SE_{regKey}_{pairComb}', f'treeDpi SE {regKey} {pairComb}')
            treeSE.Branch('kStar', kStar, 'kStar/D')

            for iMeas in range(nSamplSE):
                kStar[0] = hSE[pairComb].GetRandom()
                treeSE.Fill()
            treeSE.Write()

            # sample ME
            nSamplME = gRandom.Poisson(hME[pairComb].GetEntries())
            if reducedDataset:
                nSamplME=int(nSamplME/1000)
            print(nSamplME, hME[pairComb].GetEntries())
            treeME = TTree(f'treeDpi_ME_{regKey}_{pairComb}', f'treeDpi ME {regKey} {pairComb}')
            treeME.Branch('kStar', kStar, 'kStar/D')

            for iMeas in range(nSamplME):
                kStar[0] = hME[pairComb].GetRandom()
                treeME.Fill()

            # Write to file
            treeME.Write()
    oFile.Close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('inFilePath', metavar='text', help='AnalysisResults.root file')
    parser.add_argument('oFilePath', metavar='text', help='AnalysisResults.root file')
    parser.add_argument('-r', action='store_true', default=False, help='use reduced size of dataset')

    args = parser.parse_args()

    CreateFakeDataset(inFilePath=args.inFilePath, oFilePath=args.oFilePath, reducedDataset=args.r)
