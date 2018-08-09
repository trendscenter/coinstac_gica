load('../test/output/remote/simulatorRun/S.mat')
load('../test/remote/simulatorRun/mask.mat')

nii = load_nii('../test/remote/simulatorRun/template.nii');
img1 = brad_fill_mask(mask,length(mask),S');
img2 = reshape(img1',53,63,46,100);
nii.img = img2;
save_nii(nii, 'components.nii');

