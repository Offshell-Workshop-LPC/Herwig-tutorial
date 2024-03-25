import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Herwig7Settings.Herwig7StableParticlesForDetector_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7CH3TuneSettings_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7_7p1SettingsFor7p2_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7LHECommonSettings_cfi import *
from Configuration.Generator.Herwig7Settings.Herwig7LHEPowhegSettings_cfi import *



externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/2018/13TeV/powheg/V2/gg_H_quark-mass-effects_ZZ_NNPDF31_13TeV/gg_H_quark-mass-effects_ZZ2l2nu_NNPDF31_13TeV_M250/v2/gg_H_quark-mass-effects_ZZ2l2nu_NNPDF31_13TeV_M250.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True),
    postGenerationCommand = cms.untracked.vstring('mergeLHE.py', '-n', '-i', 'thread*/cmsgrid_final.lhe', '-o', 'cmsgrid_final.lhe'),
)


generator = cms.EDFilter("Herwig7HadronizerFilter",
    herwig7StableParticlesForDetectorBlock,
    herwig7CH3SettingsBlock,
    herwig7LHECommonSettingsBlock,
    herwig7LHEPowhegSettingsBlock,
    herwig7p1SettingsFor7p2Block,
    configFiles = cms.vstring(),
    process_settings = cms.vstring('set /Herwig/EventHandlers/EventHandler:CascadeHandler:MPIHandler NULL'),
    parameterSets = cms.vstring('herwig7CH3PDF', 'herwig7CH3AlphaS', 'herwig7CH3MPISettings', 'hw_7p1SettingsFor7p2', 'herwig7StableParticlesForDetector', 'hw_lhe_common_settings', 'hw_lhe_powheg_settings', 'process_settings'),
    crossSection = cms.untracked.double(-1),
    dataLocation = cms.string('${HERWIGPATH:-6}'),
    eventHandlers = cms.string('/Herwig/EventHandlers'),
    filterEfficiency = cms.untracked.double(1.0),
    generatorModule = cms.string('/Herwig/Generators/EventGenerator'),
    repository = cms.string('${HERWIGPATH}/HerwigDefaults.rpo'),
    run = cms.string('GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7'),
    runModeList = cms.untracked.string("read,run"),
    seed = cms.untracked.int32(12345)
)


from GeneratorInterface.RivetInterface.rivetAnalyzer_cfi import rivetAnalyzer

rivetAnalyzer.AnalysisNames = cms.vstring(
    "MC_JETS",
    "MC_MUONS",
    "MC_XS",
    "MC_GENERIC"
)
rivetAnalyzer.OutputFile = cms.string("LO_MG_lhe_DY.yoda")

ProductionFilterSequence = cms.Sequence(generator*rivetAnalyzer)
