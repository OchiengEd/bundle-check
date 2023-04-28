#!/usr/bin/env python3
from certbundle.validate import AnnotationChecks, CSVChecks
import yaml
import os
import re
import sys
            
class Bundle():

    def __init__(self, path :str, debug :bool = False) -> None:
        self.path = path
        self.debug = debug

    def __build_dir__(self, target: str) -> str:
        return os.path.join(self.path, target)
    
    def __manifests_dir(self) -> str | None:
        dir = self.__build_dir__('manifests')
        return dir if os.path.isdir(dir) else None

    def __tests_dir(self) -> str | None:
        dir = self.__build_dir__('tests')
        return dir if os.path.isdir(dir) else None

    def __metadata_dir(self) -> str:
        dir = self.__build_dir__('metadata')
        return dir if os.path.isdir(dir) else None

    def contents(self) -> list[str]:
        return os.listdir(self.path)
    
    def read(self, filename) -> dict:
        if not self.is_yaml(filename):
            return None
        
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
        return dict()

    def is_yaml(self, filename) -> bool:
        return os.path.isfile(filename) and \
            filename.endswith(('.yaml', '.yml'))
    
    def annotations(self) -> dict | None:
        if os.path.basename(self.__metadata_dir()) in self.contents():
            annotations = os.path.join(self.__metadata_dir(), 'annotations.yaml')
            if not os.path.isfile(annotations):
                print('error: the annotations.yaml file was not found at %s' 
                      % annotations)

        return self.read(annotations)
            
    def csv(self):
        csv_regex = re.compile(r"[a-z-]+\.clusterserviceversion.[yaml]{3,4}")
        if os.path.basename(self.__manifests_dir()) in self.contents():
            for f in os.listdir(self.__manifests_dir()):
                match = csv_regex.match(f)
                if match:
                    csv = os.path.join(self.__manifests_dir(), match.group(0))
                    
        return self.read(csv)
    
    def test(self):
        print('Running test')

        subdirs = ['metadata','manifests']
        result = set(x in [dir for dir in os.listdir(self.path)] for x in subdirs)
        if not list(result)[0]:
            print('error: invalid bundle directory')
            sys.exit()

        annotation_checks = AnnotationChecks(
            self.annotations(),
            self.csv(), 
            self.debug)
        anno_result = annotation_checks.run()

        csv_checks = CSVChecks(
            self.annotations(),
            self.csv(),
            self.debug)
        csv_result = csv_checks.run()
        

        if csv_result or anno_result:
            print('all tests PASSED')
        else:
            print('some tests failed. Re-run command with "--debug"')
