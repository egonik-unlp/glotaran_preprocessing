#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import sys
import re



class Glotafile:
    def __init__(self, file, fraction=.10):
        self.file=file
        self.fraction=fraction

    def parse_wavelengths(self):
        file=open(self.file)
        list_of_lines=[line for line in file if line != "\n"]
        wavelengths_=list_of_lines[1].split(",")[1:-1]
        wavelengths_proc=[float(re.findall(r"\d*\.\d*",wavelength)[0]) for wavelength in wavelengths_]
        wavelengths_proc.append("")
        wavelengths=np.array(wavelengths_proc)
        file.close()
        return wavelengths
    @property
    def headers(self):
        wavelengths=self.parse_wavelengths()
        headers_=np.full((int(wavelengths.shape[0]),4),"",dtype=object)
        headers_[0]=[self.file,"Holi","wavelength explicit","intervalnr {}".format(wavelengths.shape[0]-1)]
        return np.vstack((headers_.T,wavelengths))
    @property
    def body(self):
        data_array=pd.read_csv(self.file, sep=',', header=None, skiprows=11).to_numpy()
        time=data_array[:,0]*1000
        time=(time - time[int(time.shape[0]*self.fraction)]).reshape(-1,1)
        decays=data_array[:,1:-1]
        return np.hstack((time, decays))


    def build(self, filename=None):
        if not filename:
            filename="results/{}_glotaran.ascii".format(self.file[:-4])
        data=np.vstack((self.headers,self.body))
        np.savetxt(filename, data, fmt="%s", delimiter='\t')
        return data



if __name__=="__main__":
    if len(sys.argv)==1:
        print("Uso incorrecto, ingrese directorio o archivo a convertir. Para el directorio actual ingrese '.'")
    elif len(sys.argv)==2:
        if sys.argv[1][-4:] != ".txt":
             for file in os.listdir():
                 path=os.path.join(os.getcwd(), file)
                 glo=Glotafile(path).build()
        else:
            glo=Glotafile(sys.argv[1]).build()
    else:
        for param in sys.argv[1:]:
            if param[-4:]=='.txt':
                glo=Glotafile(param).build()
            else:
                print("El archivo {} no fue procesado, porque no tiene extensión .txt".format(param))
            



