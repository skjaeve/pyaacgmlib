/* function prototypes */
%include cpointer.i



%include "astalg.h"
%include "genmag.h"
%include "igrflib.h"
%include "mlt_v2.h"
%include "time.h"
%include "aacgmlib_v2.h"

/* Create some functions for working with "int *" */
%pointer_functions(int, intp);
%pointer_functions(double, doublep);

%module aacgmlib_v2
%{

#include "astalg.h"
#include "genmag.h"
#include "igrflib.h"
#include "mlt_v2.h"
#include "time.h"
#include "aacgmlib_v2.h"

 %}

%include "astalg.h"
%include "genmag.h"
%include "igrflib.h"
%include "mlt_v2.h"
%include "time.h"
%include "aacgmlib_v2.h"