/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
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
static constexpr auto number_of_datum_variables = 3;
static constexpr auto number_of_floating_point_variables = 15;
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
 
#define nrn_init _nrn_init__ical
#define _nrn_initial _nrn_initial__ical
#define nrn_cur _nrn_cur__ical
#define _nrn_current _nrn_current__ical
#define nrn_jacob _nrn_jacob__ical
#define nrn_state _nrn_state__ical
#define _net_receive _net_receive__ical 
#define evaluate_fct evaluate_fct__ical 
#define states states__ical 
 
#define _threadargscomma_ _ml, _iml, _ppvar, _thread, _globals, _nt,
#define _threadargsprotocomma_ Memb_list* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt,
#define _internalthreadargsprotocomma_ _nrn_mechanism_cache_range* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt,
#define _threadargs_ _ml, _iml, _ppvar, _thread, _globals, _nt
#define _threadargsproto_ Memb_list* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt
#define _internalthreadargsproto_ _nrn_mechanism_cache_range* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *hoc_getarg(int);
 
#define t _nt->_t
#define dt _nt->_dt
#define gcabar _ml->template fpfield<0>(_iml)
#define gcabar_columnindex 0
#define carev _ml->template fpfield<1>(_iml)
#define carev_columnindex 1
#define alpha_m _ml->template fpfield<2>(_iml)
#define alpha_m_columnindex 2
#define beta_m _ml->template fpfield<3>(_iml)
#define beta_m_columnindex 3
#define alpha_h _ml->template fpfield<4>(_iml)
#define alpha_h_columnindex 4
#define beta_h _ml->template fpfield<5>(_iml)
#define beta_h_columnindex 5
#define m _ml->template fpfield<6>(_iml)
#define m_columnindex 6
#define h _ml->template fpfield<7>(_iml)
#define h_columnindex 7
#define eca _ml->template fpfield<8>(_iml)
#define eca_columnindex 8
#define Dm _ml->template fpfield<9>(_iml)
#define Dm_columnindex 9
#define Dh _ml->template fpfield<10>(_iml)
#define Dh_columnindex 10
#define ica _ml->template fpfield<11>(_iml)
#define ica_columnindex 11
#define tadj _ml->template fpfield<12>(_iml)
#define tadj_columnindex 12
#define v _ml->template fpfield<13>(_iml)
#define v_columnindex 13
#define _g _ml->template fpfield<14>(_iml)
#define _g_columnindex 14
#define _ion_eca *(_ml->dptr_field<0>(_iml))
#define _p_ion_eca static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_ica *(_ml->dptr_field<1>(_iml))
#define _p_ion_ica static_cast<neuron::container::data_handle<double>>(_ppvar[1])
#define _ion_dicadv *(_ml->dptr_field<2>(_iml))
 /* Thread safe. No static _ml, _iml or _ppvar. */
 static int hoc_nrnpointerindex =  -1;
 static _nrn_mechanism_std_vector<Datum> _extcall_thread;
 static Prop* _extcall_prop;
 /* _prop_id kind of shadows _extcall_prop to allow validity checking. */
 static _nrn_non_owning_id_without_container _prop_id{};
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_evaluate_fct(void);
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
 {"setdata_ical", _hoc_setdata},
 {"evaluate_fct_ical", _hoc_evaluate_fct},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_evaluate_fct(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"evaluate_fct", _npy_evaluate_fct},
 {0, 0}
};
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
#define cao cao_ical
 double cao = 2;
#define cai cai_ical
 double cai = 0.00024;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"cai_ical", "mM"},
 {"cao_ical", "mM"},
 {"gcabar_ical", "mho/cm2"},
 {"carev_ical", "mV"},
 {"alpha_m_ical", "/ms"},
 {"beta_m_ical", "/ms"},
 {"alpha_h_ical", "/ms"},
 {"beta_h_ical", "/ms"},
 {0, 0}
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {"cai_ical", &cai_ical},
 {"cao_ical", &cao_ical},
 {0, 0}
};
 static DoubVec hoc_vdoub[] = {
 {0, 0, 0}
};
 static double _sav_indep;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 _prop_id = _nrn_get_prop_id(_prop);
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
 static void nrn_cur(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_jacob(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(Prop*, int, neuron::container::data_handle<double>*, neuron::container::data_handle<double>*, double*, int);
static void _ode_spec(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void _ode_matsol(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 
#define _cvode_ieq _ppvar[3].literal_value<int>()
 static void _ode_matsol_instance1(_internalthreadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"ical",
 "gcabar_ical",
 0,
 "carev_ical",
 "alpha_m_ical",
 "beta_m_ical",
 "alpha_h_ical",
 "beta_h_ical",
 0,
 "m_ical",
 "h_ical",
 0,
 0};
 static Symbol* _ca_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0.0001, /* gcabar */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 15);
 	/*initialize range parameters*/
 	gcabar = _parm_default[0]; /* 0.0001 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 15);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* eca */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ica */
 	_ppvar[2] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dicadv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 {0, 0}
};
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _IL_gutnick_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("ca", -10000.);
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
         hoc_register_npy_direct(_mechtype, npy_direct_func_proc);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"gcabar"} /* 0 */,
                                       _nrn_mechanism_field<double>{"carev"} /* 1 */,
                                       _nrn_mechanism_field<double>{"alpha_m"} /* 2 */,
                                       _nrn_mechanism_field<double>{"beta_m"} /* 3 */,
                                       _nrn_mechanism_field<double>{"alpha_h"} /* 4 */,
                                       _nrn_mechanism_field<double>{"beta_h"} /* 5 */,
                                       _nrn_mechanism_field<double>{"m"} /* 6 */,
                                       _nrn_mechanism_field<double>{"h"} /* 7 */,
                                       _nrn_mechanism_field<double>{"eca"} /* 8 */,
                                       _nrn_mechanism_field<double>{"Dm"} /* 9 */,
                                       _nrn_mechanism_field<double>{"Dh"} /* 10 */,
                                       _nrn_mechanism_field<double>{"ica"} /* 11 */,
                                       _nrn_mechanism_field<double>{"tadj"} /* 12 */,
                                       _nrn_mechanism_field<double>{"v"} /* 13 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 14 */,
                                       _nrn_mechanism_field<double*>{"_ion_eca", "ca_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_ica", "ca_ion"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"_ion_dicadv", "ca_ion"} /* 2 */,
                                       _nrn_mechanism_field<int>{"_cvode_ieq", "cvodeieq"} /* 3 */);
  hoc_register_prop_size(_mechtype, 15, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ical C\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 0x1.78e555060882cp+16;
 static double R = 0x1.0a1013e8990bep+3;
static int _reset;
static const char *modelname = "High threshold calcium current";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int evaluate_fct(_internalthreadargsprotocomma_ double);
 
static int _ode_spec1(_internalthreadargsproto_);
/*static int _ode_matsol1(_internalthreadargsproto_);*/
 static neuron::container::field_index _slist1[2], _dlist1[2];
 static int states(_internalthreadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (_internalthreadargsproto_) {int _reset = 0; {
   evaluate_fct ( _threadargscomma_ v ) ;
   Dm = alpha_m * ( 1.0 - m ) - beta_m * m ;
   Dh = alpha_h * ( 1.0 - h ) - beta_h * h ;
   }
 return _reset;
}
 static int _ode_matsol1 (_internalthreadargsproto_) {
 evaluate_fct ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( alpha_m )*( ( ( - 1.0 ) ) ) - ( beta_m )*( 1.0 ) )) ;
 Dh = Dh  / (1. - dt*( ( alpha_h )*( ( ( - 1.0 ) ) ) - ( beta_h )*( 1.0 ) )) ;
  return 0;
}
 /*END CVODE*/
 static int states (_internalthreadargsproto_) { {
   evaluate_fct ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( alpha_m )*( ( ( - 1.0 ) ) ) - ( beta_m )*( 1.0 ))))*(- ( ( alpha_m )*( ( 1.0 ) ) ) / ( ( alpha_m )*( ( ( - 1.0 ) ) ) - ( beta_m )*( 1.0 ) ) - m) ;
    h = h + (1. - exp(dt*(( alpha_h )*( ( ( - 1.0 ) ) ) - ( beta_h )*( 1.0 ))))*(- ( ( alpha_h )*( ( 1.0 ) ) ) / ( ( alpha_h )*( ( ( - 1.0 ) ) ) - ( beta_h )*( 1.0 ) ) - h) ;
   }
  return 0;
}
 
static int  evaluate_fct ( _internalthreadargsprotocomma_ double _lv ) {
   alpha_m = 0.055 * ( - 27.0 - _lv ) / ( exp ( ( - 27.0 - _lv ) / 3.8 ) - 1.0 ) ;
   beta_m = 0.94 * exp ( ( - 75.0 - _lv ) / 17.0 ) ;
   alpha_h = 0.000457 * exp ( ( - 13.0 - _lv ) / 50.0 ) ;
   beta_h = 0.0065 / ( exp ( ( - 15.0 - _lv ) / 28.0 ) + 1.0 ) ;
    return 0; }
 
static void _hoc_evaluate_fct(void) {
  double _r;
 Datum* _ppvar; Datum* _thread; NrnThread* _nt;
 
  if(!_prop_id) {
    hoc_execerror("No data for evaluate_fct_ical. Requires prior call to setdata_ical and that the specified mechanism instance still be in existence.", NULL);
  }
  Prop* _local_prop = _extcall_prop;
  _nrn_mechanism_cache_instance _ml_real{_local_prop};
auto* const _ml = &_ml_real;
size_t const _iml{};
_ppvar = _local_prop ? _nrn_mechanism_access_dparam(_local_prop) : nullptr;
_thread = _extcall_thread.data();
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
_nt = nrn_threads;
 _r = 1.;
 evaluate_fct ( _threadargscomma_ *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_evaluate_fct(Prop* _prop) {
    double _r{0.0};
 Datum* _ppvar; Datum* _thread; NrnThread* _nt;
 _nrn_mechanism_cache_instance _ml_real{_prop};
auto* const _ml = &_ml_real;
size_t const _iml{};
_ppvar = _nrn_mechanism_access_dparam(_prop);
_thread = _extcall_thread.data();
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
_nt = nrn_threads;
 _r = 1.;
 evaluate_fct ( _threadargscomma_ *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
   Datum* _ppvar;
   size_t _iml;   _nrn_mechanism_cache_range* _ml;   Node* _nd{};
  double _v{};
  int _cntml;
  _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
  _ml = &_lmr;
  _cntml = _ml_arg->_nodecount;
  Datum *_thread{_ml_arg->_thread};
  double* _globals = nullptr;
  if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _ppvar = _ml_arg->_pdata[_iml];
    _nd = _ml_arg->_nodelist[_iml];
    v = NODEV(_nd);
  eca = _ion_eca;
     _ode_spec1 (_threadargs_);
  }}
 
static void _ode_map(Prop* _prop, int _ieq, neuron::container::data_handle<double>* _pv, neuron::container::data_handle<double>* _pvdot, double* _atol, int _type) { 
  Datum* _ppvar;
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _cvode_ieq = _ieq;
  for (int _i=0; _i < 2; ++_i) {
    _pv[_i] = _nrn_mechanism_get_param_handle(_prop, _slist1[_i]);
    _pvdot[_i] = _nrn_mechanism_get_param_handle(_prop, _dlist1[_i]);
    _cvode_abstol(_atollist, _atol, _i);
  }
 }
 
static void _ode_matsol_instance1(_internalthreadargsproto_) {
 _ode_matsol1 (_threadargs_);
 }
 
static void _ode_matsol(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
   Datum* _ppvar;
   size_t _iml;   _nrn_mechanism_cache_range* _ml;   Node* _nd{};
  double _v{};
  int _cntml;
  _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
  _ml = &_lmr;
  _cntml = _ml_arg->_nodecount;
  Datum *_thread{_ml_arg->_thread};
  double* _globals = nullptr;
  if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _ppvar = _ml_arg->_pdata[_iml];
    _nd = _ml_arg->_nodelist[_iml];
    v = NODEV(_nd);
  eca = _ion_eca;
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel(_internalthreadargsproto_) {
  int _i; double _save;{
  h = h0;
  m = m0;
 {
   evaluate_fct ( _threadargscomma_ v ) ;
   }
 
}
}

static void nrn_init(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
 v = _v;
  eca = _ion_eca;
 initmodel(_threadargs_);
 }
}

static double _nrn_current(_internalthreadargsprotocomma_ double _v) {
double _current=0.; v=_v;
{ {
   carev = ( 1e3 ) * ( R * ( celsius + 273.15 ) ) / ( 2.0 * FARADAY ) * log ( cao / cai ) ;
   ica = gcabar * m * m * h * ( v - carev ) ;
   }
 _current += ica;

} return _current;
}

static void nrn_cur(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_rhs = _nt->node_rhs_storage();
auto const _vec_sav_rhs = _nt->node_sav_rhs_storage();
auto const _vec_v = _nt->node_voltage_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
  eca = _ion_eca;
 auto const _g_local = _nrn_current(_threadargscomma_ _v + .001);
 	{ double _dica;
  _dica = ica;
 _rhs = _nrn_current(_threadargscomma_ _v);
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
  _ion_ica += ica ;
	 _vec_rhs[_ni[_iml]] -= _rhs;
 
}
 
}

static void nrn_jacob(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_d = _nt->node_d_storage();
auto const _vec_sav_d = _nt->node_sav_d_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (_iml = 0; _iml < _cntml; ++_iml) {
  _vec_d[_ni[_iml]] += _g;
 
}
 
}

static void nrn_state(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni;
_ni = _ml_arg->_nodeindices;
size_t _cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (size_t _iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
 _nd = _ml_arg->_nodelist[_iml];
   _v = _vec_v[_ni[_iml]];
 v=_v;
{
  eca = _ion_eca;
 {   states(_threadargs_);
  } }}

}

static void terminal(){}

static void _initlists(){
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = {m_columnindex, 0};  _dlist1[0] = {Dm_columnindex, 0};
 _slist1[1] = {h_columnindex, 0};  _dlist1[1] = {Dh_columnindex, 0};
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "C";
    const char* nmodl_file_text = 
  "TITLE High threshold calcium current\n"
  "\n"
  "COMMENT\n"
  "-----------------------------------------------------------------------------\n"
  "	High threshold calcium current\n"
  "	------------------------------\n"
  "\n"
  "   - Ca++ current, L type channels\n"
  "   - Differential equations\n"
  "\n"
  "   - Model from:\n"
  "\n"
  "   Reuveni I; Friedman A; Amitai Y; Gutnick MJ.\n"
  "     Stepwise repolarization from Ca2+ plateaus in neocortical pyramidal cells:\n"
  "     evidence for nonhomogeneous distribution of HVA Ca2+ channels in\n"
  "     dendrites.\n"
  "   Journal of Neuroscience, 1993 Nov, 13(11):4609-21.\n"
  "\n"
  "   - Experimental data for voltage-dependent activation:\n"
  "\n"
  "   Sayer RJ; Schwindt PC; Crill WE.\n"
  "     High- and low-threshold calcium currents in neurons acutely isolated from\n"
  "     rat sensorimotor cortex.\n"
  "   Neuroscience Letters, 1990 Dec 11, 120(2):175-8.\n"
  " \n"
  "   - Experimental data for voltage-dependent inactivation:\n"
  "\n"
  "   Dichter MA; Zona C.\n"
  "     Calcium currents in cultured rat cortical neurons.\n"
  "   Brain Research, 1989 Jul 17, 492(1-2):219-29.\n"
  "\n"
  "   - Calcium-dependent inactivation was not modeled; if interested, see:\n"
  "\n"
  "   Kay AR.\n"
  "     Inactivation kinetics of calcium current of acutely dissociated CA1\n"
  "     pyramidal cells of the mature guinea-pig hippocampus.\n"
  "   Journal of Physiology, 1991 Jun, 437:27-48.\n"
  "\n"
  "   - m2h kinetics from:\n"
  "\n"
  "   Kay AR; Wong RK.\n"
  "     Calcium current activation kinetics in isolated pyramidal neurones of the\n"
  "     Ca1 region of the mature guinea-pig hippocampus.\n"
  "   Journal of Physiology, 1987 Nov, 392:603-16.\n"
  "\n"
  "   - Reversal potential described by Nernst equation\n"
  "   - no temperature dependence included (rates correspond to 36 degC)\n"
  "\n"
  "\n"
  "   Alain Destexhe, Laval University, 1996\n"
  "\n"
  "-----------------------------------------------------------------------------\n"
  "ENDCOMMENT\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX ical\n"
  "	USEION ca READ eca WRITE ica\n"
  "        RANGE gcabar, alpha_m, beta_m, alpha_h, beta_h, m, h, carev\n"
  "}\n"
  "\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "	(molar) = (1/liter)\n"
  "	(mM) = (millimolar)\n"
  "	FARADAY = (faraday) (coulomb)\n"
  "	R = (k-mole) (joule/degC)\n"
  "}\n"
  "\n"
  "\n"
  "PARAMETER {\n"
  "	v		(mV)\n"
  "	celsius	= 36	(degC)\n"
  "	eca		(mV)\n"
  "	cai 	= .00024 (mM)		: initial [Ca]i = 200 nM\n"
  "	cao 	= 2	(mM)		: [Ca]o = 2 mM\n"
  "	gcabar	= 1e-4	(mho/cm2)	: Max conductance\n"
  "}\n"
  "\n"
  "\n"
  "STATE {\n"
  "	m\n"
  "	h\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ica	(mA/cm2)		: current\n"
  "	carev	(mV)			: rev potential\n"
  "	alpha_m	(/ms)			: rate cst\n"
  "	beta_m	(/ms)\n"
  "	alpha_h	(/ms)\n"
  "	beta_h	(/ms)\n"
  "	tadj\n"
  "}\n"
  "\n"
  "\n"
  "BREAKPOINT { \n"
  "	SOLVE states METHOD cnexp : see http://www.neuron.yale.edu/phpBB/viewtopic.php?f=28&t=592\n"
  "	carev = (1e3) * (R*(celsius+273.15))/(2*FARADAY) * log (cao/cai)\n"
  "	ica = gcabar * m * m * h * (v-carev)\n"
  "}\n"
  "\n"
  "DERIVATIVE states { \n"
  "	evaluate_fct(v)\n"
  "\n"
  "	m' = alpha_m * (1-m) - beta_m * m\n"
  "	h' = alpha_h * (1-h) - beta_h * h\n"
  "}\n"
  "\n"
  "\n"
  "UNITSOFF\n"
  "\n"
  "INITIAL {\n"
  "	evaluate_fct(v)\n"
  ":	m = alpha_m / (alpha_m + beta_m)\n"
  ":	h = alpha_h / (alpha_h + beta_h)\n"
  ":	tadj = 3 ^ ((celsius-36)/10)\n"
  "}\n"
  "\n"
  "PROCEDURE evaluate_fct(v(mV)) {\n"
  "\n"
  "	: rates at 36 degC\n"
  "\n"
  "	alpha_m = 0.055 * (-27-v) / (exp((-27-v)/3.8) - 1)\n"
  "	beta_m = 0.94 * exp((-75-v)/17)\n"
  "\n"
  "	alpha_h = 0.000457 * exp((-13-v)/50)\n"
  "	beta_h = 0.0065 / (exp((-15-v)/28) + 1)\n"
  "}\n"
  "\n"
  "UNITSON\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
