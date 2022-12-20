import libximc
import tempfile
import urllib
import re
import time
import matplotlib.pyplot as plt
from libximc import *
from ctypes import *

sbuf = create_string_buffer(64)
lib.ximc_version(sbuf)


open_name = b'xi-com:\\\\.\\COM6'

device_id = lib.open_device(open_name)

'''
# Automatic search and opening of the controller. If no real controllers are found, a virtual controller will be opened.

# Set bindy (network) keyfile. Must be called before any call to "enumerate_devices" or "open_device" if you
# wish to use network-attached controllers. Accepts both absolute and relative paths, relative paths are resolved
# relative to the process working directory. If you do not need network devices then "set_bindy_key" is optional.
# In Python make sure to pass byte-array object to this function (b"string literal").
# result = lib.set_bindy_key(os.path.join(ximc_dir, "win32", "keyfile.sqlite").encode("utf-8"))
result = lib.set_bindy_key("keyfile.sqlite".encode("utf-8")) # Search for the key file in the current directory.
if result != Result.Ok:
    print("keyfile not found")
    
# This is device search and enumeration with probing. It gives more information about devices.
probe_flags =EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
enum_hints = b"addr="
# enum_hints = b"addr=" # Use this hint string for broadcast enumerate
devenum = lib.enumerate_devices(probe_flags, enum_hints)
# print("Device enum handle: " + repr(devenum))
# print("Device enum handle type: " + repr(type(devenum)))

dev_count = lib.get_device_count(devenum)
print("Device count: " + repr(dev_count))

controller_name = controller_name_t()
for dev_ind in range(0, dev_count):
    enum_name = lib.get_device_name(devenum, dev_ind)
    result = lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))
    if result == Result.Ok:
        print("Enumerated device #{} name (port name): ".format(dev_ind) + repr(enum_name) + ". Friendly name: " + repr(controller_name.ControllerName) + ".")

flag_virtual = 0

open_name = None
if dev_count > 0:
    open_name = lib.get_device_name(devenum, 0)
elif sys.version_info >= (3,0):
    # use URI for virtual device when there is new urllib python3 API
    tempdir = tempfile.gettempdir() + "/testdevice.bin"
    if os.altsep:
        tempdir = tempdir.replace(os.sep, os.altsep)
    # urlparse build wrong path if scheme is not file
    uri = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme="file", \
            netloc=None, path=tempdir, params=None, query=None, fragment=None))
    open_name = re.sub(r'^file', 'xi-emu', uri).encode()
    flag_virtual = 1
    print("The real controller is not found or busy with another app.")
    print("The virtual controller is selected to check the operation of the library.")
    print("If you want to open a real controller, connect it or close the application that uses it.")

if not open_name:
    exit(1)

if type(open_name) is str:
    open_name = open_name.encode()
'''
'''
x_device_information = device_information_t()
result = lib.get_device_information(device_id, byref(x_device_information))
if result == Result.Ok:
    print("Device information:")
    print(" Manufacturer: " +
            repr(string_at(x_device_information.Manufacturer).decode()))
    print(" ManufacturerId: " +
            repr(string_at(x_device_information.ManufacturerId).decode()))
    print(" ProductDescription: " +
            repr(string_at(x_device_information.ProductDescription).decode()))
    print(" Major: " + repr(x_device_information.Major))
    print(" Minor: " + repr(x_device_information.Minor))
    print(" Release: " + repr(x_device_information.Release))
print("\nReading serial")
x_serial = c_uint()
result = lib.get_serial_number(device_id, byref(x_serial))
if result == Result.Ok:
    print("Serial: " + repr(x_serial.value))
    
print("\nReading firmware version")
x_Major = c_uint()
x_Minor = c_uint()
x_Release = c_uint()
result = lib.get_firmware_version (device_id, byref(x_Major), byref(x_Minor), byref(x_Release));
if result == Result.Ok:
    print("Major: " + repr(x_Major.value))
    print("Minor: " + repr(x_Minor.value))
    print("Release: " + repr(x_Release.value))
encoder_information = encoder_information_t()
result = lib.get_encoder_information(device_id, byref(encoder_information))
if result == Result.Ok:
    manufacturer = repr(string_at(encoder_information.Manufacturer).decode())
    print(f'Encoder manufacturer: {manufacturer}')
    partnumber = repr(string_at(encoder_information.PartNumber).decode())
    print(f'Encoder part number: {partnumber}')
'''

'''
BorderFlags.BORDER_IS_ENCODER = True #Borders are defined by encoder position
BorderFlags.BORDERS_SWAP_MISSET_DETECTION = True #Engine stops when reach both borders
edge = edges_settings_calb_t()
edge.LeftBorder = 0.1
edge.RightBorder = 12.725
result_edge = lib.set_edges_settings_calb(device_id, byref(edge), byref(user_unit))
'''
status = status_t()
result_status = lib.get_status(device_id, byref(status))

        
def test_get_position(lib, device_id, mode=1):
    """
    Obtaining information about the position of the positioner.
    
    This function allows you to get information about the current positioner coordinates,
    both in steps and in encoder counts, if it is set.
    Also, depending on the state of the mode parameter, information can be obtained in user units.
    
    :param lib: structure for accessing the functionality of the libximc library.
    :param device_id: device id.
    :param mode: mode in feedback counts or in user units. (Default value = 1)
    """
    moveStatus = status_MvCmdSts(lib, device_id)
    # print("\nRead position")
    if mode:
        x_pos = get_position_t()
        result = lib.get_position(device_id, byref(x_pos))
        if result == Result.Ok:
            print("Position: {0} steps, {1} microsteps // Move status {2}, Movr status {3}                 "
                  .format(x_pos.EncPosition, x_pos.uPosition, moveStatus[0], moveStatus[1]),  end="\r")
        return x_pos.Position, x_pos.uPosition
    else:
        x_pos = get_position_calb_t()
        result = lib.get_position_calb(device_id, byref(x_pos), byref(user_unit))
        if result == Result.Ok:
            print("Position: {0} user unit // Move status {1}, Movr status {2}                 "
                  .format(x_pos.Position, moveStatus[0], moveStatus[1]),  end="\r")
        return x_pos.Position, 0
    
def test_move(lib, device_id, distance, udistance, mode=1):
    """
    Move to the specified coordinate.
    Depending on the mode parameter, you can set coordinates in steps or feedback counts, or in custom units.
    
    :param lib: structure for accessing the functionality of the libximc library.
    :param device_id: device id.
    :param distance: the position of the destination.
    :param udistance: destination position in micro steps if this mode is used.
    :param mode:  mode in feedback counts or in user units. (Default value = 1)
    """
    
    if mode:
        print("\nGoing to {0} steps, {1} microsteps".format(distance, udistance))
        result = lib.command_move(device_id, distance, udistance)
    else:
        # udistance is not used for setting movement in custom units.
        print("\nMove to the position {0} specified in user units.".format(distance))
        result = lib.command_move_calb(device_id, c_float(distance), byref(user_unit))
        
def test_movr(lib, device_id, distance, udistance, mode=1):
    """
    The shift by the specified offset coordinates.
    
    Depending on the mode parameter, you can set coordinates in steps or feedback counts, or in custom units.
    
    :param lib: structure for accessing the functionality of the libximc library.
    :param device_id: device id.
    :param distance: size of the offset in steps.
    :param udistance: Size of the offset in micro steps.
    :param mode:  (Default value = 1)
    """
    
    if mode:
        print("\nShift to {0} steps, {1} microsteps".format(distance, udistance))
        result = lib.command_movr(device_id, distance, udistance)
    else:
        # udistance is not used for setting movement in custom units.
        print("\nShift to the position {0} specified in user units.".format(distance))
        result = lib.command_movr_calb(device_id, c_float(distance), byref(user_unit))

def get_status(lib, device_id):
    """
    A function of reading status information from the device
    You can use this function to get basic information about the device status.
    
    :param lib: structure for accessing the functionality of the libximc library.
    :param device_id:  device id.
    """
    
    x_status = status_t()
    result = lib.get_status(device_id, byref(x_status))
    if result == Result.Ok:
        return x_status
    else:
        return None
    
def status_MvCmdSts_MVCMD_RUNNING(lib, device_id):
    currStatus = get_status(lib, device_id)
    return (currStatus.MvCmdSts & MvcmdStatus.MVCMD_RUNNING) # 0x80) # )

def status_MvCmdSts(lib, device_id):
    currStatus = get_status(lib, device_id)
    """
    MVCMD_MOVE         = 0x01
    MVCMD_MOVR         = 0x02
    MVCMD_LEFT         = 0x03
    MVCMD_RIGHT        = 0x04
    MVCMD_STOP         = 0x05
    MVCMD_HOME         = 0x06
    MVCMD_LOFT         = 0x07
    MVCMD_SSTP         = 0x08
    MVCMD_ERROR        = 0x40
    MVCMD_RUNNING      = 0x80
    """
    return (currStatus.MvCmdSts & MvcmdStatus.MVCMD_MOVE), (currStatus.MvCmdSts & MvcmdStatus.MVCMD_MOVR), (currStatus.MvCmdSts & MvcmdStatus.MVCMD_LEFT),
    (currStatus.MvCmdSts & MvcmdStatus.MVCMD_RIGHT), (currStatus.MvCmdSts & MvcmdStatus.MVCMD_STOP), (currStatus.MvCmdSts & MvcmdStatus.MVCMD_HOME),
    (currStatus.MvCmdSts & MvcmdStatus.MVCMD_LOFT), (currStatus.MvCmdSts & MvcmdStatus.MVCMD_SSTP), (currStatus.MvCmdSts & MvcmdStatus.MVCMD_ERROR),
    (currStatus.MvCmdSts & MvcmdStatus.MVCMD_RUNNING)
    
def status_StateFlags(lib, device_id):
    currStatus = get_status(lib, device_id)
    """
    STATE_IS_HOMED                  = 0x0000020
    STATE_ALARM                     = 0x0000040
    STATE_CTP_ERROR                 = 0x0000080
    STATE_POWER_OVERHEAT            = 0x0000100
    STATE_CONTROLLER_OVERHEAT       = 0x0000200
    STATE_OVERLOAD_POWER_VOLTAGE    = 0x0000400
    STATE_OVERLOAD_POWER_CURRENT    = 0x0000800
    STATE_OVERLOAD_USB_VOLTAGE      = 0x0001000
    STATE_LOW_USB_VOLTAGE           = 0x0002000
    STATE_OVERLOAD_USB_CURRENT      = 0x0004000
    STATE_BORDERS_SWAP_MISSET       = 0x0008000
    STATE_LOW_POWER_VOLTAGE         = 0x0010000
    STATE_H_BRIDGE_FAULT            = 0x0020000
    STATE_WINDING_RES_MISMATCH      = 0x0100000
    STATE_ENCODER_FAULT             = 0x0200000
    STATE_ENGINE_RESPONSE_ERROR     = 0x0800000
    STATE_EXTIO_ALARM               = 0x1000000
    """
    
    print("")
    if (currStatus.Flags & StateFlags.STATE_IS_HOMED):
        print(" True:STATE_IS_HOMED ")
    else:
        print("False:STATE_IS_HOMED ")

    if (currStatus.Flags & StateFlags.STATE_ALARM):
        print(" True:STATE_ALARM")
    else:
        print("False:STATE_ALARM")
        
    if (currStatus.Flags & StateFlags.STATE_CTP_ERROR):
        print(" True:STATE_CTP_ERROR")
    else:
        print("False:STATE_CTP_ERROR")

    if (currStatus.Flags & StateFlags.STATE_POWER_OVERHEAT):
        print(" True:STATE_POWER_OVERHEAT")
    else:
        print("False:STATE_POWER_OVERHEAT")

    if (currStatus.Flags & StateFlags.STATE_OVERLOAD_POWER_VOLTAGE):
        print(" True:STATE_OVERLOAD_POWER_VOLTAGE")
    else:
        print("False:STATE_OVERLOAD_POWER_VOLTAGE")

    if (currStatus.Flags & StateFlags.STATE_OVERLOAD_POWER_CURRENT):
        print(" True:STATE_OVERLOAD_POWER_CURRENT")
    else:
        print("False:STATE_OVERLOAD_POWER_CURRENT")

    if (currStatus.Flags & StateFlags.STATE_OVERLOAD_USB_VOLTAGE):
        print(" True:STATE_OVERLOAD_USB_VOLTAGE")
    else:
        print("False:STATE_OVERLOAD_USB_VOLTAGE")

    if (currStatus.Flags & StateFlags.STATE_LOW_USB_VOLTAGE):
        print(" True:STATE_LOW_USB_VOLTAGE")
    else:
        print("False:STATE_LOW_USB_VOLTAGE")

    if (currStatus.Flags & StateFlags.STATE_OVERLOAD_USB_CURRENT):
        print(" True:STATE_OVERLOAD_USB_CURRENT")
    else:
        print("False:STATE_OVERLOAD_USB_CURRENT")

    if (currStatus.Flags & StateFlags.STATE_BORDERS_SWAP_MISSET):
        print(" True:STATE_BORDERS_SWAP_MISSET")
    else:
        print("False:STATE_BORDERS_SWAP_MISSET")

    if (currStatus.Flags & StateFlags.STATE_LOW_POWER_VOLTAGE):
        print(" True:STATE_LOW_POWER_VOLTAGE")
    else:
        print("False:STATE_LOW_POWER_VOLTAGE")

    if (currStatus.Flags & StateFlags.STATE_H_BRIDGE_FAULT):
        print(" True:STATE_H_BRIDGE_FAULT")
    else:
        print("False:STATE_H_BRIDGE_FAULT")
        
    if (currStatus.Flags & StateFlags.STATE_WINDING_RES_MISMATCH):
        print(" True:STATE_WINDING_RES_MISMATCH")
    else:
        print("False:STATE_WINDING_RES_MISMATCH")
        
    if (currStatus.Flags & StateFlags.STATE_ENCODER_FAULT):
        print(" True:STATE_ENCODER_FAULT")
    else:
        print("False:STATE_ENCODER_FAULT")
        
    if (currStatus.Flags & StateFlags.STATE_ENGINE_RESPONSE_ERROR):
        print(" True:STATE_ENGINE_RESPONSE_ERROR")
    else:
        print("False:STATE_ENGINE_RESPONSE_ERROR")
        
    if (currStatus.Flags & StateFlags.STATE_EXTIO_ALARM):
        print(" True:STATE_EXTIO_ALARM")
    else:
        print("False:STATE_EXTIO_ALARM")
        
def plot_move(deltatime):
    x = []
    y = []
    time1 = 0;
    while status_MvCmdSts_MVCMD_RUNNING(lib, device_id):
        x.append(time1)
        y.append(test_get_position(lib, device_id, userMode)[0])
        # print(y)
        time1 += deltatime 
        time.sleep(deltatime)
        plt.plot(x, y)
            
userMode = 0

# Create engine settings structure
eng = engine_settings_t()
result_eng = lib.get_engine_settings(device_id, byref(eng))

print(f'Result eng: {result_eng}')

# Create user unit settings structure
user_unit = calibration_t()
user_unit.MicrostepMode = eng.MicrostepMode
user_unit.A = 1 / 2000

target = 30 #where to go

test_move(lib, device_id, target, 0, userMode)

plot_move(0.01)

cur_pos = test_get_position(lib, device_id, mode=userMode)[0]

print(f'Current position: {cur_pos}')

lib.close_device(byref(cast(device_id, POINTER(c_int))))