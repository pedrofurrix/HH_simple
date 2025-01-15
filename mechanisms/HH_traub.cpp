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
static constexpr auto number_of_datum_variables = 6;
static constexpr auto number_of_floating_point_variables = 25;
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
 
#define nrn_init _nrn_init__hh2
#define _nrn_initial _nrn_initial__hh2
#define nrn_cur _nrn_cur__hh2
#define _nrn_current _nrn_current__hh2
#define nrn_jacob _nrn_jacob__hh2
#define nrn_state _nrn_state__hh2
#define _net_receive _net_receive__hh2 
#define evaluate_fct evaluate_fct__hh2 
#define states states__hh2 
 
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
#define gnabar _ml->template fpfield<0>(_iml)
#define gnabar_columnindex 0
#define gkbar _ml->template fpfield<1>(_iml)
#define gkbar_columnindex 1
#define vtraub _ml->template fpfield<2>(_iml)
#define vtraub_columnindex 2
#define m_inf _ml->template fpfield<3>(_iml)
#define m_inf_columnindex 3
#define h_inf _ml->template fpfield<4>(_iml)
#define h_inf_columnindex 4
#define n_inf _ml->template fpfield<5>(_iml)
#define n_inf_columnindex 5
#define tau_m _ml->template fpfield<6>(_iml)
#define tau_m_columnindex 6
#define tau_h _ml->template fpfield<7>(_iml)
#define tau_h_columnindex 7
#define tau_n _ml->template fpfield<8>(_iml)
#define tau_n_columnindex 8
#define m_exp _ml->template fpfield<9>(_iml)
#define m_exp_columnindex 9
#define h_exp _ml->template fpfield<10>(_iml)
#define h_exp_columnindex 10
#define n_exp _ml->template fpfield<11>(_iml)
#define n_exp_columnindex 11
#define m _ml->template fpfield<12>(_iml)
#define m_columnindex 12
#define h _ml->template fpfield<13>(_iml)
#define h_columnindex 13
#define n _ml->template fpfield<14>(_iml)
#define n_columnindex 14
#define ena _ml->template fpfield<15>(_iml)
#define ena_columnindex 15
#define ek _ml->template fpfield<16>(_iml)
#define ek_columnindex 16
#define Dm _ml->template fpfield<17>(_iml)
#define Dm_columnindex 17
#define Dh _ml->template fpfield<18>(_iml)
#define Dh_columnindex 18
#define Dn _ml->template fpfield<19>(_iml)
#define Dn_columnindex 19
#define ina _ml->template fpfield<20>(_iml)
#define ina_columnindex 20
#define ik _ml->template fpfield<21>(_iml)
#define ik_columnindex 21
#define il _ml->template fpfield<22>(_iml)
#define il_columnindex 22
#define tadj _ml->template fpfield<23>(_iml)
#define tadj_columnindex 23
#define _g _ml->template fpfield<24>(_iml)
#define _g_columnindex 24
#define _ion_ena *(_ml->dptr_field<0>(_iml))
#define _p_ion_ena static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_ina *(_ml->dptr_field<1>(_iml))
#define _p_ion_ina static_cast<neuron::container::data_handle<double>>(_ppvar[1])
#define _ion_dinadv *(_ml->dptr_field<2>(_iml))
#define _ion_ek *(_ml->dptr_field<3>(_iml))
#define _p_ion_ek static_cast<neuron::container::data_handle<double>>(_ppvar[3])
#define _ion_ik *(_ml->dptr_field<4>(_iml))
#define _p_ion_ik static_cast<neuron::container::data_handle<double>>(_ppvar[4])
#define _ion_dikdv *(_ml->dptr_field<5>(_iml))
 static _nrn_mechanism_cache_instance _ml_real{nullptr};
static _nrn_mechanism_cache_range *_ml{&_ml_real};
static size_t _iml{0};
static Datum *_ppvar;
 static int hoc_nrnpointerindex =  -1;
 static Prop* _extcall_prop;
 /* _prop_id kind of shadows _extcall_prop to allow validity checking. */
 static _nrn_non_owning_id_without_container _prop_id{};
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_Exp(void);
 static void _hoc_evaluate_fct(void);
 static void _hoc_states(void);
 static void _hoc_vtrap(void);
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
 {"setdata_hh2", _hoc_setdata},
 {"Exp_hh2", _hoc_Exp},
 {"evaluate_fct_hh2", _hoc_evaluate_fct},
 {"states_hh2", _hoc_states},
 {"vtrap_hh2", _hoc_vtrap},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_Exp(Prop*);
 static double _npy_evaluate_fct(Prop*);
 static double _npy_states(Prop*);
 static double _npy_vtrap(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"Exp", _npy_Exp},
 {"evaluate_fct", _npy_evaluate_fct},
 {"states", _npy_states},
 {"vtrap", _npy_vtrap},
 {0, 0}
};
#define Exp Exp_hh2
#define vtrap vtrap_hh2
 extern double Exp( double );
 extern double vtrap( double , double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"gnabar_hh2", "mho/cm2"},
 {"gkbar_hh2", "mho/cm2"},
 {"vtraub_hh2", "mV"},
 {0, 0}
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double n0 = 0;
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
 static void nrn_cur(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_jacob(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 
static int _ode_count(int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"hh2",
 "gnabar_hh2",
 "gkbar_hh2",
 "vtraub_hh2",
 0,
 "m_inf_hh2",
 "h_inf_hh2",
 "n_inf_hh2",
 "tau_m_hh2",
 "tau_h_hh2",
 "tau_n_hh2",
 "m_exp_hh2",
 "h_exp_hh2",
 "n_exp_hh2",
 0,
 "m_hh2",
 "h_hh2",
 "n_hh2",
 0,
 0};
 static Symbol* _na_sym;
 static Symbol* _k_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0.003, /* gnabar */
     0.005, /* gkbar */
     -63, /* vtraub */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 6, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 25);
 	/*initialize range parameters*/
 	gnabar = _parm_default[0]; /* 0.003 */
 	gkbar = _parm_default[1]; /* 0.005 */
 	vtraub = _parm_default[2]; /* -63 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 25);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* ena */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ina */
 	_ppvar[2] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dinadv */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* ek */
 	_ppvar[4] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ik */
 	_ppvar[5] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dikdv */
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _HH_traub_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
         hoc_register_npy_direct(_mechtype, npy_direct_func_proc);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"gnabar"} /* 0 */,
                                       _nrn_mechanism_field<double>{"gkbar"} /* 1 */,
                                       _nrn_mechanism_field<double>{"vtraub"} /* 2 */,
                                       _nrn_mechanism_field<double>{"m_inf"} /* 3 */,
                                       _nrn_mechanism_field<double>{"h_inf"} /* 4 */,
                                       _nrn_mechanism_field<double>{"n_inf"} /* 5 */,
                                       _nrn_mechanism_field<double>{"tau_m"} /* 6 */,
                                       _nrn_mechanism_field<double>{"tau_h"} /* 7 */,
                                       _nrn_mechanism_field<double>{"tau_n"} /* 8 */,
                                       _nrn_mechanism_field<double>{"m_exp"} /* 9 */,
                                       _nrn_mechanism_field<double>{"h_exp"} /* 10 */,
                                       _nrn_mechanism_field<double>{"n_exp"} /* 11 */,
                                       _nrn_mechanism_field<double>{"m"} /* 12 */,
                                       _nrn_mechanism_field<double>{"h"} /* 13 */,
                                       _nrn_mechanism_field<double>{"n"} /* 14 */,
                                       _nrn_mechanism_field<double>{"ena"} /* 15 */,
                                       _nrn_mechanism_field<double>{"ek"} /* 16 */,
                                       _nrn_mechanism_field<double>{"Dm"} /* 17 */,
                                       _nrn_mechanism_field<double>{"Dh"} /* 18 */,
                                       _nrn_mechanism_field<double>{"Dn"} /* 19 */,
                                       _nrn_mechanism_field<double>{"ina"} /* 20 */,
                                       _nrn_mechanism_field<double>{"ik"} /* 21 */,
                                       _nrn_mechanism_field<double>{"il"} /* 22 */,
                                       _nrn_mechanism_field<double>{"tadj"} /* 23 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 24 */,
                                       _nrn_mechanism_field<double*>{"_ion_ena", "na_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_ina", "na_ion"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"_ion_dinadv", "na_ion"} /* 2 */,
                                       _nrn_mechanism_field<double*>{"_ion_ek", "k_ion"} /* 3 */,
                                       _nrn_mechanism_field<double*>{"_ion_ik", "k_ion"} /* 4 */,
                                       _nrn_mechanism_field<double*>{"_ion_dikdv", "k_ion"} /* 5 */);
  hoc_register_prop_size(_mechtype, 25, 6);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 hh2 C\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static const char *modelname = "Hippocampal HH channels";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int evaluate_fct(double);
static int states();
 
static int  states (  ) {
   evaluate_fct ( _threadargscomma_ v ) ;
   m = m + m_exp * ( m_inf - m ) ;
   h = h + h_exp * ( h_inf - h ) ;
   n = n + n_exp * ( n_inf - n ) ;
   
/*VERBATIM*/
	return 0;
  return 0; }
 
static void _hoc_states(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for states_hh2. Requires prior call to setdata_hh2 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 states (  );
 hoc_retpushx(_r);
}
 
static double _npy_states(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 states (  );
 return(_r);
}
 
static int  evaluate_fct (  double _lv ) {
   double _la , _lb , _lv2 ;
 _lv2 = _lv - vtraub ;
   _la = 0.32 * vtrap ( _threadargscomma_ 13.0 - _lv2 , 4.0 ) ;
   _lb = 0.28 * vtrap ( _threadargscomma_ _lv2 - 40.0 , 5.0 ) ;
   tau_m = 1.0 / ( _la + _lb ) / tadj ;
   m_inf = _la / ( _la + _lb ) ;
   _la = 0.128 * Exp ( _threadargscomma_ ( 17.0 - _lv2 ) / 18.0 ) ;
   _lb = 4.0 / ( 1.0 + Exp ( _threadargscomma_ ( 40.0 - _lv2 ) / 5.0 ) ) ;
   tau_h = 1.0 / ( _la + _lb ) / tadj ;
   h_inf = _la / ( _la + _lb ) ;
   _la = 0.032 * vtrap ( _threadargscomma_ 15.0 - _lv2 , 5.0 ) ;
   _lb = 0.5 * Exp ( _threadargscomma_ ( 10.0 - _lv2 ) / 40.0 ) ;
   tau_n = 1.0 / ( _la + _lb ) / tadj ;
   n_inf = _la / ( _la + _lb ) ;
   m_exp = 1.0 - Exp ( _threadargscomma_ - dt / tau_m ) ;
   h_exp = 1.0 - Exp ( _threadargscomma_ - dt / tau_h ) ;
   n_exp = 1.0 - Exp ( _threadargscomma_ - dt / tau_n ) ;
    return 0; }
 
static void _hoc_evaluate_fct(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for evaluate_fct_hh2. Requires prior call to setdata_hh2 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 evaluate_fct (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_evaluate_fct(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 evaluate_fct (  *getarg(1) );
 return(_r);
}
 
double vtrap (  double _lx , double _ly ) {
   double _lvtrap;
 if ( fabs ( _lx / _ly ) < 1e-6 ) {
     _lvtrap = _ly * ( 1.0 - _lx / _ly / 2.0 ) ;
     }
   else {
     _lvtrap = _lx / ( Exp ( _threadargscomma_ _lx / _ly ) - 1.0 ) ;
     }
   
return _lvtrap;
 }
 
static void _hoc_vtrap(void) {
  double _r;
    _r =  vtrap (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_vtrap(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  vtrap (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
double Exp (  double _lx ) {
   double _lExp;
 if ( _lx < - 100.0 ) {
     _lExp = 0.0 ;
     }
   else {
     _lExp = exp ( _lx ) ;
     }
   
return _lExp;
 }
 
static void _hoc_Exp(void) {
  double _r;
    _r =  Exp (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_Exp(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  Exp (  *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("hh2", "cannot be used with CVODE"); return 0;}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
  n = n0;
 {
   m = 0.0 ;
   h = 0.0 ;
   n = 0.0 ;
   tadj = pow( 3.0 , ( ( celsius - 36.0 ) / 10.0 ) ) ;
   }
  _sav_indep = t; t = _save;

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
  ena = _ion_ena;
  ek = _ion_ek;
 initmodel();
  }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ina = gnabar * m * m * m * h * ( v - ena ) ;
   ik = gkbar * n * n * n * n * ( v - ek ) ;
   }
 _current += ina;
 _current += ik;

} return _current;
}

static void nrn_cur(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_rhs = _nt->node_rhs_storage();
auto const _vec_sav_rhs = _nt->node_sav_rhs_storage();
auto const _vec_v = _nt->node_voltage_storage();
Node *_nd; int* _ni; double _rhs, _v; int _cntml;
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
  ena = _ion_ena;
  ek = _ion_ek;
 auto const _g_local = _nrn_current(_v + .001);
 	{ double _dik;
 double _dina;
  _dina = ina;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
  _ion_ina += ina ;
  _ion_ik += ik ;
	 _vec_rhs[_ni[_iml]] -= _rhs;
 
}}

static void nrn_jacob(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_d = _nt->node_d_storage();
auto const _vec_sav_d = _nt->node_sav_d_storage();
auto* const _ml = &_lmr;
Node *_nd; int* _ni; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
  _vec_d[_ni[_iml]] += _g;
 
}}

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
  ena = _ion_ena;
  ek = _ion_ek;
 { error =  states();
 if(error){
  std_cerr_stream << "at line 68 in file HH_traub.mod:\n	SOLVE states\n";
  std_cerr_stream << _ml << ' ' << _iml << '\n';
  abort_run(error);
}
 }  }}

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
  "TITLE Hippocampal HH channels\n"
  ":\n"
  ": Fast Na+ and K+ currents responsible for action potentials\n"
  ": Iterative equations\n"
  ":\n"
  ": Equations modified by Traub, for Hippocampal Pyramidal cells, in:\n"
  ": Traub & Miles, Neuronal Networks of the Hippocampus, Cambridge, 1991\n"
  ":\n"
  ": range variable vtraub adjust threshold\n"
  ":\n"
  ": Written by Alain Destexhe, Salk Institute, Aug 1992\n"
  ":\n"
  ": Modified Oct 96 for compatibility with Windows: trap low values of arguments\n"
  ":\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX hh2\n"
  "	USEION na READ ena WRITE ina\n"
  "	USEION k READ ek WRITE ik\n"
  "	RANGE gnabar, gkbar, vtraub\n"
  "	RANGE m_inf, h_inf, n_inf\n"
  "	RANGE tau_m, tau_h, tau_n\n"
  "	RANGE m_exp, h_exp, n_exp\n"
  "}\n"
  "\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	gnabar  = .003  (mho/cm2)\n"
  "	gkbar   = .005  (mho/cm2)\n"
  "\n"
  "	ena     = 50    (mV)\n"
  "	ek      = -90   (mV)\n"
  "	celsius = 36    (degC)\n"
  "	dt              (ms)\n"
  "	v               (mV)\n"
  "	vtraub  = -63   (mV)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m h n\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ina     (mA/cm2)\n"
  "	ik      (mA/cm2)\n"
  "	il      (mA/cm2)\n"
  "	m_inf\n"
  "	h_inf\n"
  "	n_inf\n"
  "	tau_m\n"
  "	tau_h\n"
  "	tau_n\n"
  "	m_exp\n"
  "	h_exp\n"
  "	n_exp\n"
  "	tadj\n"
  "}\n"
  "\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states\n"
  "	ina = gnabar * m*m*m*h * (v - ena)\n"
  "	ik  = gkbar * n*n*n*n * (v - ek)\n"
  "}\n"
  "\n"
  "\n"
  ":DERIVATIVE states {   : exact Hodgkin-Huxley equations\n"
  ":       evaluate_fct(v)\n"
  ":       m' = (m_inf - m) / tau_m\n"
  ":       h' = (h_inf - h) / tau_h\n"
  ":       n' = (n_inf - n) / tau_n\n"
  ":}\n"
  "\n"
  "PROCEDURE states() {    : exact when v held constant\n"
  "	evaluate_fct(v)\n"
  "	m = m + m_exp * (m_inf - m)\n"
  "	h = h + h_exp * (h_inf - h)\n"
  "	n = n + n_exp * (n_inf - n)\n"
  "	VERBATIM\n"
  "	return 0;\n"
  "	ENDVERBATIM\n"
  "}\n"
  "\n"
  "UNITSOFF\n"
  "INITIAL {\n"
  "	m = 0\n"
  "	h = 0\n"
  "	n = 0\n"
  ":\n"
  ":  Q10 was assumed to be 3 for both currents\n"
  ":\n"
  ": original measurements at roomtemperature?\n"
  "\n"
  "	tadj = 3.0 ^ ((celsius-36)/ 10 )\n"
  "}\n"
  "\n"
  "PROCEDURE evaluate_fct(v(mV)) { LOCAL a,b,v2\n"
  "\n"
  "	v2 = v - vtraub : convert to traub convention\n"
  "\n"
  ":       a = 0.32 * (13-v2) / ( Exp((13-v2)/4) - 1)\n"
  "	a = 0.32 * vtrap(13-v2, 4)\n"
  ":       b = 0.28 * (v2-40) / ( Exp((v2-40)/5) - 1)\n"
  "	b = 0.28 * vtrap(v2-40, 5)\n"
  "	tau_m = 1 / (a + b) / tadj\n"
  "	m_inf = a / (a + b)\n"
  "\n"
  "	a = 0.128 * Exp((17-v2)/18)\n"
  "	b = 4 / ( 1 + Exp((40-v2)/5) )\n"
  "	tau_h = 1 / (a + b) / tadj\n"
  "	h_inf = a / (a + b)\n"
  "\n"
  ":       a = 0.032 * (15-v2) / ( Exp((15-v2)/5) - 1)\n"
  "	a = 0.032 * vtrap(15-v2, 5)\n"
  "	b = 0.5 * Exp((10-v2)/40)\n"
  "	tau_n = 1 / (a + b) / tadj\n"
  "	n_inf = a / (a + b)\n"
  "\n"
  "	m_exp = 1 - Exp(-dt/tau_m)\n"
  "	h_exp = 1 - Exp(-dt/tau_h)\n"
  "	n_exp = 1 - Exp(-dt/tau_n)\n"
  "}\n"
  "FUNCTION vtrap(x,y) {\n"
  "	if (fabs(x/y) < 1e-6) {\n"
  "		vtrap = y*(1 - x/y/2)\n"
  "	}else{\n"
  "		vtrap = x/(Exp(x/y)-1)\n"
  "	}\n"
  "}\n"
  "\n"
  "FUNCTION Exp(x) {\n"
  "	if (x < -100) {\n"
  "		Exp = 0\n"
  "	}else{\n"
  "		Exp = exp(x)\n"
  "	}\n"
  "} \n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
