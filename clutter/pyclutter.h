#ifndef __PY_CLUTTER_H__
#define __PY_CLUTTER_H__

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <glib.h>

#define NO_IMPORT_PYGOBJECT
#include <pygobject.h>
#include <Python.h>
#include <clutter/clutter.h>
#include <clutter/clutter-feature.h>

G_BEGIN_DECLS

typedef struct _PyClutterCallback       PyClutterCallback;

PyClutterCallback *pyclutter_callback_new    (PyObject          *function,
                                              PyObject          *data,
                                              gint               n_params,
                                              GType              param_types[]);
void               pyclutter_callback_free   (PyClutterCallback *cb);
PyObject *         pyclutter_callback_invoke (PyClutterCallback *cb,
                                              ...);

guint32   pyclutter_alpha_func              (ClutterAlpha    *alpha,
                                             gpointer         data);
void      pyclutter_effect_complete         (ClutterActor    *actor,
                                             gpointer         data);

gboolean  pyclutter_geometry_from_pyobject  (PyObject        *object,
                                             ClutterGeometry *geometry);
gboolean  pyclutter_color_from_pyobject     (PyObject        *object,
                                             ClutterColor    *color);
gboolean  pyclutter_actor_box_from_pyobject (PyObject        *object,
                                             ClutterActorBox *box);

G_END_DECLS

#endif /* __PY_CLUTTER_H__ */
