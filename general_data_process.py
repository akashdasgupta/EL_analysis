from external_imports import *
from shutil import copyfile

def get_nominal_v(path):
    nominal_v = []
    with open(f"{path}\\LED_power_supply.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            nominal_v.append(float(row[0]))
    return np.array(nominal_v)

def get_exposure_list(path):
    exposures = []
    with open(f"{path}\\camera\\exposure_list.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            exposures.append(float(row[1]))
    return np.array(exposures)

def get_sm_data(path, illuminated_area):
    v = []
    i = []

    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            v.append(float(row[0]))
            i.append(float(row[1]))
    i = np.array(i)
    v = np.array(v)

    i /= illuminated_area
    return v,i

def white_over_cell_correction(white_exposure, led_specf, cell_specf, 
                          bandgap, camQEf, lenscalf, white_reflectivity, filterODf):
    wavel_range =  np.arange(300, 1000, 1)

    led_spec = led_specf(wavel_range)
    cell_spec = cell_specf(wavel_range, bandgap)

    cam_QE = camQEf(wavel_range)
    lens_cal = lenscalf(wavel_range)
    filter_OD = filterODf(wavel_range)

    white_factor =  integrate.simps((led_spec*cam_QE*lens_cal), wavel_range*1e-9) / integrate.simps(led_spec, wavel_range*1e-9)
    white_factor *= white_exposure * white_reflectivity

    cell_factor = integrate.simps((cell_spec*cam_QE*lens_cal*filter_OD), wavel_range*1e-9) / integrate.simps(cell_spec, wavel_range*1e-9)

    return white_factor/cell_factor

def copy_led_sm_data(datapath, savepath):

    if os.path.isfile(f"{datapath}\\source_meter.csv"):
        copyfile(f"{datapath}\\source_meter.csv", f"{savepath}\\source_meter.csv")

    if os.path.isfile(f"{datapath}\\LED_power_supply.csv"):
        copyfile(f"{datapath}\\LED_power_supply.csv", f"{savepath}\\LED_power_supply.csv")

    if os.path.isfile(f"{datapath}\\camera\\camera_setting_dump.txt"):
        copyfile(f"{datapath}\\camera\\camera_setting_dump.txt", f"{savepath}\\camera_setting_dump.txt")

    if os.path.isfile(f"{datapath}\\camera\\exposure_list.csv"):
        copyfile(f"{datapath}\\camera\\exposure_list.csv", f"{savepath}\\exposure_list.csv")


def open_wavelabs_data(filepath):
    V = []
    I = []
    with open(filepath,'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            try:
                V.append(float(row[0]))
                I.append(float(row[1]))
            except:
                pass
    return np.array(V), np.array(I)


