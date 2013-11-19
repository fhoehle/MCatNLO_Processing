# Auto generated configuration file
# using: 
# Revision: 1.303.2.7 
# Source: /cvs/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: Configuration/MyGenProduction/python/TT_7TeV_mcatnlo_cff.py --step GEN,SIM --beamspot Realistic7TeV2011Collision --conditions START42_V14B::All --pileup NoPileUp --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM --filein file:test_LHE2EDM.root --fileout test_GEN-SIM42.root --python_filename TT_MCatNLO_MCatNLO_Processing_START42_V14B_GEN-SIM_cfg.py --no_exec -n -1
import FWCore.ParameterSet.Config as cms

process = cms.Process('SIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic7TeV2011Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:test_LHE2EDM.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.2 $'),
    annotation = cms.untracked.string('Showering of MC@NLO 3.4 TTbar events with Herwig+Jimmy, 7 TeV, CTEQ6M'),
    name = cms.untracked.string('$Source: /local/reps/CMSSW/CMSSW/Configuration/GenProduction/python/Attic/TT_7TeV_mcatnlo_cff.py,v $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('test_GEN-SIM42.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.GlobalTag.globaltag = 'START42_V14B::All'

process.generator = cms.EDFilter("Herwig6HadronizerFilter",
    HerwigParameters = cms.PSet(
        parameterSets = cms.vstring('herwigUEsettings', 
            'herwigMcatnlo'),
        herwigMcatnlo = cms.vstring('PTMIN      = 0.5    ! minimum pt in hadronic jet'),
        herwigUEsettings = cms.vstring('JMUEO     = 1       ! multiparton interaction model', 
            'PTJIM     = 4.449   ! 2.8x(sqrt(s)/1.8TeV)^0.27 @ 10 TeV', 
            'JMRAD(73) = 1.8     ! inverse proton radius squared', 
            'PRSOF     = 0.0     ! prob. of a soft underlying event', 
            'MAXER     = 1000000 ! max error')
    ),
    doMPInteraction = cms.bool(True),
    useJimmy = cms.bool(True),
    herwigHepMCVerbosity = cms.untracked.bool(False),
    filterEfficiency = cms.untracked.double(1.0),
    herwigVerbosity = cms.untracked.int32(0),
    emulatePythiaStatusCodes = cms.untracked.bool(True),
    comEnergy = cms.double(7000.0),
    lhapdfSetPath = cms.untracked.string(''),
    printCards = cms.untracked.bool(False),
    crossSection = cms.untracked.double(148.4),
    maxEventsToPrint = cms.untracked.int32(0)
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.RAWSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 
