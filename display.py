from .montage_nii import save_montage
from nipy.core.api import Image, vox2mni
from nipy import save_image, load_image
import numpy as np
import os
import scipy.io as sio

DEFAULT_dir = '.'
DEFAULT_template = 'template.nii'
DEFAULT_output = 'components.nii'
DEFAULT_channel = 'ch.nii'
DEFAULT_pdf = 'components.pdf'
DEFAULT_signal = 0


def save_to_image(data,
                  template_file=DEFAULT_template,
                  output_file=DEFAULT_output):
    template = load_image(template_file)
    newimg = Image(data, vox2mni(template.affine))
    save_image(newimg, output_file)
    return output_file


def montage_data(data,
                 template_file=DEFAULT_template,
                 outdir=DEFAULT_dir,
                 indir=DEFAULT_dir,
                 output_file=DEFAULT_output,
                 pdf_file=DEFAULT_pdf,
                 channel_file=DEFAULT_channel,
                 signal=DEFAULT_signal):
    template_file = os.path.join(indir, template_file)
    output_file = os.path.join(outdir, output_file)
    pdf_file = os.path.join(outdir, pdf_file)
    channel_file = os.path.join(indir, channel_file)
    out = save_to_image(data,
                        template_file=template_file,
                        output_file=output_file)
    save_montage(out, channel_file, pdf_file, signal)


def fill_mask(data, mask):
    mask = mask.flatten()
    result = np.zeros((data.shape[0], mask.size))
    result[:, mask == 1] = data
    return result
