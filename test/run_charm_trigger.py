input_filename = [
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/031/00000/E629DFF7-0B56-E711-8B6A-02163E0141F0.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/046/00000/88DF6C6A-4556-E711-A5C0-02163E01A630.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/047/00000/BC06EF69-2256-E711-8932-02163E013729.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/050/00000/183B4680-3356-E711-B33A-02163E014487.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/050/00000/283634B2-4E56-E711-94F5-02163E01A618.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/050/00000/30DBC02A-3856-E711-BC0E-02163E01A69D.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/050/00000/76DD8C3A-4156-E711-99FE-02163E01A37B.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/056/00000/0C3245D6-8956-E711-BA18-02163E013892.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/056/00000/A88DDE30-6756-E711-A40A-02163E014271.root',
    '/store/data/Run2017B/Charmonium/MINIAOD/PromptReco-v1/000/297/057/00000/44363E1E-A856-E711-9893-02163E0137FA.root'
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

### TODO:
# ### * remove before running with crab
import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = lumi_json).getVLuminosityBlockRange()


process.TFileService = cms.Service("TFileService",fileName = cms.string("rootuple_charm.root"))
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
process.onia2MuMuPAT.dimuonSelection=cms.string("2.9 < mass && mass < 4.05")
process.onia2MuMuPAT.addMCTruth = cms.bool(False)

process.triggerSelection = cms.EDFilter("TriggerResultsFilter",
                                        triggerConditions = cms.vstring(
                                            'HLT_Dimuon10_PsiPrime_Barrel_Seagulls_v*',
                                            'HLT_Dimuon20_Jpsi_Barrel_Seagulls_v*',

                                            'HLT_Dimuon18_PsiPrime_v*',
                                            'HLT_Dimuon25_Jpsi_v*',

                                            'HLT_Dimuon18_PsiPrime_noCorrL1_v*',
                                            'HLT_Dimuon25_Jpsi_noCorrL1_v*',

                                            # 'HLT_Mu25_TkMu0_Onia_v*',
                                            # 'HLT_Mu30_TkMu0_Oni_v*'
                                        ),
                                        hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
                                        l1tResults = cms.InputTag( "" ),
                                        throw = cms.bool(False)
                                        )

process.Onia2MuMuFiltered = cms.EDProducer('DiMuonFilter',
      OniaTag             = cms.InputTag("onia2MuMuPAT"),
      singlemuonSelection = cms.string(""),
      dimuonSelection     = cms.string("2.9 < mass && mass < 4.05 && charge==0 && userFloat('vProb') > 0.01"),
      do_trigger_match    = cms.bool(True),
      HLTFilters          = cms.vstring(
          'hltDisplacedmumuFilterDimuon10PsiPrimeBarrelnoCow',
          'hltDisplacedmumuFilterDimuon20JpsiBarrelnoCow',

          'hltDisplacedmumuFilterDimuon18PsiPrimes',
          'hltDisplacedmumuFilterDimuon25Jpsis',

          'hltDisplacedmumuFilterDimuon18PsiPrimesNoCorrL1',
          'hltDisplacedmumuFilterDimuon25JpsisNoCorrL1',

          # 'hltDiMuonGlb25Trk0DzFiltered0p2',
          # 'hltDiMuonGlb30Trk0DzFiltered0p2',
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
process.rootuple.onia_mass_cuts = cms.vdouble(2.9, 4.05)
process.rootuple.isMC = cms.bool(False)
process.rootuple.OnlyBest = cms.bool(False)

process.rootuple.HLTLastFilters = cms.vstring(
    process.Onia2MuMuFiltered.HLTFilters
)

process.rootuple.FilterNames = cms.vstring(
    'HLT_Dimuon10_PsiPrime_Barrel_Seagulls',
    'HLT_Dimuon20_Jpsi_Barrel_Seagulls',

    'HLT_Dimuon18_PsiPrime',
    'HLT_Dimuon25_Jpsi',

    'HLT_Dimuon18_PsiPrime_noCorrL1',
    'HLT_Dimuon25_Jpsi_noCorrL1',

    # 'HLT_Mu25_TkMu0_Onia',
    # 'HLT_Mu30_TkMu0_Onia'
)

process.p = cms.Path(process.dimuonSequence*process.rootuple)
