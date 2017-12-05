import FWCore.ParameterSet.Config as cms

rootuple = cms.EDAnalyzer('Onia2MuMuRootuplerCustom',
                          dimuons = cms.InputTag("onia2MuMuPAT"),
                          muons = cms.InputTag("muons", "", "RECO"),
                          primaryVertices = cms.InputTag("offlinePrimaryVertices"),
                          TriggerResults = cms.InputTag("TriggerResults", "", "HLT"),
                          onia_pdgid = cms.uint32(443),
                          onia_mass_cuts = cms.vdouble(2.9,3.3),
                          FilterNames = cms.vstring(
                              'HLT_Dimuon10_PsiPrime_Barrel_Seagulls',
                              'HLT_Dimuon10_Upsilon_Barrel_Seagulls',
                              'HLT_Dimuon20_Jpsi_Barrel_Seagulls',
                              'HLT_Dimuon14_Phi_Barrel_Seagulls',

                              'HLT_Dimuon12_Upsilon_eta1p5',
                              'HLT_Dimuon18_PsiPrime',
                              'HLT_Dimuon25_Jpsi',

                              'HLT_Dimuon18_PsiPrime_noCorrL1',
                              'HLT_Dimuon24_Upsilon_noCorrL1',
                              'HLT_Dimuon24_Phi_noCorrL1',
                              'HLT_Dimuon25_Jpsi_noCorrL1',

                              'HLT_Mu25_TkMu0_Onia',
                              'HLT_Mu30_TkMu0_Onia',
                              'HLT_Mu20_TkMu0_Phi',
                              'HLT_Mu25_TkMu0_Phi'
                          ),
                          SingleFilterNames = cms.vstring(
                              'HLT_Mu7p5_Track2_Jpsi'
                          ),
                          isMC = cms.bool(True),
                          OnlyBest = cms.bool(True),
                          OnlyGen = cms.bool(False),
                          HLTLastFilters = cms.vstring(
                              'hltDisplacedmumuFilterDimuon10PsiPrimeBarrelnoCow',
                              'hltDisplacedmumuFilterDimuon10UpsilonBarrelnoCow',
                              'hltDisplacedmumuFilterDimuon20JpsiBarrelnoCow',
                              'hltDisplacedmumuFilterDimuon14PhiBarrelnoCow',

                              'hltDisplacedmumuFilterDimuon12Upsilons',
                              'hltDisplacedmumuFilterDimuon18PsiPrimes',
                              'hltDisplacedmumuFilterDimuon25Jpsis',

                              'hltDisplacedmumuFilterDimuon18PsiPrimesNoCorrL1',
                              'hltDisplacedmumuFilterDimuon24UpsilonsNoCorrL1',
                              'hltDisplacedmumuFilterDimuon25JpsisNoCorrL1',
                              'hltDisplacedmumuFilterDimuon24PhiBarrelNoCorrL1',

                              'hltDiMuonGlb25Trk0DzFiltered0p2',
                              'hltDiMuonGlb30Trk0DzFiltered0p2',
                              'hltDiMuonGlb20Trk0DzFiltered0p2',
                              'hltDiMuonGlb25PhiTrk0DzFiltered0p2'
                          ),
                          propagatorStation1 = cms.PSet(
                                                        useStation2 = cms.bool(False),
                                                        useTrack = cms.string("tracker"),
                                                        useState = cms.string("atVertex"),  # for AOD
                                                        useSimpleGeometry = cms.bool(True),
                          ),
                          propagatorStation2 = cms.PSet(
                                                        useStation2 = cms.bool(True),
                                                        useTrack = cms.string("tracker"),
                                                        useState = cms.string("atVertex"),  # for AOD
                                                        useSimpleGeometry = cms.bool(True),
                          )
)
