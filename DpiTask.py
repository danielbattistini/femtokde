import luigi
from sys import exit
import os

from CreateFakeDataSet import CreateFakeDataset
from ExtractGenCF import ExtractGenCF

analysisBasePath = '/home/daniel/alice/CharmingAnalyses/Dpi_HMpp13TeV_quick/'


class CreateDatasetDirTask(luigi.Task):
    path = luigi.Parameter()

    def run(self):
        os.makedirs(self.path, exist_ok=True)

    def output(self):
        return luigi.LocalTarget(self.path)


class CreateDatasetTask(luigi.Task):
    inFile = luigi.Parameter()
    oFile = luigi.Parameter()
    reducedDataset = luigi.Parameter()

    def run(self):
        CreateFakeDataset(inFilePath=self.inFile, oFilePath=self.oFile, reducedDataset=self.reducedDataset)

    def output(self):
        return luigi.LocalTarget(self.oFile)

    def requires(self):
        return [CreateDatasetDirTask(path=os.path.dirname(self.oFile))]

class ExtractGenCFTask(luigi.Task):
    inFile = luigi.Parameter()
    oFile = luigi.Parameter()

    def run(self):
        ExtractGenCFTask(inFilePath=self.inFile, oFilePath=self.oFile)

    def output(self):
        return luigi.LocalTarget(self.oFile)

    def requires(self):
        return [CreateDatasetDirTask(path=os.path.dirname(self.oFile))]

class DpiTask(luigi.Task):

    def run(self):
        print('Done!')

    def requires(self):
        return [
            CreateDatasetTask(  # data
                inFile='/home/daniel/alice/CharmingAnalyses/DKDpi/oton_mctruth/data/AnalysisResults_all.root',
                oFile='/home/daniel/alice/CharmingAnalyses/Dpi_HMpp13TeV_quick/data/data/AnalysisResults_red.root',
                reducedDataset=True
            ),
            # CreateDatasetTask(  # mcgp
            #     inFile='/home/daniel/alice/CharmingAnalyses/DKDpi/oton_mctruth/mcgp/AnalysisResults_all.root',
            #     oFile='/home/daniel/alice/CharmingAnalyses/Dpi_HMpp13TeV_quick/data/mcgp/AnalysisResults.root',
            #     reducedDataset=False
            # ),
            # ExtractGenCFTask(
            #     inFilePath='/home/daniel/alice/CharmingAnalyses/Dpi_HMpp13TeV_quick/data/data/AnalysisResults_red.root',
            #     oFilePath='/home/daniel/alice/CharmingAnalyses/Dpi_HMpp13TeV_quick/GenCF.root',
            # ),
        ]

    # def output(self):
    #     return luigi.LocalTarget('hello_world.txt')


if __name__ == '__main__':
    luigi.run()
