name overlap purpose this function determines the fraction of transmission function for each source that is overlapping with the sum of the transmission functions from all other sources category heao a 1 calling sequence result overlap trns inputs trns a 2 d array holding the transmission values for each bin of the scan and for each source fltarr nsrc nbin outputs the function returns a fltarr nsrc array giving the overlap fraction for each source procedure this function is used by the fiducial routine modification history written by han wen february 1995 function overlap trns sz size trns nsrc sz 1 nbin sz 2 if nsrc eq 1 then return 0.0 over fltarr nsrc for i 0 nsrc 1 do begin here where trns i gt 0 nbase if nbase eq 0 then over i 1 else begin here where indgen nsrc ne i trn_other reform total trns here 1 trn_mix reform trns i trn_other here where trn_mix ne 0 nmix over i float nmix nbase endelse endfor return over end