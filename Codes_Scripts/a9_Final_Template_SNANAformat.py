import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time

from Codes_Scripts.config import *


import sys

def main(SN_NAME_):

    pycoco_path = ".//Outputs//"
    COCO_PATH
    
    using_hostNOTcorrected = False
    peak_dicts = {}
    peak_dicts['SN2020fqv']= 58945.0
    peak_dicts['SN2020oi']= 58867.162
    peak_dicts['SN2020sgf']= 59130.0
    peak_dicts['SN2019yuf']=58837.0
    peak_dicts['SN2019yvr']=58846.0
    peak_dicts['SN2020esm']=58945.0

    extend_with_sudo_spec = False
    phase_extended = np.arange(-25, 100, 2)#grid_input.Phase_grid #
    wls_fake = np.arange(1605., 11005., 5)
    flux_fake = 10**-12

    for sn in [SN_NAME_]:#SNe_lista[:]:
        #print (sn)
        header = """### %s.SED ###
    ### Mangled with pycoco, corrected for Host Extinction and MW
    ### %i-%i-%i, M. Vincenzi
    """%(sn, time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday) 
        header_noHostCorr = """### %s.SED ###
    ### Mangled with pycoco, NOT corrected for Host Extinction, corrected for MW
    ### %i-%i-%i, M. Vincenzi
    """%(sn, time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday) 

        if using_hostNOTcorrected:
            final_spectra_path = pycoco_path+'%s/FINAL_spectra_2dim/HostNotCorr/'%(sn)
        else: 
            final_spectra_path = pycoco_path+'%s/FINAL_spectra_2dim/'%(sn)
            
        final_spectra = [f for f in os.listdir(final_spectra_path) \
                             if os.path.isfile(os.path.join(final_spectra_path, f))&('.txt' in f)]
        peak = peak_dicts[sn]
        mjds = np.array([f[:8] for f in final_spectra], dtype=float)
        if len(np.unique(mjds))!=len(mjds):
            repeat_mjd = np.unique(mjds[(np.array([list(mjds).count(m) for m in mjds])==2)])[0]
            mjds[(np.array([list(mjds).count(m) for m in mjds])==2)] = np.array([repeat_mjd, repeat_mjd+0.01])
        phase = mjds-peak
        
        if using_hostNOTcorrected:
            fout = open(TMPL_path+'/PyCoCo_noHostCorr/pycoco_%s_noHostCorr.SED'%sn, 'w+')
            fout.write(header_noHostCorr)
        else:
            fout = open(COCO_PATH+'/Templates_HostCorrected/pycoco_%s.SED'%sn, 'w+')
            fout.write(header)

        
        if not extend_with_sudo_spec:
            phase_extended = phase
        
        for ph in phase_extended[phase_extended<min(phase)]:
            for w in wls_fake:
                fout.write('%.3f\t%.2f\t%.2E\n'%(ph,w,flux_fake))
        for ph,s in zip(phase, final_spectra):
            spec = pd.read_csv(final_spectra_path+s, delimiter='\t')
            resample_flux = np.interp(wls_fake, spec['#wls'].values, spec['flux'].values,
                 right=np.nan, left=np.nan)
            resample_fluxerr = np.interp(wls_fake, spec['#wls'].values, spec['fluxerr'].values,
                 right=np.nan, left=np.nan)
            resample_spec = pd.DataFrame.from_dict(zip(spec.columns,[wls_fake, resample_flux, resample_fluxerr])).dropna()
            
            tempDict = {}
            tempDict['#wls'] = resample_spec[1][0]
            tempDict['flux'] = resample_spec[1][1]
            tempDict['fluxerr'] = resample_spec[1][2]
            resample_spec = pd.DataFrame(tempDict)
                
                
            if max(resample_spec['#wls']<11000):
                wls_ext = wls_fake[wls_fake>max(resample_spec['#wls'])]
                flux_ext = np.ones(len(wls_ext))*flux_fake
                flux_err_ext = np.ones(len(wls_ext))*flux_fake
                extend_spec = resample_spec.append(pd.DataFrame.from_dict(zip(resample_spec.columns,
                                                                      [wls_ext, flux_ext, flux_err_ext])), ignore_index=True)
            else:
                extend_spec = resample_spec.copy()
            if min(resample_spec['#wls']>min(wls_fake)): 
                print (sn, 'MIN', min(resample_spec['#wls']))
            extend_spec['phase']=ph
            for p,w,f in extend_spec[['phase', '#wls','flux']].values:
                fout.write('%.3f %.2f %.2E\n'%(p,w,f))
        for ph in phase_extended[phase_extended>max(phase)]:
            for w in wls_fake:
                fout.write('%.3f %.2f %.2E\n'%(ph,w,flux_fake))

        fout.close()
