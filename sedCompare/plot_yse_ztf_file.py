#!/usr/bin/env python3
# Written by Kostantin Malanchev & Patrick Aleo
# Modified by Filip Matasic

import os
import glob

import dataclasses
import pandas as pd
import matplotlib.pyplot as plt

from astropy.io import ascii
from astropy.table import Table

import numpy as np

@dataclasses.dataclass
class Observation:
    MJD: float
    FLUX: float
    FLUXERR: float
    MAG: float
    MAGERR: float
    FLT: str


REDSHIFT_UNKNOWN = -99.0


def read_YSE_ZTF_snana_dir(dir_name,keep_ztf=True):
    """
    file_path : str
        The file path to the combined YSE+ZTF light curve SNANA-style format data file.
    keep_ztf : bool
        True: Plots including ZTF data
        False : Plots not include ZTF data
    
    """
    snid_list = []
    meta_list = []
    yse_ztf_fp_df_list = []
    
    for file_path in sorted(glob.glob(dir_name+'/*')):
        #print(file_path)
    
        meta = {}
        lc = []
        with open(file_path) as file:
            for line in file:
                try:
                    if line.startswith('SNID: '):
                        _, snid = line.split()
                        meta['object_id'] = snid
                        meta['original_object_id'] = snid

                    if line.startswith('RA: '):
                        _, ra, _ = line.split()
                        meta['ra'] = float(ra)

                    if line.startswith('DECL: '):
                        _, decl, _ = line.split()
                        meta['dec'] = float(decl)

                    if line.startswith('MWEBV: '):
                        _, mwebv, _, _mwebv_error, *_ = line.split()
                        meta['mwebv'] = float(mwebv)

                    if line.startswith('REDSHIFT_FINAL: '):
                        try:
                            _, redshift, _, _redshift_error, _ = line.split()
                        # 2020roe has empty redshift
                        except ValueError:
                            redshift = REDSHIFT_UNKNOWN
                        meta['redshift'] = float(redshift)

                    if line.startswith('NOBS_wZTF: ') or line.startswith('NOBS_AFTER_MASK: '):
                        _, desired_nobs = line.split()
                        meta['num_points'] = int(desired_nobs)
                        continue
                    
                    if line.startswith('SPEC_CLASS: '):
                        try:
                            _, sn, spec_subtype = line.split()
                            meta['transient_spec_class'] = transient_spec_class = str(sn+spec_subtype)
                        except:
                            _, spec_subtype = line.split()
                            meta['transient_spec_class'] = transient_spec_class = str(spec_subtype)
                        
                    if line.startswith('SPEC_CLASS_BROAD: '):
                        try: 
                            _, sn, subtype = line.split()
                            meta['spectype_3class'] = spectype_3class = str(sn+subtype)
                        except: 
                            _, subtype = line.split() 
                            meta['spectype_3class'] = spectype_3class = str(subtype)
                        
                    if line.startswith('PARSNIP_PRED: '):
                        try: 
                            _, sn, p_pred = line.split()
                            meta['parsnip_pred_class'] = parsnip_pred_class = str(sn+p_pred)
                        except: 
                            _, p_pred = line.split() # for "NA" Prediction
                            meta['parsnip_pred_class'] = parsnip_pred_class = str(p_pred)
                        
                    if line.startswith('PARSNIP_CONF: '):
                        _, p_conf = line.split()
                        meta['parsnip_pred_conf'] = parsnip_pred_conf = str(p_conf)
                        
                    if line.startswith('SUPERPHOT_PRED: '):
                        try: 
                            _, sn, s_pred = line.split()
                            meta['superphot_pred_class'] = superphot_pred_class = str(sn+s_pred)
                        except: 
                            _, s_pred = line.split() # for "NA" Prediction
                            meta['superphot_pred_class'] = superphot_pred_class = str(s_pred)
                        
                    if line.startswith('SUPERPHOT_CONF: '):
                        _, s_conf = line.split()
                        meta['superphot_pred_conf'] = superphot_pred_conf = str(s_conf)
                        
                    if line.startswith('MAX_MJD_GAP(days): '):
                        _, max_mjd_gap = line.split()
                        meta['max_mjd_gap'] = float(max_mjd_gap)
                        
                        
                except ValueError as e:
                    print(e)
                    print(meta['object_id'])
                    raise e
                    
                    
                if not line.startswith('OBS: '):
                    continue

                _obs, mjd, flt, _field, fluxcal, fluxcalerr, mag, magerr, _flag = line.split()
                lc.append(Observation(
                    MJD=float(mjd),
                    FLT=str(flt),
                    FLUX=float(fluxcal),
                    FLUXERR=float(fluxcalerr),
                    MAG=float(mag),
                    MAGERR=float(magerr))
                )
                 

        meta.setdefault('mwebv', 0.0)

        #assert len(meta) == 13, f'meta has wrong number of values,\nmeta = {meta}'
        #assert len(lc) == meta['num_points']
        table = Table([dataclasses.asdict(obs) for obs in lc if keep_ztf or obs.FLT not in ZTF_BANDS])

        yse_ztf_fp_df = table.to_pandas()
        
        snid_list.append(snid)
        meta_list.append(meta)
        yse_ztf_fp_df_list.append(yse_ztf_fp_df)
        
    return snid_list, meta_list, yse_ztf_fp_df_list

def get_grizXY_plot(d,ax,offset):
    snid_list, meta_list, yse_ztf_fp_df_list = read_YSE_ZTF_snana_dir(dir_name=d)
    for j in range(len(snid_list)):
        g = yse_ztf_fp_df_list[j][yse_ztf_fp_df_list[j]["FLT"] == "g"]
        r = yse_ztf_fp_df_list[j][yse_ztf_fp_df_list[j]["FLT"] == "r"]
        i = yse_ztf_fp_df_list[j][yse_ztf_fp_df_list[j]["FLT"] == "i"]
        z = yse_ztf_fp_df_list[j][yse_ztf_fp_df_list[j]["FLT"] == "z"]
        x = yse_ztf_fp_df_list[j][yse_ztf_fp_df_list[j]["FLT"] == "X"]
        y = yse_ztf_fp_df_list[j][yse_ztf_fp_df_list[j]["FLT"] == "Y"]
        plotFiles(g,r,i,z,x,y,snid_list[j],ax,offset)

def plotFiles(g,r,i,z,x,y,snid,ax,offset):
    allObs = [x]#[g,r,i,z,x,y]
    plt.gca().invert_yaxis()
    for obs in allObs:
        mjds = obs['MJD'].to_numpy()
        mags = obs['MAG'].to_numpy()
        magserr = obs['MAGERR'].to_numpy()
        #plt.plot(mjds,mags)
        ax.errorbar(mjds - offset, mags,magserr, fmt='o', ms=7,alpha = 0.7,color = u"#b9ac70", elinewidth=2,label = "Real Observation (ZTF-g)")
    plt.title(snid)
    #plt.show()

#get_grizXY_plot('./toGenerate')
