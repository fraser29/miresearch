# miresearch
Organisation and automation tools for medical imaging research data

## About

This is a collection of classes for following OOP principles for organisation of research data for medical imaging research studies. 

It takes advantage of the dicom standard and the package [spydcmtk](https://github.com/fraser29/spydcmtk) for automating and generalising many typical steps with the intention of making the researcher's life easier. 

This package may be easily adapted and expanded upon for a high level control over your research data. Or, it may be used as is for basic structure and organisation of data and automation of common tasks. 

## Class structure

AbstractSubject
    


# Exposed commandline tool: miresearch

```bash

miresearch -h
usage:  ... 

Actions:
  -Load LOADPATH        Path to load dicoms from (file / directory / tar / tar.gz / zip)
  -LOAD_MULTI           Combine with "Load": Load new subject for each subdirectory under loadPath
  -LOAD_MULTI_FORCE     Combine with "Load": Force to ignore studyUIDs and load new ID per subdirectory
  -WatchDirectory WATCHDIRECTORY
                        Will watch given directory for new data and load as new study
  -SummaryCSV SUMMARYCSV
                        Write summary CSV file (give output file name)

```

# Configuration

miresearch uses a miresearch.conf file for configuration. 

By default miresearch.conf files are search for in the following locations: 

1. source_code_directory/miresearch.conf (file with default settings)
2. $HOME/miresearch.conf
3. $HOME/.miresearch.conf
4. $HOME/.config/miresearch.conf
5. Full file path defined at environment variable: "MIRESEARCH_CONF"
6. Full path passed as commandline argument to `miresearch`

Files are read in the above order with each subsequent variable present overwritting any previously defined. 
For information on files found and variables used run:

`miresearch -INFO` 

# Documentation

For full documentation see [wiki](https://github.com/fraser29/miresearch/wiki)