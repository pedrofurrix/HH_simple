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
static constexpr auto number_of_floating_point_variables = 8;
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
 
#define nrn_init _nrn_init__Fsquare
#define _nrn_initial _nrn_initial__Fsquare
#define nrn_cur _nrn_cur__Fsquare
#define _nrn_current _nrn_current__Fsquare
#define nrn_jacob _nrn_jacob__Fsquare
#define nrn_state _nrn_state__Fsquare
#define _net_receive _net_receive__Fsquare 
 
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
#define ton _ml->template fpfield<0>(_iml)
#define ton_columnindex 0
#define dp _ml->template fpfield<1>(_iml)
#define dp_columnindex 1
#define num _ml->template fpfield<2>(_iml)
#define num_columnindex 2
#define amp1 _ml->template fpfield<3>(_iml)
#define amp1_columnindex 3
#define amp2 _ml->template fpfield<4>(_iml)
#define amp2_columnindex 4
#define on _ml->template fpfield<5>(_iml)
#define on_columnindex 5
#define tally _ml->template fpfield<6>(_iml)
#define tally_columnindex 6
#define _tsav _ml->template fpfield<7>(_iml)
#define _tsav_columnindex 7
#define _nd_area *_ml->dptr_field<0>(_iml)
#define x	*_ppvar[2].get<double*>()
#define _p_x _ppvar[2].literal_value<void*>()
 static _nrn_mechanism_cache_instance _ml_real{nullptr};
static _nrn_mechanism_cache_range *_ml{&_ml_real};
static size_t _iml{0};
static Datum *_ppvar;
 static int hoc_nrnpointerindex =  2;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_nonneg(void*);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mechtype);
#endif
 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(Object* _ho) { void* create_point_process(int, Object*);
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt(void*);
 static double _hoc_loc_pnt(void* _vptr) {double loc_point_process(int, void*);
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(void* _vptr) {double has_loc_point(void*);
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(void* _vptr) {
 double get_loc_point_process(void*); return (get_loc_point_process(_vptr));
}
 static void _hoc_setdata(void*);
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 {0, 0}
};
 static Member_func _member_func[] = {
 {"loc", _hoc_loc_pnt},
 {"has_loc", _hoc_has_loc},
 {"get_loc", _hoc_get_loc_pnt},
 {"nonneg", _hoc_nonneg},
 {0, 0}
};
#define nonneg nonneg_Fsquare
 extern double nonneg( double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {"dp", 0, 1e+09},
 {"ton", 0, 1e+09},
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"ton", "ms"},
 {"dp", "ms"},
 {"num", "1"},
 {"amp1", "1"},
 {"amp2", "1"},
 {"x", "1"},
 {0, 0}
};
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {0, 0}
};
 static DoubVec hoc_vdoub[] = {
 {0, 0, 0}
};
 static double _sav_indep;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
_ppvar = _nrn_mechanism_access_dparam(_prop);
 Node * _node = _nrn_mechanism_access_node(_prop);
v = _nrn_mechanism_access_voltage(_node);
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 static void nrn_alloc(Prop*);
static void nrn_init(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_state(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 static void _hoc_destroy_pnt(void* _vptr) {
   destroy_point_process(_vptr);
}
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"Fsquare",
 "ton",
 "dp",
 "num",
 "amp1",
 "amp2",
 0,
 0,
 0,
 "x",
 0};
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0, /* ton */
     0, /* dp */
     0, /* num */
     0, /* amp1 */
     0, /* amp2 */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
  if (nrn_point_prop_) {
    _nrn_mechanism_access_alloc_seq(_prop) = _nrn_mechanism_access_alloc_seq(nrn_point_prop_);
    _ppvar = _nrn_mechanism_access_dparam(nrn_point_prop_);
  } else {
   _ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 8);
 	/*initialize range parameters*/
 	ton = _parm_default[0]; /* 0 */
 	dp = _parm_default[1]; /* 0 */
 	num = _parm_default[2]; /* 0 */
 	amp1 = _parm_default[3]; /* 0 */
 	amp2 = _parm_default[4]; /* 0 */
  }
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 8);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
 
#define _tqitem &(_ppvar[3])
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _fsquare_reg() {
	int _vectorized = 0;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nullptr, nullptr, nullptr, nrn_init,
	 hoc_nrnpointerindex, 0,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"ton"} /* 0 */,
                                       _nrn_mechanism_field<double>{"dp"} /* 1 */,
                                       _nrn_mechanism_field<double>{"num"} /* 2 */,
                                       _nrn_mechanism_field<double>{"amp1"} /* 3 */,
                                       _nrn_mechanism_field<double>{"amp2"} /* 4 */,
                                       _nrn_mechanism_field<double>{"on"} /* 5 */,
                                       _nrn_mechanism_field<double>{"tally"} /* 6 */,
                                       _nrn_mechanism_field<double>{"_tsav"} /* 7 */,
                                       _nrn_mechanism_field<double*>{"_nd_area", "area"} /* 0 */,
                                       _nrn_mechanism_field<Point_process*>{"_pntproc", "pntproc"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"x", "pointer"} /* 2 */,
                                       _nrn_mechanism_field<void*>{"_tqitem", "netsend"} /* 3 */);
  hoc_register_prop_size(_mechtype, 8, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "pointer");
  hoc_register_dparam_semantics(_mechtype, 3, "netsend");
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 Fsquare C\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static const char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
double nonneg (  double _lx ) {
   double _lnonneg;
 _lnonneg = _lx ;
   if ( _lx < 0.0 ) {
     _lnonneg = 0.0 ;
     }
   else {
     _lnonneg = _lx ;
     }
   
return _lnonneg;
 }
 
static double _hoc_nonneg(void* _vptr) {
 double _r;
    auto* const _pnt = static_cast<Point_process*>(_vptr);
  auto* const _p = _pnt->_prop;
  if (!_p) {
    hoc_execerror("POINT_PROCESS data instance not valid", NULL);
  }
   _setdata(_p);
 _r =  nonneg (  *getarg(1) );
 return(_r);
}
 
static void _net_receive (Point_process* _pnt, double* _args, double _lflag) 
{   neuron::legacy::set_globals_from_prop(_pnt->_prop, _ml_real, _ml, _iml);
    _ppvar = _nrn_mechanism_access_dparam(_pnt->_prop);
  if (_tsav > t){ hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t;   if (_lflag == 1. ) {*(_tqitem) = nullptr;}
 {
   if ( tally > 0.0 ) {
     if ( _lflag  == 1.0 ) {
       if ( on  == 0.0 ) {
         on = 1.0 ;
         }
       x = amp1 ;
       net_send ( _tqitem, _args, _pnt, t +  dp , 2.0 ) ;
       }
     if ( _lflag  == 2.0 ) {
       x = amp2 ;
       tally = tally - 1.0 ;
       if ( tally > 0.0 ) {
         net_send ( _tqitem, _args, _pnt, t +  dp , 1.0 ) ;
         }
       else {
         net_send ( _tqitem, _args, _pnt, t +  dp , 3.0 ) ;
         }
       }
     }
   if ( _lflag  == 3.0 ) {
     on = 0.0 ;
     x = 0.0 ;
     }
   } }

static void initmodel() {
  int _i; double _save;_ninits++;
{
 {
   on = 0.0 ;
   x = 0.0 ;
   ton = nonneg ( _threadargscomma_ ton ) ;
   dp = nonneg ( _threadargscomma_ dp ) ;
   num = nonneg ( _threadargscomma_ num ) ;
   if ( num * dp > 0.0 ) {
     tally = num ;
     net_send ( _tqitem, nullptr, _ppvar[1].get<Point_process*>(), t +  ton , 1.0 ) ;
     }
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
 _tsav = -1e20;
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
  "COMMENT\n"
  "square.mod\n"
  "Generates a square wave.\n"
  "User specifies\n"
  "ton  time at which first cycle starts\n"
  "dp   duration of a phase (duration of a half cycle)\n"
  "num  number of cycles\n"
  "amp1 level for first half cycle\n"
  "amp2 level for second half cycle\n"
  ": bal  nonzero forces amp2 = -amp1\n"
  "20150417 NTC\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "  POINT_PROCESS Fsquare\n"
  ":  RANGE ton, dp, num, amp1, amp2, bal\n"
  "  RANGE ton, dp, num, amp1, amp2\n"
  "  POINTER x\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "  ton = 0 (ms) <0, 1e9> : time at which first cycle starts\n"
  "  dp = 0 (ms) <0, 1e9> : phase duration (half cycle duration)\n"
  "  num = 0 (1) : how many cycles\n"
  "  amp1 = 0 (1) : level for first half cycle\n"
  "  amp2 = 0 (1) : level for second half cycle\n"
  ":  bal = 0 (1) : nonzero forces amp2 = -amp1\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "  x (1)\n"
  "  on (1)\n"
  "  tally (1) : how many more cycles are to be generated\n"
  "}\n"
  "\n"
  "UNITSOFF\n"
  "FUNCTION nonneg(x) {\n"
  "  nonneg = x\n"
  "  if (x<0) {\n"
  "    nonneg = 0\n"
  "  } else {\n"
  "    nonneg = x\n"
  "  }\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "  on = 0\n"
  "  x = 0\n"
  "  : force these to be nonnegative\n"
  "  ton = nonneg(ton)\n"
  "  dp = nonneg(dp)\n"
  "  num = nonneg(num)\n"
  "\n"
  "  : do nothing if num == 0 or dp == 0\n"
  "  if (num*dp>0) {\n"
  "    tally = num\n"
  "    net_send(ton,1) : to start first phase\n"
  "  }\n"
  "\n"
  ":  if (bal!=0) {\n"
  ":    amp2 = -amp1\n"
  ":  }\n"
  "}\n"
  "UNITSON\n"
  "\n"
  "NET_RECEIVE (w) {\n"
  "  : respond only to self-events\n"
  "  if (tally>0) { : generate output until all cycles have been completed\n"
  "    if (flag == 1) { : start a new cycle\n"
  "      if (on == 0) {\n"
  "        on = 1 : signal that it's \"on\"\n"
  "      }\n"
  "      x = amp1 : enter phase 1\n"
  "      : prepare for phase 2\n"
  "      net_send(dp, 2)\n"
  "    }\n"
  "    if (flag == 2) {\n"
  "      x = amp2 : enter phase 2\n"
  "      tally = tally - 1\n"
  "      if (tally>0) {\n"
  "        net_send(dp, 1) : prepare for next cycle\n"
  "      } else {\n"
  "        net_send(dp, 3) : end of waveform\n"
  "      }\n"
  "    }\n"
  "  }\n"
  "  if (flag == 3) { : no more cycles to generate\n"
  "    on = 0 : signal that it's \"off\"\n"
  "    x = 0\n"
  "  }\n"
  "}\n"
  "\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
