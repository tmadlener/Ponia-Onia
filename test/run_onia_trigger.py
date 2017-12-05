input_filename = [
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/031/00000/FAFBED74-0D56-E711-B70C-02163E013448.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/046/00000/46EC52EE-2456-E711-AE33-02163E019C74.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/047/00000/76B44962-2B56-E711-A977-02163E01A597.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/050/00000/8EE75C34-3C56-E711-8F5C-02163E013742.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/050/00000/F079E200-4156-E711-AF08-02163E01A2C5.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/050/00000/F241B6D8-5256-E711-99AC-02163E011AEC.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/056/00000/5EE19BE9-7356-E711-A395-02163E01339B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/056/00000/E83D0DB5-8756-E711-92E2-02163E01A679.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/057/00000/0C946421-B856-E711-B27A-02163E01383B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/057/00000/7445EC0A-A656-E711-BAB2-02163E014794.root',
]

lumi_json = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'

import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register('globalTag', '', VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string, '')
options.parseArguments()

if not options.globalTag:
    import sys
    sys.exit()

import FWCore.ParameterSet.Config as cms
process = cms.Process('Rootuple')

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

### TODO:
### * global tag according to run
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, options.globalTag, '')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 20000

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring(input_filename))

# ### TODO:
# ### * remove before running with crab
import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = lumi_json).getVLuminosityBlockRange()


process.TFileService = cms.Service("TFileService",fileName = cms.string("rootuple_onia.root"))
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))

process.load("Ponia.OniaPhoton.slimmedMuonsTriggerMatcher2017_cfi")

# In MiniAOD, the PATMuons are already present. We just need to run Onia2MuMu, with a selection of muons.
process.oniaSelectedMuons = cms.EDFilter('PATMuonSelector',
   src = cms.InputTag('slimmedMuonsWithTrigger'),
   cut = cms.string('muonID(\"TMOneStationTight\")'
                    ' && abs(innerTrack.dxy) < 0.3'
                    ' && abs(innerTrack.dz)  < 20.'
                    ' && innerTrack.hitPattern.trackerLayersWithMeasurement > 5'
                    ' && innerTrack.hitPattern.pixelLayersWithMeasurement > 0'
                    ' && innerTrack.quality(\"highPurity\")'
                    ' && (abs(eta) <= 1.4 && pt > 4.)'
   ),
   filter = cms.bool(True)
)

process.load("HeavyFlavorAnalysis.Onia2MuMu.onia2MuMuPAT_cfi")
process.onia2MuMuPAT.muons=cms.InputTag('oniaSelectedMuons')
process.onia2MuMuPAT.primaryVertexTag=cms.InputTag('offlineSlimmedPrimaryVertices')
process.onia2MuMuPAT.beamSpotTag=cms.InputTag('offlineBeamSpot')
process.onia2MuMuPAT.higherPuritySelection=cms.string("")
process.onia2MuMuPAT.lowerPuritySelection=cms.string("")
process.onia2MuMuPAT.dimuonSelection=cms.string("(0.85 < mass && mass < 1.2) || (8.5 < mass && mass < 11.5)")
process.onia2MuMuPAT.addMCTruth = cms.bool(False)

process.triggerSelection = cms.EDFilter("TriggerResultsFilter",
                                        triggerConditions = cms.vstring(
                                            'HLT_Dimuon10_Upsilon_Barrel_Seagulls_v*',
                                            'HLT_Dimuon14_Phi_Barrel_Seagulls_v*',

                                            'HLT_Dimuon12_Upsilon_eta1p5_v*',

                                            'HLT_Dimuon24_Upsilon_noCorrL1_v*',
                                            'HLT_Dimuon24_Phi_noCorrL1_v*',

                                            'HLT_Mu20_TkMu0_Phi_v*',
                                            'HLT_Mu25_TkMu0_Ph_v*'
                                            'HLT_Mu25_TkMu0_Onia_v*',
                                            'HLT_Mu30_TkMu0_Onia_v*'
                                        ),
                                        hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
                                        l1tResults = cms.InputTag( "" ),
                                        throw = cms.bool(False)
                                        )

process.Onia2MuMuFiltered = cms.EDProducer('DiMuonFilter',
      OniaTag             = cms.InputTag("onia2MuMuPAT"),
      singlemuonSelection = cms.string(""),
      dimuonSelection     = cms.string("(0.85 < mass && mass < 1.2) || (8.5 < mass && mass < 11.5) && charge==0 && userFloat('vProb') > 0.01"),
      do_trigger_match    = cms.bool(True),
      HLTFilters          = cms.vstring(
          'hltDisplacedmumuFilterDimuon10UpsilonBarrelnoCow',
          'hltDisplacedmumuFilterDimuon14PhiBarrelnoCow',

          'hltDisplacedmumuFilterDimuon12Upsilons',

          'hltDisplacedmumuFilterDimuon24UpsilonsNoCorrL1',
          'hltDisplacedmumuFilterDimuon24PhiBarrelNoCorrL1',

          'hltDiMuonGlb20Trk0DzFiltered0p2',
          'hltDiMuonGlb25PhiTrk0DzFiltered0p2'
          'hltDiMuonGlb25Trk0DzFiltered0p2',
          'hltDiMuonGlb30Trk0DzFiltered0p2',
      ),
)

process.DiMuonCounter = cms.EDFilter('CandViewCountFilter',
    src       = cms.InputTag("Onia2MuMuFiltered"),
    minNumber = cms.uint32(1),
    filter    = cms.bool(True)
)

process.dimuonSequence = cms.Sequence(
    process.triggerSelection *
    process.slimmedMuonsWithTriggerSequence *
    process.oniaSelectedMuons *
    process.onia2MuMuPAT *
    process.Onia2MuMuFiltered *
    process.DiMuonCounter
)

### TODO: This currently does some duplicated work, but should work for now
process.load('Ponia.Onia.Onia2MuMuRootuplerCustom_cfi')
process.rootuple.onia_mass_cuts = cms.vdouble(0.85, 11.5)
process.rootuple.isMC = cms.bool(False)
process.rootuple.OnlyBest = cms.bool(False)

process.rootuple.HLTLastFilters = cms.vstring(
    process.Onia2MuMuFiltered.HLTFilters
)

process.rootuple.FilterNames = cms.vstring(
    'HLT_Dimuon10_Upsilon_Barrel_Seagulls',
    'HLT_Dimuon14_Phi_Barrel_Seagulls',

    'HLT_Dimuon12_Upsilon_eta1p5',

    'HLT_Dimuon24_Upsilon_noCorrL1',
    'HLT_Dimuon24_Phi_noCorrL1',

    'HLT_Mu20_TkMu0_Phi',
    'HLT_Mu25_TkMu0_Phi'

    'HLT_Mu25_TkMu0_Onia',
    'HLT_Mu30_TkMu0_Onia'
)

process.p = cms.Path(process.dimuonSequence*process.rootuple)
