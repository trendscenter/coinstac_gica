function niiOut = mat2nii(filename)
    % input is the filename of a .mat file containing a spatial map.
    niiTemplate = load_nii('/export/mialab/users/bbaker/projects/djica/niiTemp/template.nii');
    dimTemplate = niiTemplate.hdr.dime.dim;
    mapDims = dimTemplate(2:5);
    if isempty(findstr(filename,'.mat'))
        filename = [filename '.mat'];
    end
    loadVars = load(filename);
    loadFields = fieldnames(loadVars);
    newDims = zeros(1,4);
    niiOut = niiTemplate;
    for f=1:numel(loadFields)
        thisField = loadVars.(loadFields{f});
        thisField = thisField(1:50,:);
        thisSize = size(thisField);
        %thisSize = [50 53 63 46]

        if nnz(ismember(thisSize,mapDims)) == 4 & ~(thisSize == mapDims)
            [i a] = sort(thisSize);
            [i b] = sort(mapDims);
            permMap = b(a);
            niiOut.img = permute(thisField,permMap);
            niiOut.hdr.dime.dim(2:5) = thisSize(permMap);
            save_nii(niiOut,['nii/' filename(1:strfind(filename,'.mat')) loadFields{f} '.nii']);
        elseif nnz(ismember(thisSize,mapDims)) == 3 %if there at least three matching dimensions
            newDims(ismember(mapDims,thisSize)) = mapDims(ismember(mapDims,thisSize));
            newDims(newDims == 0) = mapDims(~ismember(mapDims,thisSize));
            [i a] = sort(thisSize);
            [i b] = sort(mapDims);
            permMap = b(a);
            newDims(~ismember(mapDims,thisSize)) = thisSize(~ismember(thisSize,mapDims));
            niiOut.hdr.dime.dim(2:5) = newDims;
            niiOut.img = permute(thisField,permMap);
            save_nii(niiOut,['nii/' filename(1:strfind(filename,'.mat')) loadFields{f} '.nii']);
        elseif nnz(ismember(thisSize,mapDims)) == 1 && thisSize(~ismember(thisSize,mapDims)) == prod(mapDims(~ismember(mapDims,thisSize)))
        % or if there is one matching dimension, and the others are a
        % product, then unflatten the image
            newDims(ismember(thisSize,mapDims)) = thisSize(ismember(thisSize,mapDims));
            newDims(newDims == 0) = mapDims(~ismember(mapDims,thisSize));
            niiOut.img = reshape(thisField,newDims);
            [i a] = sort(newDims);
            [i b] = sort(mapDims);
            permMap = b(a);
            niiOut.img = permute(niiOut.img,permMap);
            niiOut.hdr.dime.dim(2:5) = newDims(permMap);
            save_nii(niiOut,['nii/' filename(1:strfind(filename,'.mat')) loadFields{f} '.nii']);
        elseif length(thisSize) == 2 && nnz(thisSize(thisSize == max(thisSize)) == prod(combnk(mapDims,3)')) == 1;
            mapCombo = combnk(mapDims,3);
            newDims(find(thisSize == max(thisSize)):find(thisSize == max(thisSize))+2) = mapCombo(thisSize(thisSize == max(thisSize)) == prod(combnk(mapDims,3)')',:);
            newDims(thisSize ~= max(thisSize)) = thisSize(thisSize ~= max(thisSize));
            niiOut.img = reshape(thisField,newDims);
            newDims(~ismember(newDims,mapDims)) = mapDims(~ismember(mapDims,newDims));
            [i a] = sort(newDims);
            [i b] = sort(mapDims);
            permMap = b(a);
            newDims = newDims(permMap);
            newDims(4) = thisSize(thisSize ~= max(thisSize));
            niiOut.img = permute(niiOut.img,permMap);
            niiOut.hdr.dime.dim(2:5) = newDims;
            save_nii(niiOut,['nii/' filename(1:strfind(filename,'.mat')) loadFields{f} '.nii']);
        end
        
    end
    
end