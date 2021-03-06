from collections import defaultdict
from itertools import cycle
from os import environ
from os.path import join

import pandas as pd

import what_the_flux.what_the_flux as wtf  # noqa: F401 unused import

COCO_PATH = "C:/Users/Filip/Desktop/ASTRprojekt/template2"  # change to source directory of this code
SPEC_PATH = join(environ['HOME'], 'DropboxWIS/my_spectra_collections')

SCRIPTS_PATH = join(COCO_PATH, 'Codes_Scripts')
FILTER_PATH = FILTERS_PATH = join(COCO_PATH, "Inputs/Filters")
PRIORs_PATH = join(COCO_PATH, 'Inputs/2DIM_priors')
DATASPEC_PATH = join(COCO_PATH, "Inputs/Spectroscopy")
DATAINFO_FILEPATH = join(COCO_PATH, "Inputs/SNe_Info/info.dat")
PHOTOMETRY_PATH = join(COCO_PATH, "Inputs/Photometry")
DATALC_PATH = join(COCO_PATH, "Inputs/Photometry/4_LCs_late_extrapolated")

OUTPUT_DIR = join(COCO_PATH, "Outputs")

color_dict = {'Bessell_U': 'blue', 'Bessell_B': 'royalblue', 'Bessell_V': 'limegreen',
              'Bessell_R': 'red', 'Bessell_I': 'mediumvioletred',
              'sdss_g': 'darkgreen', 'ptf_g': 'darkgreen', "sdss_g'": 'darkgreen', 'sdss_i': 'indianred',
              "sdss_i'": 'indianred', 'sdss_r': 'darkred', "sdss_r'": 'darkred', 'sdss_z': 'sienna',
              "sdss_z'": 'sienna',
              'sdss_u': 'darkblue', "sdss_u'": 'darkblue', 'Y': 'salmon', 'H': 'darkred', 'J': 'k',
              'Ks': 'brown', 'K': 'brown', 'swift_UVW1': 'indigo', 'swift_UVW2': 'darkblue',
              'swift_UVM2': 'darkmagenta', 'swift_U': 'plum', 'swift_V': 'teal', 'swift_B': 'powderblue',
             'ps_g':u"#4daf4a",'ps_r':u"#e41a1c",'ps_i':u"#832db6",'ps_z':u"#656364",'ztf_g':u"#b9ac70",'ztf_r':u"#bd1f01"}

mark_dict = {'Bessell_U': 'o', 'Bessell_B': 'o', 'Bessell_V': 'o', 'Bessell_R': 'o', 'Bessell_I': 'o',
             'sdss_g': 's', 'ptf_g': 's', "sdss_g'": 's', 'sdss_i': 's', "sdss_i'": 's',
             'sdss_r': 's', "sdss_r'": 's', 'sdss_z': 's', "sdss_z'": 's', 'sdss_u': 's', "sdss_u'": 's',
             'Y': 'o', 'H': 'o', 'J': 'o', 'Ks': 'o', 'K': 'o',
             'swift_UVW1': 'D', 'swift_UVW2': 'D', 'swift_UVM2': 'D', 'swift_U': 'D',
             'swift_V': 'D', 'swift_B': 'D',
            'ps_g':'o','ps_r':'o','ps_i':'o','ps_z':'o','ZTF_g':'o','ZTF_r':'o'}

marks = iter(cycle(set(mark_dict.values())))
colors = iter(cycle(set(color_dict.values())))
color_dict = defaultdict(lambda: next(colors), **{})
mark_dict = defaultdict(lambda: next(marks), **{})

FILTERDICT_PATH = join(PHOTOMETRY_PATH, 'filterdict.json')
FILTERMAGSYS_PATH = join(PHOTOMETRY_PATH, 'filtermagsystems.json')

info_file = info_objects = pd.read_csv(DATAINFO_FILEPATH, comment='#', delimiter=' ')
info_objects.set_index('Name', drop=False, inplace=True)
name_type = dict(zip(info_objects['Name'], info_objects['Type']))

# OFEK: detected use of type (possible discrimination between "II and IIn" and rest):
se_sne = [row.Name for i, row in info_objects.iterrows() if
          row.Type in ['IIb', 'Ib', 'Ic', 'Ic-BL', 'Ibc-pec', 'Ia']]  # OFEK: added Ia
hydr_sne = [row.Name for i, row in info_objects.iterrows() if row.Type in ['IIn', 'II', 'IIL', 'IIP', '1987A', '87A']]

fallbackepxrange = 20  # days
