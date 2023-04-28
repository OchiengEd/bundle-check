#!/usr/bin/env python3
import re
from os import path

class Valid(object):
    def __init__(self) -> None:
        pass

    def read(self, key: str):
        try:
            value = key
        except KeyError:
            value = ''
        return value

    def run(self) -> bool:
        raise NotImplementedError('error: run method not implemented')

class AnnotationChecks(Valid):
    def __init__(self, annotations: dict, csv: dict, debug: bool) -> None:
        super().__init__()
        self.csv = csv
        self.annotations = annotations
        self.debug = debug

    def check_openshift_versions(self) -> str:
        versions = self.read(self.annotations['annotations'] \
                                 ['com.redhat.openshift.versions'])
        if self.debug:
            print('supported openshift versions: %s' % versions)
        return True if versions else False

    def operator_name_exists(self) -> bool:
        name = self.read(self.annotations['annotations'] \
                         ['operators.operatorframework.io.bundle.package.v1'])
        if self.debug:
            print('operator name: %s' % name)
        return True if name else False

    def default_channel_exists(self) -> bool:
        default = self.read(self.annotations['annotations'] \
                            ['operators.operatorframework.io.bundle.channel.default.v1'])
        if self.debug:
            print('default channel: %s' % default)
        return True if default else False
    
    def operator_channels_exists(self) -> bool:
        channels = self.read(self.annotations['annotations'] \
                            ['operators.operatorframework.io.bundle.channels.v1'])
        if self.debug:
            print('operator channels: %s' % channels)
        return True if channels else False
    
    def run(self) -> bool:
        print('running annotation checks...')
        if not self.operator_name_exists():
            return False
    
        if not self.check_openshift_versions():
            return False
        
        if not self.default_channel_exists():
            return False
        
        if not self.operator_channels_exists():
            return False
        
        return True

class CSVChecks(Valid):
    def __init__(self, annotations: dict, csv: dict, debug: bool) -> None:
        super().__init__()
        self.csv = csv
        self.annotations = annotations
        self.debug = debug

    def operator_name_exists(self) -> bool:
        name = self.read(self.csv['metadata']['name'])
        if self.debug:
            if name:
                print('package name: %s' % name)
            else:
                print('package name not found')

        return True if name else False
    
    def __related_images(self) -> list[str]:
        return [item['image'] for item in self.read(self.csv['spec']['relatedImages'])]
    
    def __all_container_images(self) -> list[str]:
        images = set(self.__related_images())
        
        # add image from .metadata.annotations.containerImage
        if self.read(self.csv['metadata']['annotations']['containerImage']):
            images.add(self.csv['metadata']['annotations']['containerImage'])

        # add image from deployment containers
        for deployment in self.csv['spec']['install']['spec']['deployments']:
            for container in deployment['spec']['template']['spec']['containers']:
                images.add(container['image'])
        return list(images)
            
    def related_images_defined(self) -> bool:
        relatedImages = self.__related_images()
        if self.debug:
            if len(relatedImages) > 0:
                print('found .spec.relatedImages')
                for img in relatedImages:
                    print(' * %s' % img)
            else:
                print('error: .spec.relatedImages not found')
        return True if len(relatedImages) > 0 else False
    
    def is_image_digest(self, image: str) -> bool:
        idigest = re.compile(r'[a-z0-9-]+\@sha256\:[a-fA-F0-9]{64}[$]?')
        match = idigest.match(path.basename(image).strip())
        return True if match else False

    def verify_image_digests(self) -> bool:
        for img in self.__all_container_images():
            if not self.is_image_digest(img):
                print('error: the image %s not using digest')
                return False
        return True

    def run(self) -> bool:
        if not self.operator_name_exists():
            return False
        
        if not self.related_images_defined():
            return False
        
        if not self.verify_image_digests():
            return False

        return True
       