# Herwig Tutorial - CMS Off-shell Higgs Workshop

## Setup

For this tutorial we will use CMSSW_10_6_38 on lxplus 7. To set this up, run the following commands:

```
# login to lxplus7

cmsrel CMSSW_10_6_38
cd CMSSW_10_6_38/src
cmsenv
# Clone this repository into the src directory:
git clone git@github.com:Offshell-Workshop-LPC/Herwig-tutorial.git
# Build cmssw so that it can find the gen fragments:
scram b -j 4
```


## Showering external lhe files

In this repository we provide a number of generator fragments to run the different examples. A fragment is a part of a configuration containing only the information specific to the physics process. To convert this into a full configuration one needs to use the cmsDriver command, which adds details of output formats and the conditions for the run. Create a test directory and run this command:

```
mkdir -p test/external_lhe
cd test/external_lhe
cmsDriver.py Herwig-tutorial/external_lhe/python/GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7_cff.py --python_filename GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7_cfg.py --eventcontent RAWSIM,NANOAODGEN --datatier GEN,NANOAOD --fileout file:GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN,NANOGEN --geometry DB:Extended --era Run2_2018 --no_exec --mc --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" -n 5000
```

The completed fragment can then be run using the "cmsRun" command:

```
cmsRun GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7_cfg.py
```

This should produce a large number of files:

 - HerwigConfig.in - Herwig input file produced by CMSSW
 - GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7.run - non-human readable run card produced by Herwig
 - GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7-S123456790.log - Detailed Herwig log (includes full event record for a few events)
 - GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7-S123456790.out - Herwig process summary (including xs)
 - GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7-S123456790.tex - Herwig credits
 - GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7.root - CMS GEN data-tier ROOT file for further processing
 - GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7_inNANOAODGEN.root - Events in NanoAOD-like format
 - GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7.yoda - Rivet histograms
 
Try having a look in the .in, .log and .out text files, as well as opening the NanoAODGen file. You can then make the rivet plots using the following command:

```
rivet-mkhtml --mc-errs GluGluHToZZTo2L2Nu_M250_Powheg_JHUGen_Herwig7.yoda
```

## Herwig in matchbox mode

Matchbox is a mode of Herwig that allows to use external (NLO) ME providers to do the showering and the hadronization, all in one go within Herwig i.e., no need to produce LHE files and pass them for the matching/merging/hadronization to Herwig. 

A first sample with NLO DY->ll exists for Run 2 with UL conditions, consisting of 120 M events and is available in [DAS](https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FDYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7%2F*ext1-v2%2F*). 

A fragment for this process is provided and can be run in much the same way as before:

```
mkdir -p test/matchbox
cd test/matchbox

cmsDriver.py CMS_Herwig_tutorial_2024/matchbox/python/DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_cff.py --python_filename DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_cfg.py --eventcontent RAWSIM,NANOAODGEN --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,NANOAOD --fileout file:DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7.root --conditions auto:mc --step GEN,NANOGEN --geometry DB:Extended --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" --no_exec --mc -n 5000 

# This will speed-up generation for the tutorial 
# Do not do it, if you make any changes in the configuation

cp /afs/cern.ch/user/t/theofil/public/CMS_Herwig_tutorial_2024/Herwig-cache.CMSSW_10_6_38.lxplus7.tar.bz2 .
tar -xjvf Herwig-cache.CMSSW_10_6_38.lxplus7.tar.bz2


cmsRun DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_cfg.py 
```

### Exercise: modify configuration to use dipole shower
We have to edit the Herwig configuration inside the ```DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_cff.py ``` fragment. For this purpose will will clone this configuration into a new file 
```
cp $CMSSW_BASE/src/CMS_Herwig_tutorial_2024/matchbox/python/DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_cff.py $CMSSW_BASE/src/CMS_Herwig_tutorial_2024/matchbox/python/DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_dipole_cff.py

```
and edit it inside 
```
nano $CMSSW_BASE/src/CMS_Herwig_tutorial_2024/matchbox/python/DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_dipole_cff.py
````

so that the following lines appear:
```
   '# read Matchbox/MCatNLO-DefaultShower.in',
   'read Matchbox/MCatNLO-DipoleShower.in',   

   '# read Matchbox/FiveFlavourScheme.in',
   'read snippets/DipoleShowerFiveFlavours.in',   
```
In the end, do not forget to run 
```
scram b
```
so that CMSSW is informed for the new card. You can find an (untested) version of the configuration in MCM [PPD-RunIISummer20UL18GEN-00019](https://cms-pdmv-prod.web.cern.ch/mcm/edit?db_name=requests&prepid=PPD-RunIISummer20UL18GEN-00019&page=0) 


```
mkdir dipole
cd dipole

cmsDriver.py CMS_Herwig_tutorial_2024/matchbox/python/DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_dipole_cff.py --python_filename DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_dipole_cfg.py --eventcontent RAWSIM,NANOAODGEN --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,NANOAOD --fileout file:DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_dipole.root --conditions auto:mc --step GEN,NANOGEN --geometry DB:Extended --customise_commands process.MessageLogger.cerr.FwkReport.reportEvery="int(1000)" --no_exec --mc -n 5000 

# This will speed-up generation for the tutorial 
# Do not do it, if you make any changes in the configuation

cp /afs/cern.ch/user/t/theofil/public/CMS_Herwig_tutorial_2024/Herwig-cache_dipole.CMSSW_10_6_38.lxplus7.tar.bz2 .
tar -xjvf Herwig-cache_dipole.CMSSW_10_6_38.lxplus7.tar.bz2


cmsRun DYToLL_NLO_5FS_TuneCH3_13TeV_matchbox_herwig7_dipole_cfg.py  >& output.txt &
```

Similarly, more cards could be tested modifying accordingly the commands passed inside Herwig through the CMSSW-Herwig-interface. Contact us if you want to get help on any particular process!
