/**  Among-site rate variation calculation in C.  Does not use BEAGLE.
 */
#if ! defined(ASRV_H)
#define ASRV_H
#ifdef __cplusplus
extern "C" 
{
#endif




#include "pytbeaglehon_defs.h"


/**
 * stores an array of doubles and an array of frequencies representing the
 * a probability for each element in the array.
 * An example usage is for storing an array of rates for n_categories and the
 * probability that a site would belong to each of the rate categories.
 */
typedef struct {
	PyObject_HEAD
	unsigned n;
	int style; /* enum facet for to indicate type -- this is a hack
				  0 ="use median for rate categ"
				  1 ="use mean for rate categ"
			   */
	double param; /*shape param of the gamma distribution -- this is a hack*/
	double * rate;
	double * freq;
} ASRVObj;


/* `style` should be:
        0 for `categories of the gamma represented by their median`, or
        1 for `categories of the gamma represented by their mean`.
 */
ASRVObj* asrv_obj_new(unsigned dim, int style, double param);
void asrv_obj_dtor(ASRVObj* asrh);

/* sets the shape parameter of the gamma distribution and recalculates the 
    rates for the categories
*/
void internal_asrv_set_shape(ASRVObj *asrh, double val);





/* used internally in the library, not to be called by client code */
ASRVObj * private_asrv_obj_init(ASRVObj *, unsigned dim, int style, double param);




#ifdef __cplusplus
}
/* end of extern c bit */
#endif






#endif

/**
  pytbeaglehon phylogenetic likelihood caluclations using beaglelib.

  Copyright 2010 Mark T. Holder (except where noted). All rights reserved.

  See "LICENSE.txt" for terms and conditions of usage.
*/
