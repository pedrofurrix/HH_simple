#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern "C" void _beforesteppy_reg();
extern "C" void _cadecay_destexhe_reg();
extern "C" void _fsquare_reg();
extern "C" void _fzap_reg();
extern "C" void _HH_traub_reg();
extern "C" void _IL_gutnick_reg();
extern "C" void _IM_cortex_reg();
extern "C" void _IT_huguenard_reg();
extern "C" void _xtra_reg();

extern "C" void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," beforesteppy.mod");
fprintf(stderr," cadecay_destexhe.mod");
fprintf(stderr," fsquare.mod");
fprintf(stderr," fzap.mod");
fprintf(stderr," HH_traub.mod");
fprintf(stderr," IL_gutnick.mod");
fprintf(stderr," IM_cortex.mod");
fprintf(stderr," IT_huguenard.mod");
fprintf(stderr," xtra.mod");
fprintf(stderr, "\n");
    }
_beforesteppy_reg();
_cadecay_destexhe_reg();
_fsquare_reg();
_fzap_reg();
_HH_traub_reg();
_IL_gutnick_reg();
_IM_cortex_reg();
_IT_huguenard_reg();
_xtra_reg();
}
