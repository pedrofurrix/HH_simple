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
 
#define nrn_init _nrn_init__Fzap
#define _nrn_initial _nrn_initial__Fzap
#define nrn_cur _nrn_cur__Fzap
#define _nrn_current _nrn_current__Fzap
#define nrn_jacob _nrn_jacob__Fzap
#define nrn_state _nrn_state__Fzap
#define _net_receive _net_receive__Fzap 
 
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
#define dur _ml->template fpfield<1>(_iml)
#define dur_columnindex 1
#define f0 _ml->template fpfield<2>(_iml)
#define f0_columnindex 2
#define f1 _ml->template fpfield<3>(_iml)
#define f1_columnindex 3
#define amp _ml->template fpfield<4>(_iml)
#define amp_columnindex 4
#define f _ml->template fpfield<5>(_iml)
#define f_columnindex 5
#define on _ml->template fpfield<6>(_iml)
#define on_columnindex 6
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
 {0, 0}
};
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"ton", "ms"},
 {"dur", "ms"},
 {"f0", "1/s"},
 {"f1", "1/s"},
 {"amp", "1"},
 {"f", "1/s"},
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
 static void _ba1(Node*_nd, Datum* _ppd, Datum* _thread, NrnThread* _nt, Memb_list* _ml, size_t _iml, _nrn_model_sorted_token const&);
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
"Fzap",
 "ton",
 "dur",
 "f0",
 "f1",
 "amp",
 0,
 "f",
 0,
 0,
 "x",
 0};
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0, /* ton */
     0, /* dur */
     0, /* f0 */
     0, /* f1 */
     0, /* amp */
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
 	dur = _parm_default[1]; /* 0 */
 	f0 = _parm_default[2]; /* 0 */
 	f1 = _parm_default[3]; /* 0 */
 	amp = _parm_default[4]; /* 0 */
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

 extern "C" void _fzap_reg() {
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
                                       _nrn_mechanism_field<double>{"dur"} /* 1 */,
                                       _nrn_mechanism_field<double>{"f0"} /* 2 */,
                                       _nrn_mechanism_field<double>{"f1"} /* 3 */,
                                       _nrn_mechanism_field<double>{"amp"} /* 4 */,
                                       _nrn_mechanism_field<double>{"f"} /* 5 */,
                                       _nrn_mechanism_field<double>{"on"} /* 6 */,
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
 	hoc_reg_ba(_mechtype, _ba1, 11);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 Fzap C\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double PI = 0x1.921fb54442d18p+1;
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
 if ( on  == 0.0 ) {
     f = 0.0 ;
     x = 0.0 ;
     }
   else {
     f = f0 + ( f1 - f0 ) * ( t - ton ) / dur ;
     x = amp * sin ( 2.0 * PI * ( t - ton ) * ( f0 + ( f1 - f0 ) * ( t - ton ) / ( 2.0 * dur ) ) * ( 0.001 ) ) ;
     }
   }
 
static void _net_receive (Point_process* _pnt, double* _args, double _lflag) 
{   neuron::legacy::set_globals_from_prop(_pnt->_prop, _ml_real, _ml, _iml);
    _ppvar = _nrn_mechanism_access_dparam(_pnt->_prop);
  if (_tsav > t){ hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t;   if (_lflag == 1. ) {*(_tqitem) = nullptr;}
 {
   if ( _lflag  == 1.0 ) {
     if ( on  == 0.0 ) {
       on = 1.0 ;
       net_send ( _tqitem, _args, _pnt, t +  dur , 1.0 ) ;
       }
     else {
       on = 0.0 ;
       }
     }
   } }

static void initmodel() {
  int _i; double _save;_ninits++;
{
 {
   f = 0.0 ;
   x = 0.0 ;
   on = 0.0 ;
   if ( ton < 0.0 ) {
     ton = 0.0 ;
     }
   if ( dur < 0.0 ) {
     dur = 0.0 ;
     }
   if ( f0 <= 0.0 ) {
     f0 = 0.0 ;
     }
   if ( f1 <= 0.0 ) {
     f1 = 0.0 ;
     }
   if ( dur > 0.0 ) {
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
  ": $Id: fzap.mod,v 1.5 2015/05/28 02:51:15 ted Exp ted $\n"
  "\n"
  "COMMENT\n"
  "fzap.mod\n"
  "\n"
  "A bogus point process that contains the variable x, \n"
  "which oscillates starting at t = del >= 0.\n"
  "The frequency f of the oscillation increases linearly with time\n"
  "from f0 at t == del to f1 at t == del + dur, \n"
  "where both del and dur are > 0.\n"
  "\n"
  "fzap uses the event delivery system to ensure compatibility with adaptive integration.\n"
  "\n"
  "=================\n"
  "NOTES AND CAVEATS\n"
  "=================\n"
  "\n"
  "1.  If x were a RANGE variable, an assignment statement would \n"
  "have to be inserted into proc advance() in order for the \n"
  "value of x to be used by other mechanisms--e.g.\n"
  "proc advance() {\n"
  "  is_xtra = Fzap[0].x\n"
  "  fadvance()\n"
  "}\n"
  "However, that would be incompatible with adaptive integration.\n"
  "To eliminate the need for such an assignment statement, x is a \n"
  "POINTER.  This preserves compatibility with adaptive integration.\n"
  "\n"
  "2.  On every fadvance, the statements that evaluate Fzap's x \n"
  "should be executed before the statements in any client mechanism \n"
  "that relies on the value of Fzap's x.  To that end, the value of \n"
  "x is computed in a BEFORE BREAKPOINT block, which will take care\n"
  "of any client mechanism that uses Fzap's x in a BREAKPOINT block.\n"
  "\n"
  "However, some client mechanisms may have their own \n"
  "BEFORE BREAKPOINT blocks that need the value of Fzap's x.  \n"
  "xtra is such a mechanism.  In this situation, care is required \n"
  "to ensure that the statements in Fzap's BEFORE BREAKPOINT block\n"
  "are executed first.  This can be done by compiling the mod file \n"
  "that defines Fzap _before_ the client mechanism's mod file.\n"
  "\n"
  "There are two ways to make this happen:\n"
  "A.  Invoke nrnivmodl with a command line that presents the file \n"
  "names in the desired sequence.  UNIX/Linux users may be quite \n"
  "comfortable with this.\n"
  "B.  Choose mod file names so that Fzap's mod file appears before \n"
  "the name of any client mod files in an alphabetical listing.\n"
  "For the example of Fzap and xtra, the file names fzap.mod and \n"
  "xtra.mod would be quite suitable.  This is more convenient for \n"
  "users of all operating systems, but especially MSWin and OS X, \n"
  "whose users are accustomed to compiling all mod files in a \n"
  "directory with mknrndll or \"drag and drop,\" respectively.\n"
  "\n"
  "12/11/2008 NTC\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "  POINT_PROCESS Fzap\n"
  "  RANGE ton, dur, f0, f1, amp, f\n"
  "  POINTER x\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "  PI = (pi) (1)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "  ton (ms)\n"
  "  dur (ms)\n"
  "  f0 (1/s)  : frequency is in Hz\n"
  "  f1 (1/s)\n"
  "  amp (1)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "  f (1/s)\n"
  "  x (1)\n"
  "  on (1)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "  f = 0\n"
  "  x = 0\n"
  "  on = 0\n"
  "\n"
  "  if (ton<0) { ton=0 }\n"
  "  if (dur<0) { dur=0 }\n"
  "  if (f0<=0) { f0=0 (1/s) }\n"
  "  if (f1<=0) { f1=0 (1/s) }\n"
  "\n"
  "  : do nothing if dur == 0\n"
  "  if (dur>0) {\n"
  "    net_send(ton, 1)  : to turn it on and start frequency ramp\n"
  "  }\n"
  "}\n"
  "\n"
  "COMMENT\n"
  "The angular velocity in radians/sec is w = 2*PI*f, \n"
  "where f is the instantaneous frequency in Hz.\n"
  "\n"
  "Assume for the moment that the frequency ramp starts at t = 0.\n"
  "f = f0 + (f1 - f0)*t/dur\n"
  "\n"
  "Then the angular displacement is\n"
  "theta = 2*PI * ( f0*t + (f1 - f0)*(t^2)/(2*dur) ) \n"
  "      = 2*PI * t * (f0 + (f1 - f0)*t/(2*dur))\n"
  "But the ramp starts at t = del, so just substitute t-del for every occurrence of t\n"
  "in the formula for theta.\n"
  "ENDCOMMENT\n"
  "\n"
  "BEFORE BREAKPOINT {\n"
  "  if (on==0) {\n"
  "    f = 0\n"
  "    x = 0\n"
  "  } else {\n"
  "    f = f0 + (f1 - f0)*(t-ton)/dur\n"
  "    x = amp * sin( 2*PI * (t-ton) * (f0 + (f1 - f0)*(t-ton)/(2*dur)) * (0.001) )\n"
  "  }\n"
  "}\n"
  "\n"
  "NET_RECEIVE (w) {\n"
  "  : respond only to self-events with flag > 0\n"
  "  if (flag == 1) {\n"
  "    if (on==0) {\n"
  "      on = 1  : turn it on\n"
  "      net_send(dur, 1)  : to stop frequency ramp, freezing frequency at f1\n"
  "    } else {\n"
  "      on = 0  : turn it off\n"
  "    }\n"
  "  }\n"
  "}\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
