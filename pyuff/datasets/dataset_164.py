import numpy as np
import os

from ..tools import _opt_fields, _parse_header_line, check_dict_for_none
from .. import pyuff

def _write164(fh, dset):
    """Writes units data - data-set 164 - to an open file fh."""
    try:
        # handle optional fields
        dset = _opt_fields(dset, {'units_description': 'User unit system',
                                        'temp_mode': 1})
        # write strings to the file
        fh.write('%6i\n%6i%74s\n' % (-1, 164, ' '))
        fh.write('%10i%20s%10i\n' % (dset['units_code'], dset['units_description'], dset['temp_mode']))
        str = '%25.16e%25.16e%25.16e\n%25.16e\n' % (
            dset['length'], dset['force'], dset['temp'], dset['temp_offset'])
        str = str.replace('e+', 'D+')
        str = str.replace('e-', 'D-')
        fh.write(str)
        fh.write('%6i\n' % -1)
    except KeyError as msg:
        raise Exception('The required key \'' + msg.args[0] + '\' not present when writing data-set #164')
    except:
        raise Exception('Error writing data-set #164')


def _extract164(blockData):
    """Extract units data - data-set 164."""
    dset = {'type': 164}
    try:
        splitData = blockData.splitlines(True)
        dset.update(_parse_header_line(splitData[2], 1, [10, 20, 10], [2, 1, 2],
                                            ['units_code', 'units_description', 'temp_mode']))
        splitData = ''.join(splitData[3:])
        splitData = splitData.split()
        dset['length'] = float(splitData[0].lower().replace('d', 'e'))
        dset['force'] = float(splitData[1].lower().replace('d', 'e'))
        dset['temp'] = float(splitData[2].lower().replace('d', 'e'))
        dset['temp_offset'] = float(splitData[3].lower().replace('d', 'e'))
    except:
        raise Exception('Error reading data-set #164')
    return dset


def dict_164(
    units_code=None,
    units_description=None,
    temp_mode=None,
    length=None,
    force=None,
    temp=None,
    temp_offset=None,
    return_full_dict=False):
    """Name: Units

    R-Record, F-Field

    :param units_code: R1 F1, Units code
    :param units_description: R1 F2, Units description
    :param temp_mode: R1 F3, Temperature mode (1-absolute, 2-relative)
    :param length: R2 F1, Length
    :param force: R2 F2, Force
    :param temp: R2 F3, Temperature
    :param temp_offset: R2 F4, Temperature offset
    :param return_full_dict: If True full dict with all keys is returned, else only specified arguments are included
    """

    dataset={'type': 164,
            'units_code':units_code,
            'units_description':units_description,
            'temp_mode':temp_mode,
            'length':length,
            'force':force,
            'temp':temp,
            'temp_offset':temp_offset}


    if return_full_dict is False:
        dataset = check_dict_for_none(dataset)

    return dataset


def prepare_test_164(save_to_file=''):
    dataset = {'type': 164,  # Universal Dataset
               'units_code': 1,  # I10, units code
               'units_description': 'SI units',  # 20A1, units description
               'temp_mode': 1,  # I10, temperature mode
               # Unit factors
               # for converting universal file units to SI.
               # To convert from universal file units to SI divide by
               # the appropriate factor listed below.
               'length': 3.28083989501312334,  # D25.17, length
               'force': 2.24808943099710480e-01,  # D25.17, force
               'temp': 1.8,  # D25.17, temperature
               'temp_offset': 459.67,  # D25.17, temperature offset
               }
    dataset_out = dataset.copy()

    if save_to_file:
        if os.path.exists(save_to_file):
            os.remove(save_to_file)
        uffwrite = pyuff.UFF(save_to_file)
        uffwrite._write_set(dataset, 'add')

    return dataset_out



