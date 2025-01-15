/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#define _pval pval
// clang-format off
#include "md1redef.h"
#include "section_fwd.hpp"
#include "nrniv_mf.h"
#include "md2redef.h"
#include "nrnconf.h"
// clang-format on
#include "neuron/cache/mechanism_range.hpp"
#include <vector>
using std::size_t;
static auto& std_cerr_stream = std::cerr;
static constexpr auto number_of_datum_variables = 3;
static constexpr auto number_of_floating_point_variables = 5;
namespace {
template <typename T>
using _nrn_mechanism_std_vector = std::vector<T>;
using _nrn_model_sorted_token = neuron::model_sorted_token;
using _nrn_mechanism_cache_range = neuron::cache::MechanismRange<number_of_floating_point_variables, number_of_datum_variables>;
using _nrn_mechanism_cache_instance = neuron::cache::MechanismInstance<number_of_floating_point_variables, number_of_datum_variables>;
using _nrn_non_owning_id_without_container = neuron::container::non_owning_identifier_without_container;
template <typename T>
using _nrn_mechanism_field = neuron::mechanism::field<T>;
template <typename... Args>
void _nrn_mechanism_register_data_fields(Args&&... args) {
  neuron::mechanism::register_data_fields(std::forward<Args>(args)...);
}
}
 
#if !NRNGPU
#undef exp
#define exp hoc_Exp
#if NRN_ENABLE_ARCH_INDEP_EXP_POW
#undef pow
#define pow hoc_pow
#endif
#endif
 
#define nrn_init _nrn_init__xtra
#define _nrn_initial _nrn_initial__xtra
#define nrn_cur _nrn_cur__xtra
#define _nrn_current _nrn_current__xtra
#define nrn_jacob _nrn_jacob__xtra
#define nrn_state _nrn_state__xtra
#define _net_receive _net_receive__xtra 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _internalthreadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
#define _internalthreadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *hoc_getarg(int);
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define rx _ml->template fpfield<0>(_iml)
#define rx_columnindex 0
#define x _ml->template fpfield<1>(_iml)
#define x_columnindex 1
#define y _ml->template fpfield<2>(_iml)
#define y_columnindex 2
#define z _ml->template fpfield<3>(_iml)
#define z_columnindex 3
#define er _ml->template fpfield<4>(_iml)
#define er_columnindex 4
#define im	*_ppvar[0].get<double*>()
#define _p_im _ppvar[0].literal_value<void*>()
#define ex	*_ppvar[1].get<double*>()
#define _p_ex _ppvar[1].literal_value<void*>()
#define area	(*(_ml->dptr_field<2>(_iml)))
 static _nrn_mechanism_cache_instance _ml_real{nullptr};
static _nrn_mechanism_cache_range *_ml{&_ml_real};
static size_t _iml{0};
static Datum *_ppvar;
 static int hoc_nrnpointerindex =  0;
 static Prop* _extcall_prop;
 /* _prop_id kind of shadows _extcall_prop to allow validity checking. */
 static _nrn_non_owning_id_without_container _prop_id{};
 /* external NEURON variables */
 /* declaration of user functions */
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mechtype);
#endif
 static void _hoc_setdata();
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 {"setdata_xtra", _hoc_setdata},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {0, 0}
};
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
#define is is_xtra
 double is = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"is_xtra", "milliamp"},
 {"rx_xtra", "megohm"},
 {"x_xtra", "1"},
 {"y_xtra", "1"},
 {"z_xtra", "1"},
 {"er_xtra", "microvolts"},
 {"im_xtra", "milliamp/cm2"},
 {"ex_xtra", "millivolts"},
 {0, 0}
};
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {"is_xtra", &is_xtra},
 {0, 0}
};
 static DoubVec hoc_vdoub[] = {
 {0, 0, 0}
};
 static double _sav_indep;
 static void _ba1(Node*_nd, Datum* _ppd, Datum* _thread, NrnThread* _nt, Memb_list* _ml, size_t _iml, _nrn_model_sorted_token const&);
 static void _ba2(Node*_nd, Datum* _ppd, Datum* _thread, NrnThread* _nt, Memb_list* _ml, size_t _iml, _nrn_model_sorted_token const&);
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 _prop_id = _nrn_get_prop_id(_prop);
 neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
_ppvar = _nrn_mechanism_access_dparam(_prop);
 Node * _node = _nrn_mechanism_access_node(_prop);
v = _nrn_mechanism_access_voltage(_node);
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 static void nrn_alloc(Prop*);
static void nrn_init(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_state(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"xtra",
 "rx_xtra",
 "x_xtra",
 "y_xtra",
 "z_xtra",
 0,
 "er_xtra",
 0,
 0,
 "im_xtra",
 "ex_xtra",
 0};
 extern Node* nrn_alloc_node_;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     1, /* rx */
     0, /* x */
     0, /* y */
     0, /* z */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 5);
 	/*initialize range parameters*/
 	rx = _parm_default[0]; /* 1 */
 	x = _parm_default[1]; /* 0 */
 	y = _parm_default[2]; /* 0 */
 	z = _parm_default[3]; /* 0 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 5);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 	_ppvar[2] = _nrn_mechanism_get_area_handle(nrn_alloc_node_);
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _xtra_reg() {
	int _vectorized = 0;
  _initlists();
 	register_mech(_mechanism, nrn_alloc,nullptr, nullptr, nullptr, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
         hoc_register_npy_direct(_mechtype, npy_direct_func_proc);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"rx"} /* 0 */,
                                       _nrn_mechanism_field<double>{"x"} /* 1 */,
                                       _nrn_mechanism_field<double>{"y"} /* 2 */,
                                       _nrn_mechanism_field<double>{"z"} /* 3 */,
                                       _nrn_mechanism_field<double>{"er"} /* 4 */,
                                       _nrn_mechanism_field<double*>{"im", "pointer"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"ex", "pointer"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"area", "area"} /* 2 */);
  hoc_register_prop_size(_mechtype, 5, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "pointer");
  hoc_register_dparam_semantics(_mechtype, 1, "pointer");
  hoc_register_dparam_semantics(_mechtype, 2, "area");
 	hoc_reg_ba(_mechtype, _ba1, 11);
 	hoc_reg_ba(_mechtype, _ba2, 22);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 xtra C\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static const char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 /* BEFORE BREAKPOINT */
 static void _ba1(Node*_nd, Datum* _ppd, Datum* _thread, NrnThread* _nt, Memb_list* _ml_arg, size_t _iml, _nrn_model_sorted_token const& _sorted_token)  {
    _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _ml_arg->_type()}; auto* const _ml = &_lmr;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
 _ppvar = _ppd;
  v = NODEV(_nd);
 ex = is * rx * ( 1e6 ) ;
   }
 /* AFTER SOLVE */
 static void _ba2(Node*_nd, Datum* _ppd, Datum* _thread, NrnThread* _nt, Memb_list* _ml_arg, size_t _iml, _nrn_model_sorted_token const& _sorted_token)  {
    _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _ml_arg->_type()}; auto* const _ml = &_lmr;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
 _ppvar = _ppd;
  v = NODEV(_nd);
 er = ( 10.0 ) * rx * im * area ;
   }

static void initmodel() {
  int _i; double _save;_ninits++;
{
 {
   ex = is * rx * ( 1e6 ) ;
   er = ( 10.0 ) * rx * im * area ;
   }

}
}

static void nrn_init(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
Node *_nd; double _v; int* _ni; int _cntml;
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
 v = _v;
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{
} return _current;
}

static void nrn_state(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _cntml;
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
 _nd = _ml_arg->_nodelist[_iml];
   _v = _vec_v[_ni[_iml]];
 v=_v;
{
}}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "C";
    const char* nmodl_file_text = 
  ": $Id: xtra.mod,v 1.4 2014/08/18 23:15:25 ted Exp ted $\n"
  "\n"
  "COMMENT\n"
  "This mechanism is intended to be used in conjunction \n"
  "with the extracellular mechanism.  Pointers specified \n"
  "at the hoc level must be used to connect the \n"
  "extracellular mechanism's e_extracellular and i_membrane \n"
  "to this mechanism's ex and im, respectively.\n"
  "\n"
  "xtra does three useful things:\n"
  "\n"
  "1. Serves as a target for Vector.play() to facilitate \n"
  "extracellular stimulation.  Assumes that one has initialized \n"
  "a Vector to hold the time sequence of the stimulus current.\n"
  "This Vector is to be played into the GLOBAL variable is \n"
  "(GLOBAL so only one Vector.play() needs to be executed), \n"
  "which is multiplied by the RANGE variable rx (\"transfer \n"
  "resistance between the stimulus electrode and the local \n"
  "node\").  This product, called ex in this mechanism, is the \n"
  "extracellular potential at the local node, i.e. is used to \n"
  "drive local e_extracellular.\n"
  "\n"
  "2. Reports the contribution of local i_membrane to the \n"
  "total signal that would be picked up by an extracellular \n"
  "recording electrode.  This is computed as the product of rx, \n"
  "i_membrane (called im in this mechanism), and the surface area \n"
  "of the local segment, and is reported as er.  The total \n"
  "extracellularly recorded potential is the sum of all er_xtra \n"
  "over all segments in all sections, and is to be computed at \n"
  "the hoc level, e.g. with code like\n"
  "\n"
  "func fieldrec() { local sum\n"
  "  sum = 0\n"
  "  forall {\n"
  "    if (ismembrane(\"xtra\")) {\n"
  "      for (x,0) sum += er_xtra(x)\n"
  "    }\n"
  "  }\n"
  "  return sum\n"
  "}\n"
  "\n"
  "Bipolar recording, i.e. recording the difference in potential \n"
  "between two extracellular electrodes, can be achieved with no \n"
  "change to either this NMODL code or fieldrec(); the values of \n"
  "rx will reflect the difference between the potentials at the \n"
  "recording electrodes caused by the local membrane current, so \n"
  "some rx will be negative and others positive.  The same rx \n"
  "can be used for bipolar stimulation.\n"
  "\n"
  "Multiple monopolar or bipolar extracellular recording and \n"
  "stimulation can be accommodated by changing this mod file to \n"
  "include additional rx, er, and is, and changing fieldrec() \n"
  "to a proc.\n"
  "\n"
  "3. Allows local storage of xyz coordinates interpolated from \n"
  "the pt3d data.  These coordinates are used by hoc code that \n"
  "computes the transfer resistance that couples the membrane \n"
  "to extracellular stimulating and recording electrodes.\n"
  "\n"
  "\n"
  "Prior to NEURON 5.5, the SOLVE statement in the BREAKPOINT block \n"
  "used METHOD cvode_t so that the adaptive integrators wouldn't miss \n"
  "the stimulus.  Otherwise, the BREAKPOINT block would have been called \n"
  "_after_ the integration step, rather than from within cvodes/ida, \n"
  "causing this mechanism to fail to deliver a stimulus current \n"
  "when the adaptive integrator is used.\n"
  "\n"
  "With NEURON 5.5 and later, this mechanism abandons the BREAKPOINT \n"
  "block and uses the two new blocks BEFORE BREAKPOINT and  \n"
  "AFTER SOLVE, like this--\n"
  "\n"
  "BEFORE BREAKPOINT { : before each cy' = f(y,t) setup\n"
  "  ex = is*rx*(1e6)\n"
  "}\n"
  "AFTER SOLVE { : after each solution step\n"
  "  er = (10)*rx*im*area\n"
  "}\n"
  "\n"
  "This ensures that the stimulus potential is computed prior to the \n"
  "solution step, and that the recorded potential is computed after.\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX xtra\n"
  "	RANGE rx, er\n"
  "	RANGE x, y, z\n"
  "	GLOBAL is\n"
  "	POINTER im, ex\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	: default transfer resistance between stim electrodes and axon\n"
  "	rx = 1 (megohm) : mV/nA\n"
  "	x = 0 (1) : spatial coords\n"
  "	y = 0 (1)\n"
  "	z = 0 (1)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v (millivolts)\n"
  "	is (milliamp)\n"
  "	ex (millivolts)\n"
  "	im (milliamp/cm2)\n"
  "	er (microvolts)\n"
  "	area (micron2)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	ex = is*rx*(1e6)\n"
  "	er = (10)*rx*im*area\n"
  ": this demonstrates that area is known\n"
  ": UNITSOFF\n"
  ": printf(\"area = %f\\n\", area)\n"
  ": UNITSON\n"
  "}\n"
  "\n"
  ": Use BREAKPOINT for NEURON 5.4 and earlier\n"
  ": BREAKPOINT {\n"
  ":	SOLVE f METHOD cvode_t\n"
  ": }\n"
  ":\n"
  ": PROCEDURE f() {\n"
  ":	: 1 mA * 1 megohm is 1000 volts\n"
  ":	: but ex is in mV\n"
  ":	ex = is*rx*(1e6)\n"
  ":	er = (10)*rx*im*area\n"
  ": }\n"
  "\n"
  ": With NEURON 5.5 and later, abandon the BREAKPOINT block and PROCEDURE f(),\n"
  ": and instead use BEFORE BREAKPOINT and AFTER SOLVE\n"
  "\n"
  "BEFORE BREAKPOINT { : before each cy' = f(y,t) setup\n"
  "  ex = is*rx*(1e6)\n"
  "}\n"
  "AFTER SOLVE { : after each solution step\n"
  "  er = (10)*rx*im*area\n"
  "}\n"
  "\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
