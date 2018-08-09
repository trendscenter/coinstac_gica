function varargout = brad_fill_mask(msk,sizes,varargin)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%	brad_fill_mask - given a masked dataset, fills the masked areas with 0s
% 						  for display purposes
%
%	usage
%		>> sources = brad_fill_mask(mask,sizes,sources{:});
%			where sources is a cell containing datasets, mask is a dataset mask, 
%			and sizes is a cell containing desired sizes for the corresponding output datasets
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%% arg processing %%%%
    srcs = varargin;
    mask = msk;
    %
    disp(srcs)
    %%%% refill the space %%%%
    o_src = cell(1,length(srcs));
    for i = 1:length(srcs)
        o_src{i} = zeros(size(srcs{i},2),sizes(i));
        o_src{i}(:,mask==1) = srcs{i}';
    end
    %
    varargout = o_src;

end
