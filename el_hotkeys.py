import pymel.core as pm
import pymel.core.datatypes as dt
import random
from el_anim_utilities import anim_util as anim

# Maya Hotkey Collection
# --------------------------------------------------------------------------------------#
# set a key at the midpoint between two selected keys
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.keyframe_midpoint()
"""


def keyframe_midpoint():
    """sets a key halfway between selected keys"""

    curves = pm.keyframe(q=True, selected=True, name=True)

    if len(curves) > 0:
        for curve in curves:
            key_times = pm.keyframe(curve, q=True, tc=True, sl=True)
            if len(key_times) > 1:
                start = key_times[0]
                end = key_times[-1]
                halfway = int(abs(end - start) * .5)

                pm.setKeyframe(curve, e=True, insert=True, time=start + halfway)
            else:
                pm.warning('[divisor.py] Need at least 2 keys selected on curve {}'.format(curve))
    else:
        pm.warning('[divisor.py ]No curves selected')


# --------------------------------------------------------------------------------------#
# select out tangents of selected keys
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.select_out_tangents()
"""


def select_out_tangents():
    """select out tangents of current selected keys"""
    curvelist = pm.keyframe(q=True, sl=True, name=True)

    for curve in curvelist:
        sel_keys = pm.keyframe(curve, q=True, sl=True)  # returns list of frames
        for i in range(len(sel_keys)):
            pm.selectKey(curve, time=(sel_keys[i],), outTangent=True, add=True)


"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.select_in_tangents()
"""


# select in tangents
def select_in_tangents():
    """select in tangents of current selected keys"""
    curvelist = pm.keyframe(q=True, sl=True, name=True)

    for curve in curvelist:
        sel_keys = pm.keyframe(curve, q=True, sl=True)  # returns list of frames
        for i in range(len(sel_keys)):
            pm.selectKey(curve, time=(sel_keys[i],), inTangent=True, add=True)


# --------------------------------------------------------------------------------------#
# prints the frame length and value range of key selection in the command line
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.get_selection_frame_value_length()
"""


def get_selection_frame_value_length():
    """Print the frame and value length of selected keys on a single curve"""
    import pymel.core as pm

    curve = pm.findKeyframe(c=True)

    if len(curve) == 1:  # only 1 curve selected
        l_keys = pm.keyframe(q=True, selected=True, tc=True)
        v_keys = pm.keyframe(q=True, selected=True, vc=True)

        if len(l_keys) > 1:  # at least 2 keys selected
            key_length = abs(l_keys[-1] - l_keys[0])  # frame length
            key_value = abs(max(v_keys) - min(v_keys))  # value range
            print ("frame length:  {}, value range:  {:.3f}".format(key_length, key_value)),
        else:
            pm.warning('Need to select at least 2 keys'),
    else:
        pm.warning('Select only 1 curve'),


# --------------------------------------------------------------------------------------#
# sets selected keys tangents to flat
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.make_flat_tangents()
"""


def make_flat_tangents():
    """sets selected keys tangents to flat"""
    pm.keyTangent(edit=True, itt='flat', ott='flat')


# --------------------------------------------------------------------------------------#
# sets selected keys tangents to spline
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.make_spline_tangents()
"""


def make_spline_tangents():
    """sets selected keys tangents to spline"""
    pm.keyTangent(edit=True, itt='spline', ott='spline')


# --------------------------------------------------------------------------------------#
# sharpen in tangent
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.sharpen_in_tangent()
"""


def sharpen_in_tangent():
    """sharpen in tangent (set tangent weight to .01)"""
    pm.keyTangent(edit=True, weightLock=False, lock=False, inWeight=.01)


"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.sharpen_out_tangent()
"""


# sharpen out tangent
def sharpen_out_tangent():
    """sharpen in tangent (set tangent weight to .01)"""
    pm.keyTangent(edit=True, weightLock=False, lock=False, outWeight=.01)


# --------------------------------------------------------------------------------------#
# toggle graph editor infinity display on/off
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.infinity_toggle()
"""


def infinity_toggle():
    """toggle graph editor infinity display on/off"""
    if pm.animCurveEditor('graphEditor1GraphEd', exists=True):
        ge = 'graphEditor1GraphEd'
        if pm.animCurveEditor(ge, q=True, displayInfinities=True):
            pm.animCurveEditor(ge, edit=True, displayInfinities='off')
        else:
            pm.animCurveEditor(ge, edit=True, displayInfinities='on')


# --------------------------------------------------------------------------------------#
# Various paste keys options

# paste keys insert at current frame
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.paste_keys_insert()
"""


def paste_keys_insert():
    """paste keys insert at current frame"""
    current_frame = pm.getCurrentTime()
    pm.pasteKey(option='insert', connect=True, time=(current_frame,))


# paste keys replace completely
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.paste_keys_replace()
"""


def paste_keys_replace():
    """paste keys replace completely"""
    pm.pasteKey(option='replaceCompletely')


# paste keys replace connect (replace but at the starting value of the pasted over curve)
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.paste_keys_connect()
"""


def paste_keys_connect():
    """paste keys replace connect (replace but at the starting value of the pasted over curve)"""
    pm.pasteKey(option='replace', connect=True)


# paste keys merge at current frame
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.paste_keys_merge()
"""


def paste_keys_merge():
    """paste keys merge at current frame"""
    current_frame = pm.getCurrentTime()
    pm.pasteKey(option='merge', time=(current_frame,))


# --------------------------------------------------------------------------------------#
# Show only polygons
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.show_only_polygons()
"""


def show_only_polygons():
    """Show only polygons"""
    active_view = pm.getPanel(withFocus=True)
    pm.modelEditor(active_view, edit=True, allObjects=False)
    pm.modelEditor(active_view, edit=True, polymeshes=True)


# --------------------------------------------------------------------------------------#
# Toggle nurbs curves on/off
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.toggle_nurbs_curves()
"""


def toggle_nurbs_curves():
    """Toggle nurbs curves on/off"""
    active_view = pm.getPanel(withFocus=True)
    if pm.modelEditor(active_view, q=True, nurbsCurves=True):
        pm.modelEditor(active_view, edit=True, nurbsCurves=False)
    else:
        pm.modelEditor(active_view, edit=True, nurbsCurves=True)


# --------------------------------------------------------------------------------------#
# Hotkey to swap two selected animation curves
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.swap_two_curves()
"""


def swap_two_curves():
    """Hotkey to swap two selected animation curves"""
    curves = pm.keyframe(q=True, selected=True, name=True)

    if len(curves) == 2:
        swap_a, swap_b = curves[0], curves[1]

        pm.copyKey(swap_a)

        # snapshot of swap_b before copying over
        pm.bufferCurve(swap_b, overwrite=True)

        pm.pasteKey(swap_b, option='replaceCompletely')

        # swap temporarily to previous buffer curve on swap_b
        pm.bufferCurve(swap_b, swap=True)
        pm.copyKey(swap_b)

        # swap back
        pm.bufferCurve(swap_b, swap=True)
        pm.pasteKey(swap_a, option='replaceCompletely')
    else:
        pm.warning('[swap_curves] Select 2 curves.')


# --------------------------------------------------------------------------------------#
# Apply euler filter
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.apply_euler_filter()
"""


def apply_euler_filter():
    """Apply euler filter"""
    pm.filterCurve()


# --------------------------------------------------------------------------------------#
# Shift curves forwards or backwards by defined frame
# Change number after amount= to define how many frames, use -1 etc to shift backwards
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.shift_curves(amount=1) 
"""


def shift_curves(amount=1):
    """Shift curves forwards or backwards by defined frame (amount)"""
    curves = pm.findKeyframe(curve=True)

    if len(curves) > 0:
        for curve in curves:
            pm.keyframe(curve, edit=True, relative=True, timeChange=amount)


# --------------------------------------------------------------------------------------#
# Measure the distance between two objects in 3D space
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.get_distance_between_two_objects()
"""


def get_distance_between_two_objects():
    """use rotation pivot to get the position since frozen transforms will affect where the object is """

    sel = pm.ls(sl=True)

    if len(sel) == 2:
        position1 = pm.xform(sel[0], query=True, worldSpace=True, rotatePivot=True)
        position2 = pm.xform(sel[1], query=True, worldSpace=True, rotatePivot=True)
        v1, v2 = dt.Vector(position1), dt.Vector(position2)

        print('Distance between {} and {}:   {}'.format(sel[0], sel[1], dt.Vector(abs(v1 - v2)).length())),
    else:
        pm.warning('[get_distance] Select 2 objects.'),


# --------------------------------------------------------------------------------------#
# Delete all keys before, after, or both, except the current one which has an insert key set
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.key_delete()
"""

# Command for only before:
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.key_delete(all_keys=False, only_before=True)
"""

# Command for only after: 
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.key_delete(all_keys=False, only_before=False)
"""


def key_delete(all_keys=True, only_before=False):
    """Delete all keys before, after, or both, except the current one which has an insert key set"""
    current_frame = pm.getCurrentTime()
    curves = pm.findKeyframe(curve=True)

    first_key = 0.0
    last_key = 0.0

    for curve in curves:
        key = pm.findKeyframe(curve, which='first')
        if key < first_key:
            first_key = key
        key = pm.findKeyframe(curve, which='last')
        if key > last_key:
            last_key = key

    pm.setKeyframe(insert=True)
    if not all_keys:
        if only_before:
            pm.cutKey(clear=True, time=(first_key, current_frame - 1))
        else:
            pm.cutKey(clear=True, time=(current_frame + 1, last_key))
    else:
        pm.cutKey(clear=True, time=(first_key, current_frame - 1))
        pm.cutKey(clear=True, time=(current_frame + 1, last_key))


# --------------------------------------------------------------------------------------#
# Set a keyframe one frame past the current timerange
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.key_one_past_range()
"""


def key_one_past_range():
    """Set a keyframe one frame past the current timerange"""
    cycle_start = pm.playbackOptions(query=True, minTime=True)
    cycle_end = pm.playbackOptions(query=True, maxTime=True) + 1.0
    pm.setKeyframe(time=[cycle_start, cycle_end])


# --------------------------------------------------------------------------------------#
# set playback range start to current frame
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.range_start_at_current()
"""


def range_start_at_current():
    """set playback range start to current frame"""
    current_frame = pm.currentTime(q=True)
    pm.playbackOptions(min=current_frame)


# --------------------------------------------------------------------------------------#
# set playback range end to current frame
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.range_end_at_current()
"""


def range_end_at_current():
    """set playback range end to current frame"""
    current_frame = pm.currentTime(q=True)
    pm.playbackOptions(min=current_frame)


# --------------------------------------------------------------------------------------#
# set playback range start to range minimum value
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.range_start_at_min()
"""


def range_start_at_min():
    """set playback range start to range minimum value"""
    range_start = pm.playbackOptions(q=True, animationStartTime=True)
    pm.playbackOptions(min=range_start)


# --------------------------------------------------------------------------------------#
# set playback range end to range maximum value
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.range_start_at_max()
"""


def range_start_at_max():
    """set playback range end to range maximum value"""
    range_start = pm.playbackOptions(q=True, animationEndTime=True)
    pm.playbackOptions(max=range_start)


# --------------------------------------------------------------------------------------#
# set playback range end to range maximum value
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.set_start_to_current_frame()
"""


def set_start_to_current_frame():
    """set playback range start to the current frame"""
    current_frame = pm.currentTime(q=True)
    pm.playbackOptions(min=current_frame)


# --------------------------------------------------------------------------------------#
# set playback range end to range maximum value
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.set_end_to_current_frame()
"""


def set_end_to_current_frame():
    """set playback range end to the current frame"""
    current_frame = pm.currentTime(q=True)
    pm.playbackOptions(max=current_frame)


# --------------------------------------------------------------------------------------#
# flip between start/end frames to compare cycle start/end poses
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.flip_between_start_end()
"""


def flip_between_start_end():
    """flip between start/end frames to compare cycle start/end poses"""
    range_start = pm.playbackOptions(q=True, min=True)
    range_end = pm.playbackOptions(q=True, max=True)
    current_frame = pm.currentTime(q=True)

    if current_frame != range_end or current_frame != range_start:
        pm.currentTime(range_start, e=True)
    if current_frame == range_start:
        pm.currentTime(range_end, e=True)


# --------------------------------------------------------------------------------------#
# mute/unmute translateZ channel on selected control (for run cycles to save having to select)
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.mute_tz_toggle()
"""


def mute_tz_toggle():
    """mute/unmute translateZ channel on selected control (for run cycles to save having to select)"""
    def get_main_ctrl():
        namespaces = pm.namespaceInfo(lon=True)
        name = ''
        for ns in namespaces:
            if len(ns) == 2 and ns != 'UI':
                name = ns
        return name + ':Main'

    main_ctrl = get_main_ctrl()

    try:
        if pm.mute('%s.translateZ' % main_ctrl, query=True):
            pm.mute('%s.translateZ' % main_ctrl, disable=True)
        else:
            pm.mute('%s.translateZ' % main_ctrl)
    except IndexError:
        pm.warning('Nothing selected to mute.'),

"""
def mute_tz_toggle():
    mutist = pm.ls(sl=True)

    try:
        if pm.mute('%s.translateZ' % mutist[0], query=True):
            pm.mute('%s.translateZ' % mutist[0], disable=True)
        else:
            pm.mute('%s.translateZ' % mutist[0])
    except IndexError:
        pm.warning('Nothing selected to mute.'),
"""

# --------------------------------------------------------------------------------------#
# mute/unmute selected channel box channels on all selected controls
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.mute_toggle()
"""


def mute_toggle():
    """mute/unmute selected channel box channels on all selected controls"""
    selection = pm.ls(sl=True)
    channels = pm.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)

    for sel in selection:
        for channel in channels:
            if pm.mute('{}.{}'.format(sel.name(), channel), query=True):
                pm.mute('{}.{}'.format(sel.name(), channel), disable=True)
            else:
                pm.mute('{}.{}'.format(sel.name(), channel))


# --------------------------------------------------------------------------------------#
# nudge selected key values by randomized amounts within the defined range
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.nudge_keys(nudge_amt=0.07, default_val_range=1.0, force_default_val_range=False)
"""


def nudge_keys(nudge_amt=0.07, default_val_range=1.0, force_default_val_range=False):
    """nudge selected key values by randomized amounts within the defined range"""
    curves = pm.keyframe(q=True, sl=True, name=True)

    for curve in curves:
        key_vals = pm.keyframe(curve, q=True, sl=True, vc=True)
        key_times = pm.keyframe(curve, q=True, sl=True, tc=True)

        if not force_default_val_range:
            val_range = abs(max(key_vals) - min(key_vals))

            if val_range < 1:
                val_range = default_val_range
        else:
            val_range = default_val_range

        for t, v in zip(key_times, key_vals):
            val = random.uniform(val_range * .01, val_range * nudge_amt)
            pm.keyframe(curve, e=True, vc=val * random.choice([-1, 1]), r=True, time=(t,))


# --------------------------------------------------------------------------------------#
# Swaps the values of 2 selected keys per curve
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.swap_keys()
"""


def swap_keys():
    """Swaps the values of 2 selected keys per curve"""
    curves = pm.keyframe(q=True, sl=True, name=True)

    if len(curves) > 0:
        keys = {}

        for curve in curves:
            key_times = pm.keyframe(curve, q=True, sl=True, tc=True)

            if len(key_times) == 2:
                keys[curve] = key_times
            else:
                pm.warning('[swap_keys] Select only 2 keys per curve to swap on {}'.format(curve))

        for k, v in keys.iteritems():
            value_a = pm.keyframe(k, q=True, time=(v[0],), vc=True)[0]
            value_b = pm.keyframe(k, q=True, time=(v[1],), vc=True)[0]

            for key, new_val in zip(v, (value_b, value_a)):
                pm.keyframe(k, edit=True, time=(key,), vc=new_val)
    else:
        pm.warning('[swap_keys] Select at least 2 keys on 1 animation curve')


# --------------------------------------------------------------------------------------#
# Select all controls in the current active animation layer
"""
import el_hotkeys
reload(el_hotkeys)
el_hotkeys.select_ctrls_in_selected_animlayer()
"""


def select_ctrls_in_selected_animlayer():
    """Select all controls in the current active animation layer"""
    current_anim_layers = pm.treeView(anim_layer_editor, q=True, si=True)
    pm.mel.layerEditorSelectObjectAnimLayer(current_anim_layers)